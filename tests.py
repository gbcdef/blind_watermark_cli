from unittest import TestCase

from main import *
from blind_watermark import WaterMark
import os


class TestCli(TestCase):
    def setUp(self) -> None:
        self.image = 'fixture/abc.png'
        self.text = 'hello world'
        self.output = 'fixture/abc_embed_output.png'
        self.marker = Marker(123,321)

    def test_main(self):
        marker = self.marker
        marker.add_text_mark_write(self.image, self.text, self.output)
        os.path.isfile(self.output)
        extracted_text = marker.extract_text_mark(self.output, self.text)
        self.assertEqual(self.text, extracted_text)
        os.remove(self.output)

    def test_add_text_watermark_with_cipher(self):
        marker = self.marker
        marker._read_data(self.image, self.text)
        a, b, c = marker._get_encryption_code()
        self.assertEqual(a, 123)
        self.assertEqual(b, 321)
        wm = WaterMark()
        wm.read_img(self.image)
        wm.read_wm(self.text, mode='str')
        bit_length = len(wm.wm_bit)
        self.assertEqual(c, bit_length)

    def test_write_to_with_passcode(self):
        marker = self.marker
        marker._read_data(self.image, self.text)
        a, b, c = marker._get_encryption_code()
        path = marker.add_text_mark_write(self.image, self.text, self.output, True)

        self.assertTrue(
            os.path.exists('fixture/abc_embed_output_pwm123_pimg321.png'),
            "File does not exists"
        )

        os.remove(path)



