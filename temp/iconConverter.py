from PIL import Image
import os

# --- Configuration ---
input_folder = "assets/images/images_webp"    # Folder containing .webp files


# --- Loop through all files ---
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".webp"):
        webp_path = os.path.join(input_folder, filename)
        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = jpg_filename

        # Open and convert the image
        with Image.open(webp_path) as img:
            rgb_img = img.convert("RGB")  # JPG doesn’t support alpha channel
            rgb_img.save(jpg_path, "JPEG", quality=95)

        print(f"✅ Converted: {filename} → {jpg_filename}")

print("🎉 Conversion complete!")
