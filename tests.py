from unittest import TestCase

from main import Marker
import os


class TestCli(TestCase):
    def test_main(self):
        image = 'fixture/abc.png'
        text = 'hello world'
        output = 'fixture/abc_embed_output.png'
        marker = Marker(231, 432)
        marker.add_text_mark(image, text, output)
        extracted_text = marker.extract_text_mark(output, text)
        self.assertEqual(text, extracted_text)
        os.remove(output)
