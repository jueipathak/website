import os
from PIL import Image

# Configuration
DIRECTORY = "./assets/img"  # Root directory to search for images
QUALITY = 82            # 80-85 is optimal for web delivery
DELETE_ORIGINALS = False # Set to True if you want to delete original PNG/JPG files after conversion

# Supported file extensions
EXTENSIONS = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")

def convert_images_to_webp(root_dir, quality=82, delete_originals=False):
    converted_count = 0
    total_saved_bytes = 0

    print(f"Starting conversion in: {os.path.abspath(root_dir)}\n")

    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(EXTENSIONS):
                original_path = os.path.join(dirpath, file)
                filename_without_ext = os.path.splitext(original_path)[0]
                webp_path = f"{filename_without_ext}.webp"

                try:
                    # Open and process image
                    with Image.open(original_path) as img:
                        # Convert RGBA/P modes to RGB if converting JPEG-like transparency-free targets
                        # Pillow automatically handles PNG transparency when saving to WebP
                        img.save(webp_path, "WEBP", quality=quality, optimize=True)

                    original_size = os.path.getsize(original_path)
                    webp_size = os.path.getsize(webp_path)
                    saved_bytes = original_size - webp_size
                    total_saved_bytes += max(0, saved_bytes)

                    print(f"✔ Converted: {file} -> {os.path.basename(webp_path)}")
                    print(f"  Size: {original_size / 1024:.1f}KB → {webp_size / 1024:.1f}KB ({saved_bytes / 1024:.1f}KB saved)\n")

                    converted_count += 1

                    # Remove original file if enabled
                    if delete_originals:
                        os.remove(original_path)

                except Exception as e:
                    print(f"❌ Failed to convert {original_path}: {e}\n")

    print("=" * 40)
    print(f"Done! Converted {converted_count} images.")
    print(f"Total space saved: {total_saved_bytes / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    convert_images_to_webp(DIRECTORY, quality=QUALITY, delete_originals=DELETE_ORIGINALS)