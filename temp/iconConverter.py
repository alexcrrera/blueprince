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
PRESERVE_ASPECT = True  # Set False to stretch

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


def convert_webp_to_jpg(input_folder, output_folder):
    """
    Converts all .webp images to .jpg and forces them to a fixed square size.
    Also updates rooms.json with full room entries if missing.
    """
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
                    img.thumbnail(FORCED_SIZE, Image.LANCZOS)
                    square_img = Image.new("RGB", FORCED_SIZE, (0, 0, 0))
                    x = (FORCED_SIZE[0] - img.width) // 2
                    y = (FORCED_SIZE[1] - img.height) // 2
                    square_img.paste(img, (x, y))
                    output_img = square_img
                else:
                    output_img = img.resize(FORCED_SIZE, Image.LANCZOS)

                output_img.save(jpg_path, "JPEG", quality=95)
                print(f"✅ Converted: {filename} → {jpg_filename}")

                # --- Update JSON if missing ---
                if base_name not in room_data:
                    room_data[base_name] = {
                        "image": jpg_filename,
                        "color": "bleue",
                        "rarity": 0,
                        "cost": 0,
                        "doors": ["N", "E", "W", "S"],
                        "placement_condition": 0,
                        "q": 1,
                        "items": {}
                    }
                    print(f"➕ Added new room entry: {base_name}")

        except Exception as e:
            print(f"❌ Error converting {filename}: {e}")

    # Save updated JSON file
    save_json(room_data, JSON_FILE)
    print("🎉 Conversion complete!")


# --- Run conversion ---
if __name__ == "__main__":
    print(f"🔧 Using forced size: {FORCED_SIZE}")
    print(f"📂 Input:  {INPUT_FOLDER}")
    print(f"📁 Output: {OUTPUT_FOLDER}")
    print(f"🧾 JSON:   {JSON_FILE}\n")

    convert_webp_to_jpg(INPUT_FOLDER, OUTPUT_FOLDER)
