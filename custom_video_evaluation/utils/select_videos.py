import os
import random

def find_mp4_files(root):
    """Recursively find all 'image.mp4' files in the given root directory."""
    mp4_files = []
    for dirpath, _, filenames in os.walk(root):
        if 'image.mp4' in filenames:
            mp4_files.append(os.path.join(dirpath, 'image.mp4'))
    return mp4_files

def get_annotation_path(video_path, video_root, annotation_root):
    """Derive the corresponding annotation base path from a video path."""
    relative_path = os.path.relpath(video_path, video_root)
    parts = relative_path.split(os.sep)
    annotation_subpath = os.sep.join(parts[:-2])  # Remove 'align_rgb/image.mp4'
    annotation_subpath_2Dseg = os.path.join(annotation_subpath, '2Dseg/mask')
    annotation_subpath_objpose = os.path.join(annotation_subpath, 'objpose')
    return [os.path.join(annotation_root, annotation_subpath_2Dseg),
            os.path.join(annotation_root, annotation_subpath_objpose)]

def select_n_videos(
    N,
    video_root="/home/rizo/mipt_ccm/sam2/hoi/HOI4D_release",
    annotation_root="/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations"):
    """
    Select N random video paths and their corresponding annotation paths.

    Args:
        video_root (str): Root directory of the video dataset.
        annotation_root (str): Root directory of the annotation dataset.
        N (int): Number of videos to randomly select.

    Returns:
        tuple: Two lists containing N selected video paths and their annotation paths.

    Raises:
        ValueError: If the number of available videos is less than N.
    """
    print(10*"#", "Video Selection Sterted", 10*"#")
    # Generate all video paths
    all_mp4s = find_mp4_files(video_root)
    print(f"Found {len(all_mp4s)} videos in {video_root}")
    if len(all_mp4s) < N:
        raise ValueError(f"Found {len(all_mp4s)} videos, but {N} are required")
    
    # Set the seed
    random.seed(42)
    
    # Randomly select N video paths
    selected_mp4s = random.sample(all_mp4s, N)
    
    # Get corresponding annotation paths
    selected_annotations = [get_annotation_path(mp4, video_root, annotation_root) for mp4 in selected_mp4s]
    
    print(10*"#", "Video Selection Ended", 10*"#")
    
    return selected_mp4s, selected_annotations

# Example usage
# if __name__ == "__main__":
#     VIDEO_ROOT = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_release"
#     ANNOTATION_ROOT = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_annotations"
#     N = 5
    
#     video_paths, annotation_paths = select_n_videos(N)
    
#     print("Selected Video Paths:")
#     for i, v_path in enumerate(video_paths, 1):
#         print(f"{i}: {v_path}")
    
#     print("\nCorresponding Annotation Paths:")
#     for i, a_path in enumerate(annotation_paths, 1):
#         print(f"{i}: {a_path}")