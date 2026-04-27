import os
import subprocess
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image

KEYWORDS = ["flag{", "ctf{", "hack{"]

def highlight(text):
    for line in text.split("\n"):
        if any(k in line.lower() for k in KEYWORDS):
            output.insert(tk.END, "🔥 " + line + "\n", "red")
        else:
            output.insert(tk.END, line + "\n")

def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd)
    except:
        return "Error running command"

def split_rgb(image_path, folder):
    img = Image.open(image_path)
    r, g, b = img.split()

    r.save(f"{folder}/R.png")
    g.save(f"{folder}/G.png")
    b.save(f"{folder}/B.png")

def scan():
    output.delete(1.0, tk.END)

    for f in os.listdir():
        if f.endswith(".png"):
            output.insert(tk.END, f"\n===== {f} =====\n")

            folder = f"results_{f}"
            os.makedirs(folder, exist_ok=True)

            # STRINGS
            highlight(run_cmd(f"strings {f}"))

            # EXIF
            highlight(run_cmd(f"exiftool {f}"))

            # BINWALK
            highlight(run_cmd(f"binwalk -e {f}"))

            # ZSTEG
            highlight(run_cmd(f"zsteg -a {f}"))

            # FOREMOST
            run_cmd(f"foremost -i {f} -o {folder}/foremost")

            # STEGHIDE
            highlight(run_cmd(f"steghide extract -sf {f} -p ''"))

            # HEX DUMP
            highlight(run_cmd(f"xxd {f}"))

            # RGB SPLIT
            split_rgb(f, folder)
            output.insert(tk.END, f"🎨 RGB channels saved in {folder}\n")

# GUI
root = tk.Tk()
root.title("🔥 ULTRA STEGO SCANNER")

btn = tk.Button(root, text="Start Scan", command=scan)
btn.pack()

output = scrolledtext.ScrolledText(root, width=110, height=35)
output.pack()

output.tag_config("red", foreground="red")

root.mainloop()