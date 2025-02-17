from PIL import Image
import numpy as np

# Function to convert an image to a binary matrix (1 for black, 0 for non-black)
def convert_to_binary(image_path, tolerance=0):
    image = Image.open(image_path).convert('RGB')
    np_image = np.array(image)

    # Modify the black_mask to include tolerance
    black_mask = (
        (np_image[:, :, 0] <= tolerance) &
        (np_image[:, :, 1] <= tolerance) &
        (np_image[:, :, 2] <= tolerance)
    )

    # Binary image: 1 for black, 0 for everything else
    binary_image = np.zeros((np_image.shape[0], np_image.shape[1]), dtype=np.uint8)
    binary_image[black_mask] = 1

    # Add debug statements
    num_black_pixels = np.sum(binary_image)
    print(f"Number of black pixels in {image_path} with tolerance {tolerance}: {num_black_pixels}")

    return binary_image, np_image.shape[0] * np_image.shape[1]

# Function to compare two images based on their black pixels
def compare_images(image_path1, image_path2, tolerance=0):
    # Convert both images to binary matrices with the given tolerance
    binary_image1, total_pixels_image1 = convert_to_binary(image_path1, tolerance)
    binary_image2, total_pixels_image2 = convert_to_binary(image_path2, tolerance)

    # Calculate the number of black pixels in each image
    black_pixels_image1 = np.sum(binary_image1 == 1)
    black_pixels_image2 = np.sum(binary_image2 == 1)

    # Convert binary images to signed integers before subtraction to avoid unsigned integer wraparound
    binary_image1_int = binary_image1.astype(np.int16)
    binary_image2_int = binary_image2.astype(np.int16)

    # Step 2: Subtract the two binary matrices element-wise
    difference_matrix = binary_image1_int - binary_image2_int

    # Step 3: Take the absolute value of the differences
    absolute_difference = np.abs(difference_matrix)

    # Step 4: Sum all the values in the absolute difference matrix
    total_difference = np.sum(absolute_difference)

    # New code to output the number of differing pixels
    num_differing_pixels = total_difference  # Same as total_difference
    print(f"Number of differing pixels: {num_differing_pixels}")

    # Generate the difference image
    # Convert absolute_difference to uint8
    absolute_difference_uint8 = absolute_difference.astype(np.uint8)
    # Multiply by 255 to scale differences to full intensity
    diff_array = absolute_difference_uint8 * 255
    # Create the difference image in 'L' mode (grayscale)
    diff_image = Image.fromarray(diff_array, mode='L')
    diff_image.save('difference_image.png')
    print("Difference image saved as 'difference_image.png'.")

    # Print the results
    print(f"Total number of pixels in Image 1: {total_pixels_image1}")
    print(f"Number of black pixels in Image 1: {black_pixels_image1}")
    print(f"Total number of pixels in Image 2: {total_pixels_image2}")
    print(f"Number of black pixels in Image 2: {black_pixels_image2}")
    print(f"Total difference in black pixels: {total_difference}")

    # Step 5: Determine similarity
    if total_difference == 0:
        print("The images are identical in the spatial distribution of black pixels.")
    else:
        print("The images are different in the spatial distribution of black pixels.")

# Example file paths (replace with your actual image file paths)
# You can adjust the tolerance value here
tolerance_value = 0  # Try changing this to 10, 20, etc.

#image_path1 = '57_Win32.InstallCore.AFR potentially unwanted application  512x512.jpg'
#image_path2 = '120_Win32.TrojanDropper.Delf.AF trojan  512x512.jpg'
#image_path1 = '68_Win32.TrojanDownloader.Wauchos.AD trojan  512x512.jpg'
#image_path2 = '6_Win32.TrojanDownloader.Wauchos.AD trojan  512x512.jpg'
#image_path1 = '94_Win32.Kryptik.GEAD trojan  512x512.jpg'
#image_path2 = '96_Win32.Kryptik.GEAD trojan  512x512.jpg'
image_path1 = '12_Win32.TrojanDownloader.Wauchos.AD trojan  512x512.jpg'
image_path2 = '56_Win32.TrojanDownloader.Wauchos.AF trojan  512x512.jpg'
# Compare the images with the specified tolerance
compare_images(image_path1, image_path2, tolerance=tolerance_value)
