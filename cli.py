from sys import argv

from lib import kodxauto

if __name__ == '__main__':
    arg_len = len(argv)
    if (arg_len==2):   
        kodxauto.start(argv[1])
    else:
        print("""Usage:
        argv[1]: name of the saved macros folder
        """)
    