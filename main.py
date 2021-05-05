from blind_watermark import WaterMark
import os
import argparse
import logging
import random

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger(__name__)


class Marker:
    def __init__(self, password_wm, password_img):
        self.password_wm = password_wm
        self.password_img = password_img
        self.bwm = WaterMark(password_wm=password_wm, password_img=password_img)
        self.bit_length = 0

    def add_text_mark(self, path_to_image, wm_text, path_to_output):
        bwm = self.bwm
        lg.info(f'Working directory: {os.getcwd()}')
        lg.info(f'Parameters: {path_to_image}, {wm_text}, {path_to_output}')


        if os.path.isfile(path_to_image):
            bwm.read_img(path_to_image)
            bwm.read_wm(wm_text, mode='str')
            bwm.embed(path_to_output)
            lg.info(f'File saved to: {os.path.abspath(path_to_output)}')
        else:
            raise FileNotFoundError

    def extract_text_mark(self, path_to_image, wm_text):
        bwm = self.bwm
        bwm.read_wm(wm_text, mode='str')
        length = len(bwm.wm_bit)
        result = bwm.extract(path_to_image, length, mode='str')
        lg.info(f'Extracted text watermark: {result}')
        return result

    def read_data(self, path_to_image, wm_text):
        if not os.path.isfile(path_to_image):
            raise FileNotFoundError
        self.bwm.read_img(path_to_image)
        self.bwm.read_wm(wm_text, mode='str')
        self.bit_length = len(self.bwm.wm_bit)

    def get_encryption_code(self, path_to_image, wm_text):
        self.read_data(path_to_image, wm_text)
        return self.password_wm, self.password_img, self.bit_length


class MarkerRandom(Marker):
    def __init__(self):
        self.password_wm = random.randint(100000, 999999)
        self.password_img = random.randint(100000, 999999)
        super().__init__(self.password_wm, self.password_img)

    def add_text_mark(self, path_to_image, wm_text, path_to_output):
        suffix = path_to_image.split('.')[-1]
        lg.info(f'Suffix: {suffix}')
        output = ''.join((path_to_output,
                          '_pwm', str(self.password_wm),
                          '_pimg', str(self.password_img),
                          '.', suffix))
        lg.info(f'Output: {output}')
        super().add_text_mark(path_to_image, wm_text, output)
        lg.info(f'Don\'t forget your password pair for this image: {self.password_wm}, {self.password_img}')


def main():
    # lg.setLevel(logging.WARN)

    parser = argparse.ArgumentParser(description='Add blind watermark to images')
    parser.add_argument('image', type=str)
    parser.add_argument('-t', type=str, help='Text watermark')
    parser.add_argument('-o', type=str, default='embed')
    args = parser.parse_args()

    marker = MarkerRandom()
    marker.add_text_mark(args.image, args.t, args.o)


if __name__ == '__main__':
    main()
