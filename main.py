from blind_watermark import WaterMark
import os
import argparse
import logging
import random

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger(__name__)


class Marker:
    def __init__(self, password_wm, password_img):
        self._password_wm = password_wm
        self._password_img = password_img
        self.bwm = WaterMark(password_wm=password_wm, password_img=password_img)
        self._bit_length = 0
        self._path_to_image = ''

    def add_text_mark_write(self, path_to_image, wm_text, path_to_output, is_with_passcode=False):
        lg.info(f'Working directory: {os.getcwd()}')
        lg.info(f'Parameters: {path_to_image}, {wm_text}, {path_to_output}')
        self._path_to_image = path_to_image

        self._read_data(path_to_image, wm_text)
        if is_with_passcode:
            path = self._write_to_with_passcode(path_to_output)
        else:
            path = self._write_to(path_to_output)
        lg.info(f'File saved to: {os.path.abspath(path_to_output)}')
        lg.info(f'Watermark is: {wm_text}')
        return path

    def _write_to(self, path_to_output):
        self.bwm.embed(path_to_output)
        return path_to_output

    def _write_to_with_passcode(self, path_to_output):
        basename = os.path.basename(path_to_output)
        dirname = os.path.dirname(path_to_output)
        filename, suffix = os.path.splitext(basename)
        lg.info(f'Suffix: {suffix}')
        path_to_output_with_passcode = f'{os.path.join(dirname, filename)}' \
                                       f'_{self._password_wm}' \
                                       f'_{self._password_img}' \
                                       f'_{self._bit_length}' \
                                       f'{suffix}'
        lg.info(f'Output: {path_to_output_with_passcode}')
        lg.info(f'Don\'t forget your password pair for this image: {self._password_wm}, {self._password_img}')
        return self._write_to(path_to_output_with_passcode)

    @staticmethod
    def extract_text_mark(path_to_image, password=None):
        import re
        lg.info(password)
        if password:
            _tmp = password
        else:
            _tmp = path_to_image
        match = re.match(r'.*_(\d+)_(\d+)_(\d+)\.\D{3,4}', _tmp)
        lg.info(match)
        if not match:
            raise Exception
        # a, b, length = (int(x) for x in password.split('_'))
        a, b, length = (int(x) for x in match.groups())

        lg.info(f'{a}, {b}, {length}')

        wm = WaterMark(a, b)

        result = wm.extract(path_to_image, length, mode='str')
        lg.info(f'Extracted text watermark: {result}')
        return result

    def _read_data(self, path_to_image, wm_text):
        if not os.path.isfile(path_to_image):
            raise FileNotFoundError
        self.bwm.read_img(path_to_image)
        self.bwm.read_wm(wm_text, mode='str')
        self._bit_length = len(self.bwm.wm_bit)

    def _get_encryption_code(self):
        if self._bit_length == 0:
            raise NotImplementedError
        return self._password_wm, self._password_img, self._bit_length


class MarkerRandom(Marker):
    def __init__(self):
        self._password_wm = random.randint(100000, 999999)
        self._password_img = random.randint(100000, 999999)
        super().__init__(self._password_wm, self._password_img)


def main():
    # lg.setLevel(logging.WARN)

    parser = argparse.ArgumentParser(description='Add blind watermark to images')
    parser.add_argument('command', type=str)
    parser.add_argument('image', type=str)
    parser.add_argument('-t', type=str, default='Watermark', help='Text watermark')
    parser.add_argument('-w', type=bool, default=True)
    parser.add_argument('-o', type=str, default='embed.png')
    parser.add_argument('-p', default=None)
    # parser.add_argument('-v', type=bool, default=False)
    args = parser.parse_args()

    # if args.v:
    #     lg.setLevel(logging.INFO)

    if args.command == 'encode':
        marker = MarkerRandom()
        marker.add_text_mark_write(args.image, args.t, args.o, args.w)
    elif args.command == 'encodedir':
        if not os.path.isdir(args.image):
            raise NotADirectoryError

        import shutil
        for file in os.listdir(args.image):
            marker = MarkerRandom()
            fullpath = os.path.join(args.image, file)
            writepath: str = os.path.join(args.image, 'watermarked_' + file)
            lg.info(fullpath)
            lg.info(writepath)
            try:
                path = marker.add_text_mark_write(fullpath, args.t, writepath, args.w)
                lg.info(path)
                shutil.copy2(path, writepath)
            except:
                lg.warning(f'Add watermark failed: {fullpath}')

    elif args.command == 'decode':
        text = Marker.extract_text_mark(args.image, args.p)
        print(f'Text watermark is: {text}')


if __name__ == '__main__':
    main()
