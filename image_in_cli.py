import numpy
from PIL import Image
from colorama import Style, Back, Fore, init as colorama_init
from timeit import default_timer as timer
import sys
from shutil import get_terminal_size

class ImageInCli:
    image_path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 1 else get_terminal_size()[0]

    def __init__(self):
        colorama_init()
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
            [[0, 0, 0], Style.DIM +             Fore.BLACK + '█' + Style.RESET_ALL],
            [[0, 0, 128], Style.DIM +           Fore.BLUE + '█' + Style.RESET_ALL],
            [[0, 128, 0], Style.DIM +           Fore.GREEN + '█' + Style.RESET_ALL],
            [[0, 128, 128], Style.DIM +         Fore.CYAN + '█' + Style.RESET_ALL],
            [[128, 0, 0], Style.DIM +           Fore.RED + '█' + Style.RESET_ALL],
            [[128, 0, 128], Style.DIM +         Fore.MAGENTA + '█' + Style.RESET_ALL],
            [[128, 128, 0], Style.DIM +         Fore.YELLOW + '█' + Style.RESET_ALL],
            [[192, 192, 192], Style.DIM +       Fore.WHITE + '█' + Style.RESET_ALL],
            [[128, 128, 128], Style.BRIGHT +    Fore.BLACK + '█' + Style.RESET_ALL],
            [[0, 0, 255], Style.BRIGHT +        Fore.BLUE + '█' + Style.RESET_ALL],
            [[0, 255, 0], Style.BRIGHT +        Fore.GREEN + '█' + Style.RESET_ALL],
            [[0, 255, 255], Style.BRIGHT +      Fore.CYAN + '█' + Style.RESET_ALL],
            [[255, 0, 0], Style.BRIGHT +        Fore.RED + '█' + Style.RESET_ALL],
            [[255, 0, 255], Style.BRIGHT +      Fore.MAGENTA + '█' + Style.RESET_ALL],
            [[255, 255, 0], Style.BRIGHT +      Fore.YELLOW + '█' + Style.RESET_ALL],
            [[255, 255, 255], Style.BRIGHT +    Fore.WHITE + '█' + Style.RESET_ALL],
            [[174, 142, 142], Style.DIM + Back.WHITE + Fore.RED + '▒' + Back.BLACK + Style.RESET_ALL],
            [[219, 140, 145], Style.DIM + Back.LIGHTWHITE_EX + Fore.RED + '▒' + Back.BLACK + Style.RESET_ALL],
            [[128, 100,   0], Style.DIM + Back.YELLOW + Fore.RED + '▒' + Back.BLACK + Style.RESET_ALL],
            [[ 80,  56,   0], Style.DIM + Back.GREEN  + Fore.RED + '▓' + Back.BLACK + Style.RESET_ALL],
            [[ 34,  33,  37], Style.DIM + Back.BLACK  + Style.BRIGHT + Fore.BLACK + '▒' + Back.BLACK + Style.RESET_ALL],
            [[ 85,  84,  79], Style.DIM + Back.BLACK  + Style.BRIGHT + Fore.BLACK + '▓' + Back.BLACK + Style.RESET_ALL],
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
        for row in self.matrix:
            line = ''
            for pixel in row:
                rgb_str = str(pixel[0]) + ',' + str(pixel[1]) + ',' + str(pixel[2])
                color_code = self.color_codes[self.nearest_color_indexes[rgb_str]][1]

                line += color_code
            whole_string += line + '\n'
        print(whole_string)
        print(Style.RESET_ALL)


start = timer()
cli_image = ImageInCli()
end = timer()
print('Time: {0}s'.format(end - start))

start = timer()
cli_image.draw_image()
end = timer()
print('Time: {0}s'.format(end - start))
