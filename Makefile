# Makefile for packaging the PDF OCR Converter app with PyInstaller

# Variables
APP_NAME = "Anders PDF OCR Converter"
SCRIPT = main.py
DATA_FILE = ocr-to-pdf.sh
OUTPUT_DIR = dist

# Rule to build the application using PyInstaller
build:
	pyinstaller --onefile --name $(APP_NAME) --add-data $(DATA_FILE):. main.py


# Clean up build artifacts
clean:
	rm -rf build $(OUTPUT_DIR) $(APP_NAME).spec

.PHONY: build clean
