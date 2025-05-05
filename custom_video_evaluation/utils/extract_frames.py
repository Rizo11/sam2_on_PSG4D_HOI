import subprocess
import os

def path_to_string(video_path):
    """
    Convert a file path to a string by replacing path separators with underscores.

    Args:
        video_path (str): The input path (e.g., 'a/b/c').

    Returns:
        str: The path with separators replaced by underscores (e.g., 'a_b_c').
    """
    components = video_path.split(os.sep)
    
    # Remove the file extension from the last component
    last_component = os.path.splitext(components[-1])[0]
    components[-1] = last_component
    
    return '_'.join(components[-9:])
    
    return video_path.replace(os.sep, '_')


def extract_frames(mp4_path, output_dir):
    """
    Extracts frames from an MP4 video file and saves them as JPEG images in the specified output directory.

    The frames are named in the format '00000.jpg', '00001.jpg', etc., starting from 00000.

    Args:
        mp4_path (str): Path to the input MP4 video file.
        output_dir (str): Path to the directory where the extracted frames will be saved.

    Raises:
        FileNotFoundError: If the input MP4 file does not exist.
        subprocess.CalledProcessError: If the ffmpeg command fails.
    """
    
    print(10*"#", "Frame Extraction Started", 10*"#")
    
    # Check if the input MP4 file exists
    if not os.path.isfile(mp4_path):
        raise FileNotFoundError(f"The input MP4 file does not exist: {mp4_path}")
    
    output_dir = output_dir + "/" + path_to_string(mp4_path)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', mp4_path,       # Input file
        '-q:v', '2',          # Quality level for JPEG
        '-start_number', '0', # Start numbering from 0
        os.path.join(output_dir, '%05d.jpg')  # Output pattern
    ]
    
    
    # Run the ffmpeg command
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Frames extracted successfully to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting frames: {e}")
        raise
    
    print(10*"#", "Frame Extraction Ended", 10*"#")
    
    return output_dir

# Example usage
# if __name__ == "__main__":
#     mp4_file = "/home/rizo/mipt_ccm/sam2/hoi/HOI4D_release/ZY20210800001/H1/C14/N24/S367/s01/T1/align_rgb/image.mp4"
#     output_folder = "/home/rizo/mipt_ccm/sam2_eval/frames"
#     extract_frames(mp4_file, output_folder)