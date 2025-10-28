import os
import json

def generate_sfx_json():
    # Path of this script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Paths relative to this script
    sfx_dir = os.path.join(base_dir, "..", "assets", "audio", "sfx")
    output_file = os.path.join(base_dir, "..", "src", "sfx.json")

    if not os.path.exists(sfx_dir):
        raise FileNotFoundError(f"Directory not found: {sfx_dir}")

    # Collect all .mp3 files in the sfx folder
    sfx_files = [f for f in os.listdir(sfx_dir) if f.lower().endswith(".mp3")]

    # Create dictionary with clean paths relative to project root
    sfx_dict = {
        os.path.splitext(f)[0]: f"assets/audio/sfx/{f}"
        for f in sfx_files
    }

    # Save JSON file inside src/
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sfx_dict, f, indent=4, ensure_ascii=False)

    print(f"✅ Created {output_file} with {len(sfx_files)} entries.")


if __name__ == "__main__":
    generate_sfx_json()
