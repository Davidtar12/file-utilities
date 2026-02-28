import subprocess
import os
import sys


def compress_pdf(input_file, output_file, quality, gs_path):
    """
    Compress the PDF using Ghostscript with additional image downsampling and a higher PDF compatibility level.
    """
    command = [
        gs_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.5",  # Increase compatibility level to enable object streams
        f"-dPDFSETTINGS={quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        # Downsampling and compression options:
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        "-dEmbedAllFonts=true",
        "-dColorImageDownsampleType=/Bicubic",
        "-dColorImageResolution=50",  # Lowering from 72 to 50 DPI
        "-dGrayImageDownsampleType=/Bicubic",
        "-dGrayImageResolution=50",
        "-dMonoImageDownsampleType=/Subsample",
        "-dMonoImageResolution=50",
        "-sOutputFile=" + output_file,
        input_file
    ]
    subprocess.run(command, check=True)


def get_file_size(file_path):
    return os.path.getsize(file_path)


def main():
    if len(sys.argv) < 3:
        print("Usage: python compresspdf.py input.pdf output.pdf")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    target_size = 20 * 1024 * 1024  # 20 MB in bytes

    # Path to your Ghostscript executable:
    gs_path = r"C:\Program Files\gs\gs10.03.0\bin\gswin64c.exe"

    # Quality settings from best quality to most aggressive:
    quality_settings = ["/prepress", "/printer", "/ebook", "/screen"]

    for quality in quality_settings:
        try:
            print(f"Trying quality setting: {quality}")
            compress_pdf(input_file, output_file, quality, gs_path)
        except subprocess.CalledProcessError:
            print(f"Error during compression with quality setting {quality}.")
            continue

        file_size = get_file_size(output_file)
        print(f"Resulting file size with {quality}: {file_size / (1024 * 1024):.2f} MB")
        if file_size < target_size:
            print("Success: Output file is below 20 MB.")
            return
    print("Failed to compress the PDF to below 20 MB with available quality settings.")


if __name__ == "__main__":
    main()
