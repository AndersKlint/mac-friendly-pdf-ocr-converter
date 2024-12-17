import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import subprocess
import os
import platform

# Function to check and install dependencies (only on macOS)
def install_dependencies():
    if platform.system() != "Darwin":
        # Skip installation on Linux or other systems
        return
    
    # Check if Homebrew is installed
    if not subprocess.run(["which", "brew"], capture_output=True).stdout:
        # Install Homebrew if not found
        messagebox.showinfo("Installing Dependencies", "Homebrew not found. Installing Homebrew...")
        subprocess.run(["/bin/bash", "-c", "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"], check=True)

    # Check if Tesseract is installed
    if not subprocess.run(["which", "tesseract"], capture_output=True).stdout:
        # Install Tesseract if not found
        messagebox.showinfo("Installing Dependencies", "Tesseract not found. Installing Tesseract...")
        subprocess.run(["brew", "install", "tesseract"], check=True)

    # Check if Tesseract language packs are installed
    language_check = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True)
    if "tesseract-lang" not in language_check.stdout:
        messagebox.showinfo("Installing Dependencies", "Installing Tesseract language packs...")
        subprocess.run(["brew", "install", "tesseract-lang"], check=True)

# Function to run OCR script
def run_ocr():
    # Ask user for input file
    input_pdf = filedialog.askopenfilename(title="Select Input PDF", filetypes=[("PDF files", "*.pdf")])
    if not input_pdf:
        return  # Exit if no file selected

    # Create a top-level window for the OCR language input
    ocr_language_window = tk.Toplevel(root)
    ocr_language_window.title("Enter OCR Language")

    # Ask user for OCR language with a more verbose explanation
    ocr_language_label = tk.Label(ocr_language_window, text="Enter OCR language (e.g., eng for English, chi_sim+swe for Chinese and Swedish):")
    ocr_language_label.pack(pady=10)

    ocr_language_entry = tk.Entry(ocr_language_window, width=50)
    ocr_language_entry.insert(0, "chi_sim+swe")
    ocr_language_entry.pack(pady=10)

    # Add explanation below the input box
    iso_label = tk.Label(ocr_language_window, text="Languages are identified by standardized three-letter codes (called ISO 639-2 Alpha-3).")
    iso_label.pack(pady=5)

    def on_submit():
        ocr_language = ocr_language_entry.get()
        if not ocr_language:
            return  # Exit if no OCR language provided
        ocr_language_window.destroy()  # Close the input window

        # Ask user for output file
        output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_pdf:
            return  # Exit if no output file provided

        # Install dependencies only on macOS
        install_dependencies()

        # Prepare and execute the command
        command = f"./ocr-to-pdf.sh \"{input_pdf}\" \"{ocr_language}\" \"{output_pdf}\""
        try:
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("Success", f"OCR conversion completed. Output saved to '{output_pdf}'")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error during OCR conversion: {e}")

    # Add submit button to capture input
    submit_button = tk.Button(ocr_language_window, text="Submit", command=on_submit)
    submit_button.pack(pady=20)

# Create the main window
root = tk.Tk()
root.title("PDF OCR Converter")

# Add a simple button to trigger the OCR process
button = tk.Button(root, text="Start OCR Conversion", command=run_ocr)
button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
