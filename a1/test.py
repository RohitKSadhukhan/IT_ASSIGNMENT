# Python program to print
# red text with green background
import colorama
from colorama import Fore, Back, Style
if __name__ == "__main__":
    colorama.init()
    print(Fore.RED + 'some red text')
    print(Back.GREEN + 'and with a green background')
    print(Style.DIM + 'and in dim text')
    print(Style.RESET_ALL)
    print('back to normal now')
