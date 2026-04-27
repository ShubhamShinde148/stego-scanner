import os
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image

# 🔍 Keywords for flag detection
KEYWORDS = ["flag{", "ctf{", "hack{"]

selected_file = None

# -----------------------------
# 🔧 Run system command
# -----------------------------
def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd)
    except:
        return "Error running command"

# -----------------------------
# 🔥 Highlight important lines
# -----------------------------
def highlight(text):
    for line in text.split("\n"):
        if any(k in line.lower() for k in KEYWORDS):
            output.insert(tk.END, "🔥 " + line + "\n", "red")
        else:
            output.insert(tk.END, line + "\n")

# -----------------------------
# 📂 Select PNG file
# -----------------------------
def choose_file():
    global selected_file
    selected_file = filedialog.askopenfilename(
        filetypes=[("PNG Files", "*.png")]
    )
    if selected_file:
        output.insert(tk.END, f"\n📁 Selected: {selected_file}\n")

# -----------------------------
# 🎨 RGB Channel Split
# -----------------------------
def split_rgb(image_path):
    folder = "results"
    os.makedirs(folder, exist_ok=True)

    img = Image.open(image_path)
    r, g, b = img.split()

    r.save(f"{folder}/R.png")
    g.save(f"{folder}/G.png")
    b.save(f"{folder}/B.png")

    output.insert(tk.END, "🎨 RGB channels saved in 'results/' folder\n")

# -----------------------------
# 🚀 Main Scan Function
# -----------------------------
def scan():
    output.delete(1.0, tk.END)

    if not selected_file:
        output.insert(tk.END, "❌ Please select a PNG file first\n")
        return

    f = selected_file
    output.insert(tk.END, f"\n===== Scanning: {f} =====\n\n")

    # STRINGS
    output.insert(tk.END, "\n[1] 🔤 Strings Scan\n")
    highlight(run_cmd(f"strings \"{f}\""))

    # EXIF
    output.insert(tk.END, "\n[2] 📸 EXIF Metadata\n")
    highlight(run_cmd(f"exiftool \"{f}\""))

    # BINWALK
    output.insert(tk.END, "\n[3] 📦 Binwalk Scan\n")
    highlight(run_cmd(f"binwalk -e \"{f}\""))

    # ZSTEG
    output.insert(tk.END, "\n[4] 🔎 Zsteg Scan\n")
    highlight(run_cmd(f"zsteg -a \"{f}\""))

    # STEGHIDE
    output.insert(tk.END, "\n[5] 🔐 Steghide Extract\n")
    highlight(run_cmd(f"steghide extract -sf \"{f}\" -p ''"))

    # FOREMOST
    output.insert(tk.END, "\n[6] 🧩 Foremost Carving\n")
    highlight(run_cmd(f"foremost -i \"{f}\" -o results/foremost"))

    # HEX DUMP
    output.insert(tk.END, "\n[7] 🧠 Hex Dump\n")
    highlight(run_cmd(f"xxd \"{f}\""))

    # RGB SPLIT
    output.insert(tk.END, "\n[8] 🎨 RGB Analysis\n")
    split_rgb(f)

    output.insert(tk.END, "\n✅ Scan Completed!\n")

# -----------------------------
# 🖥️ GUI Setup
# -----------------------------
root = tk.Tk()
root.title("🔥 Stego Scanner GUI Tool")
root.geometry("900x600")

# Buttons
file_btn = tk.Button(root, text="📂 Select PNG", command=choose_file)
file_btn.pack(pady=5)

scan_btn = tk.Button(root, text="🔥 Start Scan", command=scan)
scan_btn.pack(pady=5)

# Output box
output = scrolledtext.ScrolledText(root, width=110, height=30)
output.pack(padx=10, pady=10)

# Highlight style
output.tag_config("red", foreground="red")

# Run GUI
root.mainloop()
