import os
import cv2
import numpy as np
from pixel2category import get_mask_and_label

def convert(frame_id, mask_path, output_segmentation_path):
    """
    Processes a single mask image.
    - Reads the mask image.
    - Uses get_mask_and_label() to obtain per-instance binary masks (ds) and corresponding labels.
    - Creates a segmentation label image where each pixel is assigned its label.
    - Saves the label image to output_segmentation_path.
    """
    mask_img = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    if mask_img is None:
        print("Mask image not found:", mask_path)
        return None, None, None
    # Ensure the mask is in the expected shape.
    assert mask_img.shape == (1080, 1920, 3), f"Unexpected mask shape: {mask_img.shape}"
    
    # get_mask_and_label() returns:
    # ds: a list of boolean arrays (each a binary mask for one instance)
    # ls: a list of semantic labels
    # ls_instanceseg: a list of instance labels (for instance segmentation)
    ds, ls, ls_instanceseg = get_mask_and_label(mask_path)
    
    # Create an empty label image
    segmentation = np.zeros((mask_img.shape[0], mask_img.shape[1]), dtype=np.uint8)
    # For each detected instance, assign its label to those pixels.
    for i, d in enumerate(ds):
        segmentation[d] = ls[i]
    
    output_segmentation_file = os.path.join(output_segmentation_path, frame_id + ".png")
    cv2.imwrite(output_segmentation_file, segmentation)
    return segmentation, ls, ls_instanceseg

def scene2frame(filelist, mask_folder, output_segmentation_path):
    """
    For each frame (as given by filelist), constructs the mask filename,
    processes it, and saves the resulting segmentation label image.
    """
    os.makedirs(output_segmentation_path, exist_ok=True)
    for filename in filelist:
        # Frame filenames in your video folder are 4-digit (e.g., "0000.jpg")
        # but the corresponding mask JSON/PNG is named as an integer with no leading zeros.
        base = os.path.splitext(filename)[0]
        try:
            frame_num = int(base)
        except ValueError:
            print("Invalid frame filename:", filename)
            continue
        frame_id = str(frame_num)
        # Build the mask filename. If masks are stored as "00000.png", "00001.png", etc.
        mask_file = os.path.join(mask_folder, frame_id.zfill(5) + '.png')
        if not os.path.exists(mask_file):
            print("Mask file does not exist:", mask_file)
            continue
        segmentation, ls, ls_instanceseg = convert(frame_id, mask_file, output_segmentation_path)
        print(f"Processed segmentation for frame {frame_id}")

def main(numFrames=300):
    # List of frame filenames from your video folder.
    # (They don't need to be read here, just used to create a list of expected frame numbers.)
    filelist = [f"{i}.jpg" for i in range(numFrames)]
    mask_folder = os.path.join("/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations/HOI4D_annotations/ZY20210800004/H4/C8/N14/S71/s03/T2/2Dseg", "shift_mask")
    output_segmentation_path = "/home/rizo/mipt_ccm/sam2_on_PSG4D_HOI/output_segmentation2"
    scene2frame(filelist, mask_folder, output_segmentation_path)

if __name__ == '__main__':
    main(numFrames=300)