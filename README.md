# 🔥 Stego Scanner GUI Tool

A powerful Python GUI tool for scanning PNG images for hidden data using multiple forensic and steganography tools.

## 🚀 Features

* Multi-tool scanning:

  * strings
  * exiftool
  * binwalk
  * zsteg
  * steghide
  * foremost
* RGB channel extraction
* Hex dump analysis
* Auto flag detection (flag{}, hack{}, ctf{})
* GUI interface

## 🛠 Requirements

Install system tools:

```bash
sudo apt install steghide exiftool binwalk foremost
gem install zsteg
```

Install Python dependency:

```bash
pip install pillow
```

## ▶️ Run

```bash
python3 scanner.py
```

## 📸 Output

* GUI window with highlighted flags
* Extracted RGB images
* Multi-tool scan results

## ⚠️ Disclaimer

For educational and CTF use only.
