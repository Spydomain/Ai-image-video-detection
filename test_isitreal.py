import unittest
import os
import sys
import contextlib

# Import your class
from IsItReal import MediaScanner

# --- Helper to silence C-level library noise (like OpenCV/FFmpeg) ---
@contextlib.contextmanager
def suppress_stderr():
    """
    Redirects standard error to /dev/null to silence libraries like OpenCV
    that print directly to the console.
    """
    # Open the null device
    with open(os.devnull, 'w') as devnull:
        # Save the original stderr file descriptor
        try:
            old_stderr = os.dup(sys.stderr.fileno())
            # Replace stderr with null device
            os.dup2(devnull.fileno(), sys.stderr.fileno())
            yield
        except Exception:
            # If for some reason redirection fails, just run normally
            yield
        finally:
            # Restore original stderr
            try:
                os.dup2(old_stderr, sys.stderr.fileno())
                os.close(old_stderr)
            except Exception:
                pass

class TestIsItReal(unittest.TestCase):
    
    def setUp(self):
        self.scanner = MediaScanner()
        
        # 1. AI Image
        self.ai_image = "test_ai_gen.jpg"
        with open(self.ai_image, "wb") as f:
            f.write(b"\xFF\xD8\xFF" + b"padding" * 50 + b"stable diffusion")
            
        # 2. Clean Image
        self.clean_image = "test_clean.jpg"
        with open(self.clean_image, "wb") as f:
            f.write(b"\xFF\xD8\xFF" + b"random pixel data " * 100)
            
        # 3. Video with Software Encoder (Lavf)
        self.encoded_video = "test_encoded.mp4"
        with open(self.encoded_video, "wb") as f:
            # Fake MP4 header 
            f.write(b"\x00\x00\x00\x18ftypmp42" + b"padding" * 50 + b"lavf") 
            
        # 4. Video with Suspicious Container (isom)
        self.bad_container = "test_suspicious.mp4"
        with open(self.bad_container, "wb") as f:
            f.write(b"\x00\x00\x00\x20ftypisom" + b"data" * 20)

    def test_1_ai_signature_detection(self):
        """Tests if the scanner correctly identifies 'stable diffusion'."""
        verdict, color, flags = self.scanner.analyze_authenticity(self.ai_image, "image")
        self.assertIn("Likely Generated", verdict)
        self.assertTrue(any("stable diffusion" in f.lower() for f in flags))

    def test_2_clean_file_check(self):
        """Tests a file with no suspicious markers."""
        verdict, color, flags = self.scanner.analyze_authenticity(self.clean_image, "image")
        self.assertEqual(verdict, "Likely Authentic")
        self.assertEqual(len(flags), 0)

    def test_3_software_encoder_detection(self):
        """Tests 'lavf' detection (Silencing OpenCV error logs)."""
        with suppress_stderr():
            verdict, color, flags = self.scanner.analyze_authenticity(self.encoded_video, "video")
        
        self.assertTrue(any("lavf" in f.lower() for f in flags))

    def test_4_container_analysis(self):
        """Tests 'isom' container detection (Silencing OpenCV error logs)."""
        with suppress_stderr():
            verdict, color, flags = self.scanner.analyze_authenticity(self.bad_container, "video")
        
        self.assertTrue(any("isom" in f.lower() for f in flags))

    def test_5_metadata_structure(self):
        """Tests if metadata extraction works."""
        meta = self.scanner.extract_metadata(self.clean_image, "image")
        self.assertIsInstance(meta, dict)
        self.assertIn("File Size", meta)

    def tearDown(self):
        files = [self.ai_image, self.clean_image, self.encoded_video, self.bad_container]
        for f in files:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    unittest.main(verbosity=2)