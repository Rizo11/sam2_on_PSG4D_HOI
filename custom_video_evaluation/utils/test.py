import make_annotated_video
import extract_frames
import select_videos


VIDEO_ROOT = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_release"
ANNOTATION_ROOT = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations"
N = 5

video_paths, annotation_paths = select_videos.select_n_videos(N)

print("Selected Video Paths:")
for i, v_path in enumerate(video_paths, 1):
    print(f"{i}: {v_path}")

print("\nCorresponding Annotation Paths:")
for i, a_path in enumerate(annotation_paths, 1):
    print(f"{i}: {a_path}")
    
calibration_root = "/home/rizo/mipt_ccm/sam2_on_PSG4D_HOI/camera_params"
output_root = "/home/rizo/mipt_ccm/sam2_eval/annotated_video"

for i in range(N):
    video_path = video_paths[i]
    annotation_path = annotation_paths[i]
    
    # Extract frames from the video
    output_folder = "/home/rizo/mipt_ccm/sam2_eval/frames"
    frame_dir = extract_frames.extract_frames(video_path, output_folder)
    mask_dir = annotation_path[0]
    json_dir = annotation_path[1]
    
    
    # video_path = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_release/ZY20210800001/H1/C14/N24/S367/s01/T1/align_rgb"
    # frame_dir = "/home/rizo/mipt_ccm/sam2_eval/frames/ZY20210800001_H1_C14_N24_S367_s01_T1_align_rgb_image"
    # mask_dir = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations/ZY20210800001/H1/C14/N24/S367/s01/T1/2Dseg/mask"
    # json_dir = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations/ZY20210800001/H1/C14/N24/S367/s01/T1/objpose"
    
    make_annotated_video.annotate_and_save_video(
        video_path, frame_dir, mask_dir, json_dir, calibration_root, output_root)