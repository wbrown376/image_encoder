import sys
import cv2
import numpy as np
import unittest

sys.path.append('.')
from image_encoder import bmp_decoder

class TestStringMethods(unittest.TestCase):

    def test_bmp_decoder(self):
        # 使用bmp_decoder模块中的bmp_decoder函数读取bmp图像('data/lena.bmp')
        image_data = open("data/lena.bmp", "rb").read()
        width, height, pixels = bmp_decoder.decode(image_data)

        # 使用opencv库读取bmp图像
        cv_image = cv2.imread("data/lena.bmp")

        # 比较图像的宽度和高度
        cv_height, cv_width, _ = cv_image.shape
        self.assertEqual(width, cv_width)
        self.assertEqual(height, cv_height)
        self.assertEqual(pixels.size, cv_image.size)

        # 比较图像数据是否相同(两张图像求差后累积误差再对面积归一化)
        mean_error = np.sum(
            np.abs(pixels.reshape(-1).astype(np.float32) - cv_image.reshape(-1).astype(np.float32)        
                   )
                   )/pixels.size
        self.assertLessEqual(mean_error, 0.05)



if __name__ == '__main__':
    unittest.main()

