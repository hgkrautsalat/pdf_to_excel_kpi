from PIL import Image

threshold = 220

def convert_jpg_to_eps(input_path, output_path):
    """
    Convert a JPEG file to EPS format with transparent background.

    Args:
        input_path: Path to the input JPEG file
        output_path: Path to the output EPS file
    """
    try:
        # Open the JPEG image
        img = Image.open(input_path)

        # Convert to RGBA for transparency support
        img = img.convert('RGBA')

        # Get image data
        datas = img.getdata()

        # Create new data list with transparent white pixels
        new_data = []
        for item in datas:
            # Change white (or near-white) pixels to transparent
            # Adjust threshold (220) if needed for different shades
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                new_data.append((255, 255, 255, 0))  # Transparent
            else:
                new_data.append(item)

        # Update image data
        img.putdata(new_data)

        # Save as EPS
        img.save(output_path, 'EPS')
        print(f"Successfully converted {input_path} to {output_path}")

    except Exception as e:
        print(f"Error converting image: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "input.jpg"
    input_file=r"C:\Users\Susann\Desktop\NicoNaco.jpg"
    output_file = "output.eps"
    convert_jpg_to_eps(input_file, output_file)
