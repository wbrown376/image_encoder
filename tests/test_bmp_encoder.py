import sys
import cv2
import numpy as np
import unittest

sys.path.append('.')
from image_encoder import bmp_encoder

class TestStringMethods(unittest.TestCase):

    def test_bmp_decoder(self):
        # 使用opencv库读取bmp图像
        cv_image = cv2.imread("data/lena.bmp")

        # 使用bmp_encoder模块中的encode函数将图像编码为BMP格式
        bmp_np_1 = bmp_encoder.encode(cv_image)

        # 使用numpy读取bmp的原始字节
        decoded_image = cv2.imdecode(bmp_np_1, cv2.IMREAD_UNCHANGED)

        # 比较解码后的图像和原始图像是否相同
        self.assertTrue(np.array_equal(decoded_image, cv_image), "Arrays are not equal")




if __name__ == '__main__':
    unittest.main()

