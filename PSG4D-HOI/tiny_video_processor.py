import os
import cv2

# configure your root directory here
ROOT_DIR = '/home/rizo/mipt_ccm/sam2/hoi/HOI4D_release/tiny_C1_2_3_4'  # or '.' if you run it from the parent folder

# define your skip settings and downsample targets
SKIPS = [2, 5, 20]
DOWNSAMPLE_SIZES = [
    (1280, 720),
    (854, 480),
    (640, 360),
    (426, 240),
]


def process_video(mp4_path):
    """
    For a single mp4:
    - Creates skip_N folders and downsamples folders
    - Extracts & saves frames per specification
    """
    base_dir = os.path.dirname(mp4_path)

    # prepare output directories
    skip_dirs = {k: os.path.join(base_dir, f"skip_{k}") for k in SKIPS}
    down_dirs = {
        (w, h): os.path.join(base_dir, f"downsample_{w}_{h}")
        for (w, h) in DOWNSAMPLE_SIZES
    }
    for d in list(skip_dirs.values()) + list(down_dirs.values()):
        os.makedirs(d, exist_ok=True)

    cap = cv2.VideoCapture(mp4_path)
    if not cap.isOpened():
        print(f"ERROR: could not open {mp4_path}")
        return

    frame_idx = 0
    # counters for saved frames in each output
    skip_cnt = {k: 0 for k in SKIPS}
    down_cnt = {(w, h): 0 for (w, h) in DOWNSAMPLE_SIZES}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # save in each skip_N folder if it's NOT the frame to skip
        for k in SKIPS:
            if (frame_idx % k) != 1:
                out_name = f"{skip_cnt[k]:05d}.jpg"
                out_path = os.path.join(skip_dirs[k], out_name)
                cv2.imwrite(out_path, frame)
                skip_cnt[k] += 1

        # save in each downsample folder (all frames)
        for (w, h) in DOWNSAMPLE_SIZES:
            resized = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
            out_name = f"{down_cnt[(w, h)]:05d}.jpg"
            out_path = os.path.join(down_dirs[(w, h)], out_name)
            cv2.imwrite(out_path, resized)
            down_cnt[(w, h)] += 1

        frame_idx += 1

    cap.release()
    print(f"Finished {mp4_path} – processed {frame_idx} frames.")


def main():
    # walk the tree
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        for fn in filenames:
            if fn.lower().endswith('.mp4'):
                mp4_path = os.path.join(dirpath, fn)
                print("Processing:", mp4_path)
                process_video(mp4_path)


if __name__ == '__main__':
    main()
