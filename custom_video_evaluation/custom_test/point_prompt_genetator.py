import os
import random
from PIL import Image
import matplotlib.pyplot as plt


        
        
def display_random_image(folder_path):
    """
    Read one random image from a folder and display it using matplotlib.
    Clicking on the image prints the pixel coordinates.

    Args:
        folder_path (str): Path to the folder containing images.

    Raises:
        ValueError: If the folder is empty or contains no valid image files.
        FileNotFoundError: If the folder does not exist.
    """
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"The folder does not exist: {folder_path}")

    # Get list of image files (supporting common formats)
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
    )
    
    if not image_files:
        raise ValueError(f"No valid image files found in {folder_path}")

    # Randomly select one image
    selected_image = random.choice(image_files)
    image_path = os.path.join(folder_path, selected_image)

    # Read the image using PIL
    image = Image.open(image_path)

    # Create a matplotlib figure and display the image
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(image)
    ax.set_title(f"Random Image: {selected_image}")
    ax.axis('off')  # Hide axes

    def on_click(event):
        """
        Callback function to handle mouse click events on the image.
        Prints the pixel coordinates (x, y) of the clicked point.
        """
        if event.inaxes:  # Check if the click is within the image axes
            x, y = int(event.xdata), int(event.ydata)
            print(f"{selected_image}: Clicked at pixel coordinates: (x={x}, y={y})")
            return
        
    # Connect the click event to the callback function
    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()
    
    
frames_dark_1 = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_dark_1"
frames_dark_2 = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_dark_2"
frames_light_1 = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_light_1"
frames_light_2 = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_light_2"
frames_light_3 = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_light_3"
frames_light_4 = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_light_4"
frames_light_5 = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_light_5"
frames_card = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_card"
frames_short = "/home/rizo/mipt_ccm/sam2_eval/custom_test/frames/_home_rizo_mipt_ccm_sam2_eval_custom_test_short"

for i in range(1, 15):
    print(f"Displaying random image from frames_dark_{i}")
    display_random_image(frames_card)