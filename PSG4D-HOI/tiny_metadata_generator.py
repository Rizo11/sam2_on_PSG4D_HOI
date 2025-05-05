import os
import cv2
import json

# Root of your experiments
ROOT_DIR = '/home/rizo/mipt_ccm/sam2/hoi/HOI4D_release/tiny_C1_2_3_4'

# Assumed constant fps for all experiments
FPS = 5

def extract_meta_from_folder(folder_path):
    """
    - Counts the number of image files (.jpg, .png)
    - Infers width/height from the first image found
    - Returns dict(height, width, fps, num_frames)
    """
    imgs = sorted([f for f in os.listdir(folder_path)
                   if f.lower().endswith(('.jpg', '.png'))])
    if not imgs:
        return None

    # Count frames
    num_frames = len(imgs)

    # Read first image to get dimensions
    first_img = cv2.imread(os.path.join(folder_path, imgs[0]), cv2.IMREAD_UNCHANGED)
    if first_img is None:
        return None
    h, w = first_img.shape[:2]

    return {
        "height": h,
        "width":  w,
        "fps":    FPS,
        "num_frames": num_frames
    }

def main():
    entries = []

    # Walk one level deep: for each video subfolder
    for video_folder in sorted(os.listdir(ROOT_DIR)):
        vf_path = os.path.join(ROOT_DIR, video_folder)
        if not os.path.isdir(vf_path):
            continue

        # Look for all skip_* and downsample_* dirs
        for sub in sorted(os.listdir(vf_path)):
            if not (sub.startswith('skip_') or sub.startswith('downsample_')):
                continue

            folder_path = os.path.join(vf_path, sub)
            if not os.path.isdir(folder_path):
                continue

            meta = extract_meta_from_folder(folder_path)
            if meta is None:
                print(f"Skipping empty or unreadable folder: {folder_path}")
                continue

            entries.append({
                "video_id": os.path.join(ROOT_DIR, video_folder, sub).replace('\\','/'),
                "meta": meta
            })

    # Dump to stdout or file
    print(json.dumps(entries, indent=2))

if __name__ == '__main__':
    main()
