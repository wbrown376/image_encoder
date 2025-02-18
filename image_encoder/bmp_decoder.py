import struct
import numpy as np

def decode(bmp_data):
    """
    Decodes a BMP image from raw byte data.

    Args:
        bmp_data: Raw byte data of the BMP image.

    Returns:
        A tuple containing:
            - width: Width of the image in pixels.
            - height: Height of the image in pixels.
            - pixels: A numpy array representing the pixel data.
                      Each row represents a scanline, and each element is a tuple of (blue, green, red) values.
        Returns None if the BMP data is invalid or unsupported.
    """

    # BMP Header + DIB Header (54 bytes)
    if len(bmp_data) < 14+40:
        return None

    magic, file_size, reserved1, reserved2, data_offset = struct.unpack("<2sI2HI", bmp_data[:14])

    if magic != b'BM':
        return None

    # DIB Header (at least 40 bytes)
    if len(bmp_data) < data_offset:
        return None

    dib_size = struct.unpack("<I", bmp_data[14:18])[0]

    if dib_size >= 40:
        width, height, planes, bits_per_pixel, compression, image_size = struct.unpack("<iiHHII", bmp_data[18:18+20])

        if planes != 1 or bits_per_pixel != 24 or compression != 0:
            return None

        # Calculate padding
        padding = (4 - (width * 3) % 4) % 4

        # Create a numpy array to hold the pixel data
        pixels = np.zeros((height, width, 3), dtype=np.uint8)

        # Read pixel data from BMP file
        for y in range(height):
            row_start = data_offset + (height - y - 1) * (width * 3 + padding)
            for x in range(width):
                pixel_start = row_start + x * 3
                pixels[y, x] = struct.unpack("BBB", bmp_data[pixel_start:pixel_start+3])

        return width, height, pixels
    else:
        return None