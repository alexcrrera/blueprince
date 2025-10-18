import os
import sys
import json
from PIL import Image

# --- Setup paths so we can import from src/ ---
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(parent_dir, "src"))

import params  # Now params.py is accessible

# --- Configuration ---
INPUT_FOLDER = os.path.join(parent_dir, "assets", "images", "images_webp")
OUTPUT_FOLDER = os.path.join(parent_dir, "assets", "images", "rooms")
JSON_FILE = os.path.join(parent_dir, "src", "rooms.json")

FORCED_SIZE = (params.IMAGE_CONVERSION_SIZE, params.IMAGE_CONVERSION_SIZE)
PRESERVE_ASPECT = True  # Keep aspect ratio but fill the square (no black border)

# --- Ensure output folder exists ---
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def load_or_create_json(json_path):
    """Loads existing JSON or creates a new one."""
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ JSON file was empty or invalid, recreating it.")
                data = {}
    else:
        data = {}
    return data

def save_json(data, json_path):
    """Saves the JSON dictionary neatly formatted."""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"💾 Updated JSON file: {json_path}")

def resize_and_crop(img, size):
    """Resize the image to fill the target size and crop excess (no black borders)."""
    target_w, target_h = size
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        # Image trop large → on ajuste la hauteur
        new_height = target_h
        new_width = int(new_height * img_ratio)
    else:
        # Image trop haute → on ajuste la largeur
        new_width = target_w
        new_height = int(new_width / img_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Crop au centre pour garder un carré parfait
    left = (new_width - target_w) // 2
    top = (new_height - target_h) // 2
    right = left + target_w
    bottom = top + target_h

    return img.crop((left, top, right, bottom))

def convert_webp_to_jpg(input_folder, output_folder):
    """Convert all .webp images to .jpg and update rooms.json."""
    room_data = load_or_create_json(JSON_FILE)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".webp"):
            continue

        base_name = os.path.splitext(filename)[0].replace("_Icon", "")
        jpg_filename = base_name + ".jpg"

        webp_path = os.path.join(input_folder, filename)
        jpg_path = os.path.join(output_folder, jpg_filename)

        try:
            with Image.open(webp_path) as img:
                img = img.convert("RGB")

                if PRESERVE_ASPECT:
                    output_img = resize_and_crop(img, FORCED_SIZE)
                else:
                    output_img = img.resize(FORCED_SIZE, Image.LANCZOS)

                output_img.save(jpg_path, "JPEG", quality=95)
                print(f"✅ Converted: {filename} → {jpg_filename}")

                if base_name not in room_data:
                    room_data[base_name] = jpg_filename
                    print(f"➕ Added to JSON: {base_name} → {jpg_filename}")

        except Exception as e:
            print(f"❌ Error converting {filename}: {e}")

    save_json(room_data, JSON_FILE)
    print("🎉 Conversion complete!")

# --- Run conversion ---
if __name__ == "__main__":
    print(f"🔧 Using forced size: {FORCED_SIZE}")
    print(f"📂 Input:  {INPUT_FOLDER}")
    print(f"📁 Output: {OUTPUT_FOLDER}")
    print(f"🧾 JSON:   {JSON_FILE}\n")

    convert_webp_to_jpg(INPUT_FOLDER, OUTPUT_FOLDER)
