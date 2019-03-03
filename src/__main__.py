from argparse import ArgumentParser

from prompter import DSTSPrompt

import glb

def main():
    parser = ArgumentParser()

    parser.add_argument("--debug", action='store_true', 
                        help='Enables debug output')

    parser.add_argument("-f", "--file", type=str, required=False,
    					default='dsts.json',
    					help="Data file to load (Default: dsts.json in the same folder as DSTS binary)")

    args = parser.parse_args()

    glb.debug = args.debug
    glb.dataFile = args.file
    glb.print_debug("args: {0}".format(args))

    DSTSPrompt().cmdloop()

if __name__ == '__main__':
    main()
