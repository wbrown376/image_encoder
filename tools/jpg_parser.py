import struct
import argparse
import io

def read_marker_and_length(file: io.BufferedReader):
    marker = file.read(2)
    if marker[0] != 0xFF:
        print(f'marker: {marker}')
        raise ValueError("Not a valid JPEG file")
    if marker[1] == 0xD9:  # EOI marker
        file.seek(-2, 1)
        return marker, None
    length = struct.unpack('>H', file.read(2))[0]
    file.seek(-4, 1)
    return marker, length

def parse_jfif_app0(segment: bytes) -> dict:
    """
    解析 APP0 段并返回结果

    Args:
    segment (bytes): APP0 段的字节数据

    Returns:
    dict: 解析结果（标记、长度、标识符、版本、密度单位、X 密度、Y 密度）
    """
    reader = io.BytesIO(segment)

    marker = hex(struct.unpack('>H', reader.read(2))[0]).upper()
    length = struct.unpack('>H', reader.read(2))[0]
    jfif_identifier = struct.unpack('5s', reader.read(5))[0]
    version = '{}.{}'.format(*struct.unpack('>BB', reader.read(2)))
    density_units = struct.unpack('>B', reader.read(1))[0]
    x_density, y_density = struct.unpack('>HH', reader.read(4))
    x_thumbnail, y_thumbnail = struct.unpack('>BB', reader.read(4))

    return {
        'marker': marker, 
        'length': length,
        'jfif_identifier': jfif_identifier,
        'version': version,
        'density_units': density_units,
        'x_density': x_density,
        'y_density': y_density,
        'x_thumbnail': x_thumbnail,
        'y_thumbnail': y_thumbnail,
    }

def parse_quantization_tables(segment: bytes) -> dict:
    """
    Parse the Quantization Tables segment of a JPEG file.
    Args:
        segment (bytes): The JPEG file segment containing the Quantization Tables.
    Returns:
        dict: A dictionary containing information about the Quantization Tables.

    """
    reader = io.BytesIO(segment)

    marker = hex(struct.unpack('>H', reader.read(2))[0]).upper()
    length = struct.unpack('>H', reader.read(2))[0]

    qt_info = struct.unpack('B', reader.read(1))[0]
    defestination_id = { 0: 'Luminance',
                        1: 'Chrominance'}.get(qt_info & 7)
    precision = {0: '8-bit',
                  1: '16-bit'}.get(qt_info >> 4)
                 
    table = struct.unpack('B'*64, reader.read(64))

    return {
        'marker': marker, 
        'length': length,
        'qt_info': qt_info,
        'defestination_id': defestination_id,
        'precision': precision,
        'table': table
    }

def parse_sof0_segment(segment: bytes) -> dict:
    """
    Parses the SOF0 segment of a JPEG image.

| Field                | Size (bytes) | Description                                                  |
|----------------------|--------------|--------------------------------------------------------------|
| Marker Identifier    | 2            | 0xff, 0xc0 to identify SOF0 marker                          |
| Length               | 2            | This value equals to 8 + components*3                      |
| Data precision       | 1            | This is in bits/sample, usually 8 (12 and 16 not supported by most software). |
| Image height         | 2            | This must be > 0                                           |
| Image Width          | 2            | This must be > 0                                           |
| Number of components | 1            | Usually 1 = grey scaled, 3 = color YcbCr or YIQ              |
| Each component       | 3            | Contains, (component Id(1byte)(1 = Y, 2 = Cb, 3 = Cr, 4 = I, 5 = Q), sampling factors (1byte) (bit 0-3 vertical., 4-7 horizontal.), quantization table number (1 byte)). |
    """
    reader = io.BytesIO(segment)

    marker = hex(struct.unpack('>H', reader.read(2))[0]).upper()
    length = struct.unpack('>H', reader.read(2))[0]

    data_precision = struct.unpack('>B', reader.read(1))[0]
    image_height = struct.unpack('>H', reader.read(2))[0]
    image_width = struct.unpack('>H', reader.read(2))[0]
    number_of_components = struct.unpack('>B', reader.read(1))[0]

    components = []
    for _ in range(number_of_components):
        component_id = struct.unpack('>B', reader.read(1))[0]
        sampling_factors = struct.unpack('>B', reader.read(1))[0]
        quantization_table_number = struct.unpack('>B', reader.read(1))[0]
        components.append({
            'component_id': component_id,
            'sampling_factors': sampling_factors,
            'quantization_table_number': quantization_table_number
        })

    return {
        'marker': marker,
        'length': length,
        'data_precision': data_precision,
        'image_height': image_height,
        'image_width': image_width,
        'number_of_components': number_of_components,
        'components': components
    }

def parse_huffman_tables(segment: bytes) -> dict:
    """
    Parses Huffman tables from a JPEG

| Field             | Size (bytes) | Description                                                                 |
|-------------------|--------------|-----------------------------------------------------------------------------|
| Marker Identifier | 2            | 0xff, 0xc4 to identify DHT marker                                         |
| Length            | 2            | This specifies the length of Huffman table                                   |
| HT information     | 1            | bit 0..3: number of HT (0..3, otherwise error) bit 4: type of HT, 0 = DC table, 1 = AC table bit 5..7: not used, must be 0 |
| Number of Symbols | 16           | Number of symbols with codes of length 1..16, the sum(n) of these bytes is the total number of codes, which must be <= 256 |
| Symbols           | n            | Table containing the symbols in order of increasing code length (n = total number of codes) |
    """
    reader = io.BytesIO(segment)

    marker = hex(struct.unpack('>H', reader.read(2))[0]).upper()
    length = struct.unpack('>H', reader.read(2))[0]

    ht_info = struct.unpack('>B', reader.read(1))[0]
    table_class = (ht_info >> 4) & 0x01  # 0 for DC, 1 for AC
    table_id = ht_info & 0x0F  # Table ID (0-3)

    number_of_symbols = struct.unpack('>'+'B'*16, reader.read(16))
    total_symbols = sum(number_of_symbols)

    symbols = struct.unpack('>'+'B'*total_symbols, reader.read(total_symbols))
    return {
        'marker': marker,
        'length': length,
        'table_class': table_class,
        'table_id': table_id,
        'number_of_symbols': number_of_symbols,
        'total_symbols': total_symbols,  
        'symbols': symbols
    }


def parse_jpeg_file(file_path):
    # JPEG文件格式 SOI-->Appn-->DQT-->SOF0-->DHT-->SOS-->EOI
    # 1. SOI (Start Of Image): ff d8
    # 2. APP0 (Application Specific): ff e0
    # 3. DQT (Define Quantization Table): ff db
    # 4. SOF0 (Start Of Frame): ff c0
    # 5. DHT (Define Huffman Table): ff c4
    # 6. SOS (Start Of Scan): ff da
    # 8. EOI (End Of Image): ff d9
    with open(file_path, 'rb') as file:
        # 读取文件头，检查SOI(Start Of Image)标记
        magic = file.read(2)
        if magic != b'\xff\xd8':
            raise ValueError("Invalid JPEG file, missing SOI marker")

        while True:
            marker, length = read_marker_and_length(file)
            if marker is None:
                break
            if marker[1] == 0xC0:  # SOF0 marker
                segment = file.read(length+2)
                print (f'SOF0 Marker Found, length {length}')
                sof0_info = parse_sof0_segment(segment)
                print("SOF0 Information:", sof0_info)
            elif marker[1] == 0xD8:  # Start of Image marker
                print (f'Start of Image Marker Found, length {length}')
            elif marker[1] == 0xE0:  # APP0 marker
                segment = file.read(length+2)
                print (f'APP0 Marker Found, length {length}')
                jfif_info = parse_jfif_app0(segment)
                print("JFIF Information:", jfif_info)
            elif marker[1] == 0xDB:  # DQT marker
                segment = file.read(length+2)
                print (f'DQT Marker Found, length {length}')
                dqt_info = parse_quantization_tables(segment)
                print("Quantization Tables:", dqt_info)
            elif marker[1] == 0xC4:  # DHT marker
                segment = file.read(length+2)
                print (f'DHT Marker Found, length {length}')
                huffman_info = parse_huffman_tables(segment)
                print("Huffman Tables:", huffman_info)
            elif marker[1] == 0xDA:  # SOS marker
                segment = file.read(length+2)
                print (f'SOS Marker Found, length {length}')
                file.seek(-2, 2) # 跳转到EOI
            elif marker[1] == 0xD9:  # End of Image marker
                print ('End of Image Marker Found')
                break
            else:
                # Skip other markers
                file.read(length+2)

# Example usage
if __name__ == '__main__':
    # 参数解析
    parser = argparse.ArgumentParser(description='JPEG File Parser')
    parser.add_argument('--file_path', default='.\data\lena.jpg', help='Path to the JPEG file')
    args = parser.parse_args()
    
    # 解析JPEG文件
    parse_jpeg_file(args.file_path)

