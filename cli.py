from sys import argv
from lib import runner

if __name__ == '__main__':
    arg_len = len(argv)
    if (arg_len==2):   
        runner.run(argv[1])
    else:
        print("""Usage:
        argv[1]: path to the saved macros folder
        """)
    