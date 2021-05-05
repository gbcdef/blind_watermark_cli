from unittest import TestCase

from main import *
from blind_watermark import WaterMark
import os


class TestCli(TestCase):
    def setUp(self) -> None:
        self.image = 'fixture/abc.png'
        self.text = 'hello world'
        self.output = 'fixture/abc_embed_output.png'

    def test_main(self):
        marker = Marker(231, 432)
        marker.add_text_mark(self.image, self.text, self.output)
        extracted_text = marker.extract_text_mark(self.output, self.text)
        self.assertEqual(self.text, extracted_text)
        os.remove(self.output)

    def test_add_text_watermark_with_cipher(self):
        marker = Marker(123, 423)
        marker.read_data(self.image, self.text)
        a, b, c = marker.get_encryption_code(self.image, self.text)
        self.assertEqual(a, 123)
        self.assertEqual(b, 423)
        wm = WaterMark()
        wm.read_img(self.image)
        wm.read_wm(self.text, mode='str')
        bit_length = len(wm.wm_bit)
        self.assertEqual(c, bit_length)

    def test_random_marker(self):
        marker = MarkerRandom()

