import numpy as np

def encode(bmp_data):
    height, width = bmp_data.shape[:2]
    
    # 计算每行的字节数（包括 padding）
    bytes_per_row = width * 3
    if bytes_per_row % 4 != 0:
        padding = 4 - (bytes_per_row % 4)
    else:
        padding = 0
    
    # bmp 文件头
    bfType = 'BM'.encode()
    bfSize = (14 + 40 + bytes_per_row * height + padding * height).to_bytes(4, byteorder='little')
    bfReserved1 = b'\x00\x00'
    bfReserved2 = b'\x00\x00'
    bfOffBits = 14 + 40
    
    # DIB 位图信息头
    biSize = int(40).to_bytes(4, byteorder='little')
    biWidth = width.to_bytes(4, byteorder='little')
    biHeight = height.to_bytes(4, byteorder='little')
    biPlanes = b'\x01\x00'
    biBitCount = int(24).to_bytes(2, byteorder='little')
    biCompression = b'\x00\x00\x00\x00'  # BI_RGB，不压缩
    biSizeImage = (bytes_per_row * height + padding * height).to_bytes(4, byteorder='little')
    biXPelsPerMeter = int(0).to_bytes(4, byteorder='little')
    biYPelsPerMeter = int(0).to_bytes(4, byteorder='little')
    biClrUsed = b'\x00\x00\x00\x00'
    biClrImportant = b'\x00\x00\x00\x00'
    
    # 组合文件头和信息头
    header = (bfType + bfSize + bfReserved1 + bfReserved2 + bfOffBits.to_bytes(4, byteorder='little'))
    info_header = biSize + biWidth + biHeight + biPlanes + biBitCount + biCompression + biSizeImage + biXPelsPerMeter + biYPelsPerMeter + biClrUsed + biClrImportant
    
    # 逆序排列图像数据
    flipped_data = np.flipud(bmp_data)
    
    # 添加 padding 到每行末尾
    padded_data = flipped_data.tobytes()
    for i in range(height):
        row_start = i * bytes_per_row
        if padding > 0:
            padded_data += b'\x00' * padding
    
    # 将所有部分组合在一起
    bmp_bytes = header + info_header + padded_data
    
    return np.frombuffer(bmp_bytes, dtype=np.uint8)