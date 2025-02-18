## BMP 文件头
BMP（Bitmap）文件头是 Windows BMP 图像文件格式的开始部分，用于存储图像的基本信息。以下是 BMP 文件头的结构：

### 文件头（14 bytes）
* `bfType` (2 bytes)：文件类型标识，必须为 `BM`（0x424d）
* `bfSize` (4 bytes)：文件大小（字节），unsigned
* `bfReserved1` (2 bytes)：保留字段
* `bfReserved2` (2 bytes)：保留字段
* `bfOffBits` (4 bytes)：图像数据偏移量（字节），unsigned

### 信息头（40 bytes）
* `biSize` (4 bytes)：信息头大小（字节），unsigned
* `biWidth` (4 bytes)：图像宽度（像素），signed
* `biHeight` (4 bytes)：图像高度（像素），signed
* `biPlanes` (2 bytes)：图像平面数, unsigned
* `biBitCount` (2 bytes)：每像素位数, unsigned
* `biCompression` (4 bytes)：压缩类型, unsigned
* `biSizeImage` (4 bytes)：图像数据大小（字节）, unsigned
* `biXPelsPerMeter` (4 bytes)：水平分辨率（像素/米）, signed
* `biYPelsPerMeter` (4 bytes)：垂直分辨率（像素/米）, signed
* `biClrUsed` (4 bytes)：颜色表中的颜色数, unsigned
* `biClrImportant` (4 bytes)：重要颜色数, unsigned

BMP 文件头的总大小为 54 bytes。信息头中的各个字段用于存储图像的基本信息，包括图像的大小、分辨率、颜色深度等。