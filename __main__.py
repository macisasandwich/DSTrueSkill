from argparse import ArgumentParser

from prompter import DSTSPrompt

import glb

def main():
    parser = ArgumentParser()

    parser.add_argument("debug", action='store_true', 
                        help='Enables debug output')

    args = parser.parse_args()

    glb.debug = args.debug
    glb.print_debug("args: {0}".format(args))

    DSTSPrompt().cmdloop()

if __name__ == '__main__':
    main()
