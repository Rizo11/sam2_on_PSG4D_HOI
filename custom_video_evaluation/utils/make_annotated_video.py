import cv2
import numpy as np
import json
import os
import tempfile
import shutil
from moviepy.editor import ImageSequenceClip
from PIL import Image
import matplotlib.pyplot as plt

from pathlib import Path
from path_to_string import path_to_string

def find_zy_directory(path):
    p = Path(path)
    for part in p.parts:
        if part.startswith("ZY"):
            return part
    return None

def load_calibration(video_path, calibration_root):
    """Load the intrinsic calibration matrix based on the camera ID from the video path."""
    camera_id = find_zy_directory(video_path)  # e.g., 'ZY20210800001'
    calib_path = os.path.join(calibration_root, camera_id, 'intrin.npy')
    K = np.load(calib_path)
    return K

def project_3d_to_2d(K, center):
    """Project a 3D point in camera coordinates to 2D image coordinates."""
    X = np.array([center['x'], center['y'], center['z']])
    uvw = K @ X
    u, v = uvw[0] / uvw[2], uvw[1] / uvw[2]
    return int(u), int(v)

def get_color(obj_id):
    """Generate a unique color for each object ID."""
    cmap = plt.get_cmap('tab10')
    color = cmap(obj_id % 10)[:3]
    return tuple(int(255 * c) for c in color)

def get_output_video_path(video_path, output_root):
    """Determine the output video path based on the input video path."""
    video_name = path_to_string(video_path)
    output_path = os.path.join(output_root, f"{video_name}_annotated.mp4")
    return output_path

def annotate_and_save_video(video_path, frame_dir, mask_dir, json_dir, calibration_root, output_root):
    """
    Annotate video frames with segmentation masks, bounding boxes, object names, and centers,
    then save the result as a video.
    
    Args:
        video_path (str): Path to the original video (e.g., 'ZY20210800001/H1/C6/.../image.mp4')
        frame_dir (str): Directory containing JPEG frames (e.g., '00000.jpg')
        mask_dir (str): Directory containing mask PNGs (e.g., '00000.png')
        json_dir (str): Directory containing JSON annotations (e.g., '00000.json')
        calibration_root (str): Root directory of calibration files
        video_root (str): Root directory of input videos
        output_root (str): Root directory for output videos
    """
    
    print(10*"#", "Video Annotation Started", 10*"#")
    
    # Load calibration matrix
    K = load_calibration(video_path, calibration_root)
    
    # Prepare output video path
    output_video_path = get_output_video_path(video_path, output_root)
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    
    # Create temporary directory for annotated frames
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Process each frame (assuming 300 frames, adjust as needed)
        for frame_idx in range(300):
            # Load the JPEG frame
            image_path = os.path.join(frame_dir, f'{frame_idx:05d}.jpg')
            image = cv2.imread(image_path)
            if image is None:
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Load the segmentation mask
            mask_path = os.path.join(mask_dir, f'{frame_idx:05d}.png')
            mask = np.array(Image.open(mask_path))
            
            # Load the JSON annotations
            json_path = os.path.join(json_dir, f'{frame_idx:d}.json')
            if not Path(json_path).exists():
                json_path = os.path.join(json_dir, f'{frame_idx:5d}.json')
                
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            # Annotate each object
            for obj in data['dataList']:
                obj_id = obj['id']
                label = obj['label']
                center_3d = obj['center']
                
                # Project 3D center to 2D image coordinates
                u, v = project_3d_to_2d(K, center_3d)
                
                # Extract binary mask for this object
                binary_mask = (mask == obj_id).astype(np.uint8)
                
                # Compute bounding box from the mask
                print(binary_mask.shape)
                print(binary_mask)
                print(mask_path)
                
                contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if not contours:
                    continue  # Skip if no mask exists for this object
                x, y, w, h = cv2.boundingRect(contours[0])
                
                # Get a unique color for this object
                color = get_color(obj_id)
                
                # Apply segmentation mask with transparency
                mask_colored = np.zeros_like(image)
                mask_colored[binary_mask == 1] = color
                alpha = 0.5
                image = cv2.addWeighted(image, 1, mask_colored, alpha, 0)
                
                # Draw bounding box
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                
                # Draw a star (circle) at the center
                cv2.circle(image, (u, v), 5, color, -1)
                
                # Write object name above the center
                cv2.putText(image, label, (u, v - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # Save the annotated frame
            annotated_path = os.path.join(temp_dir, f'{frame_idx:05d}.jpg')
            cv2.imwrite(annotated_path, image)
        
        # Combine annotated frames into a video
        frames = [os.path.join(temp_dir, f'{i:05d}.jpg') for i in range(300)]
        clip = ImageSequenceClip(frames, fps=30)
        clip.write_videofile(output_video_path, codec='libx264')
        print(f"Video saved to {output_video_path}")
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
    
    print(10*"#", "Video Annotation Ended", 10*"#")

# Example usage
if __name__ == "__main__":
    video_path = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_release/ZY20210800001/H1/C14/N24/S367/s01/T1/align_rgb"
    frame_dir = "/home/rizo/mipt_ccm/sam2_eval/frames/ZY20210800001_H1_C14_N24_S367_s01_T1_align_rgb_image"
    mask_dir = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations/ZY20210800001/H1/C14/N24/S367/s01/T1/2Dseg/mask"
    json_dir = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations/ZY20210800001/H1/C14/N24/S367/s01/T1/objpose"
    calibration_root = "/home/rizo/mipt_ccm/sam2_on_PSG4D_HOI/camera_params"
    output_root = "/home/rizo/mipt_ccm/sam2_eval/annotated_video"
    
    annotate_and_save_video(video_path, frame_dir, mask_dir, json_dir, calibration_root, output_root)