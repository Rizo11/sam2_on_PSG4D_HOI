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
