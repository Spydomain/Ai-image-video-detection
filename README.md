# 🛡️ IsItReal: Forensic Content Analyzer

**IsItReal** is a defensive cybersecurity tool designed to detect potentially AI-generated images and videos. Unlike simple metadata viewers, this tool performs **deep forensic analysis** on file containers, binary signatures, and visual compression artifacts to identify synthetic media.

## 🚀 Features

* **Deep Byte Scanning:** Scans raw binary data (head and tail) for hidden signatures from tools like Stable Diffusion, Midjourney, RunwayML, Pika Labs, and generic FFmpeg encoders (`Lavf`).
* **Video Forensics:** * **Container Analysis:** Flags generic `isom` containers (common in Python scripts/web-converters) vs. hardware-native `qt`/`mp4` containers (common in real cameras).
    * **Heuristic Profiling:** Detects suspicious FPS/Duration patterns (e.g., flat integer FPS + short duration).
    * **Texture Analysis:** Uses Laplacian Variance to detect unnaturally smooth frames common in AI video generation.
* **Image Forensics:**
    * **Metadata Extraction:** Parses EXIF, XMP, and PNG text chunks for generation parameters.
    * **Noise Analysis:** Flags abnormal pixel variance (too smooth or high artifact density).
* **Privacy Focused:** All analysis runs locally on your machine. No files are uploaded to the cloud.


### Setup
1.  **Clone the repository**
    ```bash
    git clone https://github.com/Spydomain/Ai-image-video-detection.git
    cd Ai-image-video-detection
    ```

2.  **Install Dependencies**
    ```bash
    pip install opencv-python Pillow
    ```
    *(Note: If you are on Arch/Ubuntu 24.04+, you may need to use a virtual environment or `--break-system-packages`)*

3.  **Run the Tool**
    ```bash
    python3 IsItReal.py
    ```

## 🧠 How It Works

### The "Isom" vs. "QT" Check
Real cameras (Sony, Canon, iPhone) typically save video using specific hardware encoders and container brands like `qt  ` (QuickTime) or `avc1`. 

AI tools and Python scripts (like those using MoviePy or ImageIO) almost exclusively use the generic **ISO Media (`isom`)** brand via FFmpeg. **IsItReal** flags `isom` containers as "Suspicious" when combined with other indicators like generic `Lavf` encoder tags.

### Deep Byte Scan
AI models often leave specific traces in the file's binary data (XMP packets or atom structures). This tool seeks through the file's header and footer bytes to match signatures against a database of known generative tools (e.g., `b"runwayml"`, `b"stable diffusion"`, `b"comfyui"`).

## 📸 Screenshots

*(You can upload the screenshots you took earlier to an 'assets' folder and link them here)*
!<img width="942" height="754" alt="image" src="https://github.com/user-attachments/assets/e1fd8610-1376-491d-b844-9af2cc2e840d" />


## 🤝 Contributing
Contributions are welcome! If you find new AI signatures or edge cases, please submit a Pull Request.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
