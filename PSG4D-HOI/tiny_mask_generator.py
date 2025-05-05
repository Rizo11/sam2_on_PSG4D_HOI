import os
import cv2

# Root folder containing your object subfolders (bottle_4, car_1, etc.)
ROOT_DIR = '/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations/tiny_C1_2_3_4'  # adjust if needed

# Skip factors and downsample targets must match your video script
SKIPS = [2, 5, 20]
DOWNSAMPLE_SIZES = [
    (1280, 720),
    (854, 480),
    (640, 360),
    (426, 240),
]

def process_mask_folder(mask_dir):
    # prepare output directories
    skip_dirs = {k: os.path.join(mask_dir, f"skip_{k}") for k in SKIPS}
    down_dirs = {
        (w, h): os.path.join(mask_dir, f"downsample_{w}_{h}")
        for (w, h) in DOWNSAMPLE_SIZES
    }
    for d in list(skip_dirs.values()) + list(down_dirs.values()):
        os.makedirs(d, exist_ok=True)

    # list all PNG masks in sorted order
    files = sorted([f for f in os.listdir(mask_dir) if f.endswith('.png')])
    skip_cnt = {k: 0 for k in SKIPS}
    down_cnt = {(w, h): 0 for (w, h) in DOWNSAMPLE_SIZES}

    for idx, fname in enumerate(files):
        src_path = os.path.join(mask_dir, fname)
        # load with unchanged flag to preserve palette/alpha if any
        mask = cv2.imread(src_path, cv2.IMREAD_UNCHANGED)
        if mask is None:
            print(f"WARNING: failed to load {src_path}")
            continue

        # SKIP folders
        for k in SKIPS:
            if (idx % k) != 1:
                out_name = f"{skip_cnt[k]:05d}.png"
                cv2.imwrite(os.path.join(skip_dirs[k], out_name), mask)
                skip_cnt[k] += 1

        # DOWNSAMPLE folders
        for (w, h) in DOWNSAMPLE_SIZES:
            resized = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
            out_name = f"{down_cnt[(w, h)]:05d}.png"
            cv2.imwrite(os.path.join(down_dirs[(w, h)], out_name), resized)
            down_cnt[(w, h)] += 1

    print(f"Processed masks in {mask_dir}: {len(files)} files")

def main():
    # Walk only one level deep: find folders containing .png masks
    for class_dir in os.listdir(ROOT_DIR):
        full_dir = os.path.join(ROOT_DIR, class_dir)
        if not os.path.isdir(full_dir):
            continue
        # Check for any PNGs
        pngs = [f for f in os.listdir(full_dir) if f.endswith('.png')]
        if not pngs:
            continue

        print(f">> Found mask folder: {full_dir}")
        process_mask_folder(full_dir)

if __name__ == '__main__':
    main()
