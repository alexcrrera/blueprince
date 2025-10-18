import os
import sys
from PIL import Image

# --- Setup paths so we can import from src/ ---
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(parent_dir, "src"))

import params  # Now params.py is accessible


# --- Configuration ---
INPUT_FOLDER = os.path.join(parent_dir, "assets", "images", "images_webp")
OUTPUT_FOLDER = os.path.join(parent_dir, "assets", "images")

# Get forced square size from params (e.g. ROOM_TILE_SIZE = 100)
FORCED_SIZE = (params.IMAGE_CONVERSION_SIZE, params.IMAGE_CONVERSION_SIZE)

# If you want to preserve proportions instead of stretching:
PRESERVE_ASPECT = True  # Set False to stretch


# --- Ensure output folder exists ---
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_webp_to_jpg(input_folder, output_folder):
    """
    Converts all .webp images to .jpg and forces them to a fixed square size.
    Removes '_Icon' from filenames automatically.
    """
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".webp"):
            continue

        # Remove extension and "_Icon" suffix if present
        base_name = os.path.splitext(filename)[0]
        base_name = base_name.replace("_Icon", "")

        jpg_filename = base_name + ".jpg"
        webp_path = os.path.join(input_folder, filename)
        jpg_path = os.path.join(output_folder, jpg_filename)

        try:
            with Image.open(webp_path) as img:
                img = img.convert("RGB")  # JPG doesn't support alpha

                if PRESERVE_ASPECT:
                    # --- Keep proportions and pad with black ---
                    img.thumbnail(FORCED_SIZE, Image.LANCZOS)

                    # Create black background (square)
                    square_img = Image.new("RGB", FORCED_SIZE, (0, 0, 0))

                    # Center the image
                    x = (FORCED_SIZE[0] - img.width) // 2
                    y = (FORCED_SIZE[1] - img.height) // 2
                    square_img.paste(img, (x, y))
                    output_img = square_img
                else:
                    # --- Force exact size (stretch) ---
                    output_img = img.resize(FORCED_SIZE, Image.LANCZOS)

                # Save as JPEG
                output_img.save(jpg_path, "JPEG", quality=95)

                print(f"✅ Converted: {filename} → {jpg_filename} ({FORCED_SIZE[0]}x{FORCED_SIZE[1]})")

        except Exception as e:
            print(f"❌ Error converting {filename}: {e}")

    print("🎉 Conversion complete!")


# --- Run conversion ---
if __name__ == "__main__":
    print(f"🔧 Using forced size: {FORCED_SIZE}")
    print(f"📂 Input:  {INPUT_FOLDER}")
    print(f"📁 Output: {OUTPUT_FOLDER}\n")

    convert_webp_to_jpg(INPUT_FOLDER, OUTPUT_FOLDER)
