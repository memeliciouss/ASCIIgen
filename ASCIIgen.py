import cv2
import numpy as np

def ascii_video(input_path, output_path, ascii_resolution=64, char_width=10, char_height=20,
                         invert_ascii=False, colored = False, ascii_char_set="short"):

    # Args:
    #     input_path (str)
    #     output_path (str)
    #     ascii_resolution (int): The number of ASCII characters per dimension (e.g., 64 for 64x64 cells), this determines the 'resolution' of the ASCII art
    #     char_width (int): Pixel width of each ASCII character in the output video frame
    #     char_height (int): Pixel height of each ASCII character in the output video frame
    #     invert_ascii (bool): If True, inverts the mapping (dark pixels become bright characters and vice-versa)
    #     colored (bool): If True, gives average cell color to text, else White text on black background when False
    #     ascii_char_set (str): Specifies the set of ASCII characters to use

    # ASCII characters ordered from darkest to lightest
    ASCII_CHAR_SETS = {
        "short": "@%#*+=-:. ",
        "long": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
        "dot": ". ",
        "hash": "# ",
        # Can directly pass a custom string of ordered chars too
    }

    # Select the ASCII character set
    if ascii_char_set in ASCII_CHAR_SETS:
        current_ascii_chars = ASCII_CHAR_SETS[ascii_char_set]
    else:
        # If string does not map to any set, use it as a custom string of char
        current_ascii_chars = ascii_char_set
        print(f"Using ASCII character set: '{current_ascii_chars}'")
    
    if invert_ascii:
        current_ascii_chars = current_ascii_chars[::-1]


    def get_ascii_char(pixel_intensity):
        # Maps a grayscale pixel intensity (0-255) to an ASCII character.

        # Ensure intensity is within 0-255 range
        pixel_intensity = max(0, min(255, pixel_intensity))


        # Scale the effective intensity to the length of ASCII_CHARS string
        index = int(pixel_intensity / 256 * len(current_ascii_chars))

        # Ensure index is within valid bounds
        index = min(index, len(current_ascii_chars) - 1)
        return current_ascii_chars[index]


    # Open the input video file
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Codec for MP4

    print(f"Input Video: {frame_width}x{frame_height} @ {fps} FPS")

    # Calculate output video frame dimensions
    output_width = ascii_resolution * char_width
    output_height = ascii_resolution * char_height
    
    # Create a VideoWriter object to save the output video
    # Note: The isColor parameter is set to True because we are drawing colored text (black/white) on a colored background (white/black).
    out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height), isColor=True)

    if not out.isOpened():
        print(f"Error: Could not open video writer for {output_path}")
        cap.release()
        return

    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                # No more frames to read
                break
            
            # Black background
            background = (0, 0, 0)
            # Create a blank image to draw ASCII characters onto for the output video
            ascii_video_frame = np.full((output_height, output_width, 3), background, dtype=np.uint8)

            # Frame Source
            # 1. Decide which version of the frame to resize: original color or grayscale.
            if colored:
                # Keep the original color frame
                frame_to_resize = frame 
            else:
                # Grayscale
                frame_to_resize = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 2. Define new resolution & Average pixel brightness
            # Ascii resolution
            downsampled_pixels = cv2.resize(frame_to_resize,
                                            (ascii_resolution, ascii_resolution),
                                            interpolation=cv2.INTER_AREA)

            # 3. Convert to ASCII art according to brightness level
            for r in range(ascii_resolution):
                for c in range(ascii_resolution):
                    # Cell Value
                    cell_value = downsampled_pixels[r, c]

                    # Determine the brightness of this cell for selecting the ASCII character
                    if colored:
                        # Convert the BGR cell_value to grayscale to get its overall brightness
                        pixel_intensity = cv2.cvtColor(np.uint8([[cell_value]]), cv2.COLOR_BGR2GRAY)[0][0]
                    else:
                        # If not using original colors, cell_value is already grayscale brightness
                        pixel_intensity = cell_value

                    # Get the ASCII character based on the cell
                    ascii_char = get_ascii_char(pixel_intensity)

                    # Character Color
                    if colored:
                        # Use original averaged color of the cell
                        char_color = tuple(int(x) for x in cell_value) 
                    else:
                        # Use white color text on black background
                        char_color = (255, 255, 255)

                    # Draw the ASCII character onto the output video frame
                    x = c * char_width
                    y = (r + 1) * char_height

                    cv2.putText(ascii_video_frame,
                                ascii_char,
                                (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                char_height / 20.0,
                                char_color, # Use the determined char drawing color
                                1,
                                cv2.LINE_AA)

            # Write the generated ASCII art frame to the output video
            out.write(ascii_video_frame)
            frame_count += 1
            print(f"Processing frame {frame_count}...", end='\r')

        print(f"\nFinished processing {frame_count} frames.")
        print(f"ASCII art video saved to: {output_path}")

    except Exception as e:
        print(f"\nAn error occurred during video processing: {e}")
    finally:
        # Release resources
        cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":

    input = 'input.mp4'
    output = 'output.mp4'
    resolution = 80

    ascii_video(input, output, resolution, invert_ascii=True, colored=True, ascii_char_set=";:. ")