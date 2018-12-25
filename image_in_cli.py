import numpy
from PIL import Image
from colorama import Style, Back, Fore, init as colorama_init
from timeit import default_timer as timer
import sys
from shutil import get_terminal_size


class ImageInCli:
    image_path = None
    width = None

    def __init__(self, **kwargs):
        colorama_init()
        self.image_path = kwargs['image_path']
        self.width = get_terminal_size()[0] if kwargs['width'] == None else kwargs['width'] 
        self.matrix = None
        self.color_codes = None
        self.nearest_color_indexes = None

        self.init_color_codes()
        self.get_rgb_matrix(1.5)
        self.get_nearest_color_indexes()
        pass

    def get_rgb_matrix(self, char_ratio):
        img = Image.open(self.image_path)
        basewidth = self.width
        anti_char_ratio_width = int(basewidth * char_ratio)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((anti_char_ratio_width, hsize), Image.ANTIALIAS)
        self.matrix = numpy.asarray(img)

    def init_color_codes(self):
        rgb_color_codes = [
            [[0, 0, 0], Style.DIM + Fore.BLACK, '█'],
            [[0, 0, 128], Style.DIM + Fore.BLUE, '█'],
            [[0, 128, 0], Style.DIM + Fore.GREEN, '█'],
            [[0, 128, 128], Style.DIM + Fore.CYAN, '█'],
            [[128, 0, 0], Style.DIM + Fore.RED, '█'],
            [[128, 0, 128], Style.DIM + Fore.MAGENTA, '█'],
            [[128, 128, 0], Style.DIM + Fore.YELLOW, '█'],
            [[192, 192, 192], Style.DIM + Fore.WHITE, '█'],
            [[128, 128, 128], Style.BRIGHT + Fore.BLACK, '█'],
            [[0, 0, 255], Style.BRIGHT + Fore.BLUE, '█'],
            [[0, 255, 0], Style.BRIGHT + Fore.GREEN, '█'],
            [[0, 255, 255], Style.BRIGHT + Fore.CYAN, '█'],
            [[255, 0, 0], Style.BRIGHT + Fore.RED, '█'],
            [[255, 0, 255], Style.BRIGHT + Fore.MAGENTA, '█'],
            [[255, 255, 0], Style.BRIGHT + Fore.YELLOW, '█'],
            [[255, 255, 255], Style.BRIGHT + Fore.WHITE, '█'],
            [[174, 142, 142], Style.DIM + Back.WHITE + Fore.RED, '▒'],
            [[219, 140, 145], Style.DIM + Back.LIGHTWHITE_EX + Fore.RED, '▒'],
            [[128, 100, 0], Style.DIM + Back.YELLOW + Fore.RED, '▒'],
            [[80, 56, 0], Style.DIM + Back.GREEN + Fore.RED, '▓'],
            [[34, 33, 37], Back.BLACK + Style.BRIGHT + Fore.BLACK, '▒'],
            [[85, 84, 79], Back.BLACK + Style.BRIGHT + Fore.BLACK, '▓'],
        ]

        self.color_codes = rgb_color_codes

    def get_nearest_color_index(self, rgb):
        avg_diffs = []

        for i, color in enumerate(self.color_codes):
            red_diff = abs(color[0][0] - rgb[0])
            green_diff = abs(color[0][1] - rgb[1])
            blue_diff = abs(color[0][2] - rgb[2])
            avg_diff = (red_diff + green_diff + blue_diff) / 3

            avg_diffs.append([avg_diff, i])

        nearest_index = min(avg_diffs, key=lambda x: x[0])[1]

        return nearest_index

    def get_nearest_color_indexes(self):
        nearest_color_indexes = {}
        for row in self.matrix:
            for pixel in row:
                rgb_str = str(pixel[0]) + ',' + str(pixel[1]) + ',' + str(pixel[2])
                if not (rgb_str in nearest_color_indexes):
                    nearest_color_index = self.get_nearest_color_index(pixel)
                    nearest_color_indexes[rgb_str] = nearest_color_index

        self.nearest_color_indexes = nearest_color_indexes

    def draw_image(self):
        print(Back.BLACK)
        whole_string = ''
        prev_color_code = None
        for row in self.matrix:
            line = ''
            for pixel in row:
                rgb_str = str(pixel[0]) + ',' + str(pixel[1]) + ',' + str(pixel[2])
                color = self.color_codes[self.nearest_color_indexes[rgb_str]]
                color_code = ''
                if not (color[1] == prev_color_code):
                    color_code += Style.RESET_ALL + color[1]
                    prev_color_code = color[1]
                color_code += color[2]

                line += color_code
            whole_string += line + '\n'
        print(whole_string)
        print(Style.RESET_ALL)


if __name__ == '__main__':
    def print_help():
        print('''
Command Line Usage
python -m $MODULE_NAME$ [help] [img=img_path] [width=width?]
''')
    
    if len(sys.argv) == 1 or sys.argv[1]=='help' or sys.argv[1] == '/?':
         print_help()
         exit(0)
    else:
        print(sys.argv)
        opts = dict(list(map(lambda field:field.split('='), sys.argv[1:])))
        print(opts)
        if not ('img' in opts):
            print('Error: Specify image path by img argument')
            print_help()
            exit(1)
            
        cli_img = ImageInCli(image_path=opts['img'], width=int(opts['width']) if 'width' in opts else None)    
        cli_img.draw_image()
    