#!/bin/bash

# Script to convert a PDF to an OCR-processed version with a specified language
# Usage: ./convert_to_ocr.sh <input-pdf> <language> [output-pdf]
# Example:
#   ./convert_to_ocr.sh document.pdf eng                     # For English OCR, replaces input file
#   ./convert_to_ocr.sh document.pdf chi_sim+swe output.pdf  # For Chinese and Swedish OCR, saves as output.pdf

# Check if the required arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <input-pdf> <language> [output-pdf]"
    echo "Examples of language codes:"
    echo "  eng        : English"
    echo "  chi_sim    : Simplified Chinese"
    echo "  swe        : Swedish"
    echo "  chi_sim+swe: Simplified Chinese and Swedish"
    echo "You must provide at least the input PDF file and the OCR language."
    exit 1
fi

# Input PDF
INPUT_PDF="$1"

# OCR language
OCR_LANGUAGE="$2"

# Output PDF
if [ -z "$3" ]; then
    # Default to replacing the original file if no output file is specified
    OUTPUT_PDF="$INPUT_PDF"
else
    OUTPUT_PDF="$3"
fi

# Check if the input file exists
if [ ! -f "$INPUT_PDF" ]; then
    echo "Error: File '$INPUT_PDF' not found!"
    exit 1
fi

# Temporary OCR output file if replacing the input
TEMP_OCR_PDF="${INPUT_PDF%.pdf}_ocr_temp.pdf"

# Run ocrmypdf to perform OCR conversion with the specified language
ocrmypdf -f -l "$OCR_LANGUAGE" \
  --output-type pdf \
  --image-dpi 150 \
  --jbig2-lossy \
  --fast-web-view 1 \
  --optimize 3 \
  "$INPUT_PDF" "$TEMP_OCR_PDF"

# Check if ocrmypdf succeeded
if [ $? -eq 0 ]; then
    # Move the temporary OCR file to the specified output file
    mv "$TEMP_OCR_PDF" "$OUTPUT_PDF"
    echo "OCR conversion completed with language '$OCR_LANGUAGE'."
    echo "Output saved to '$OUTPUT_PDF'."
else
    echo "Error: OCR conversion failed. The original file has not been modified."
    # Remove temporary OCR output file if it exists
    [ -f "$TEMP_OCR_PDF" ] && rm "$TEMP_OCR_PDF"
    exit 1
fi
