from cmd import Cmd

class DSTSPrompt(Cmd):
    prompt = 'DSTrueSKill> '
    intro = "Welcome! Type ? to list commands"

    def do_add(self, arg):
        # adds player
        pass

    def do_list(self, arg):
        # lists existing players in the environment
        pass 

    def do_match(self, arg):
        # iteration 1: requires winner and loser predecided and enter in order
        # just updates MMR 
        pass

    def do_exit(self, arg):
        # writes out environment and exit

        return True

    def help_add(self):
        pass 

    def help_list(self):
        pass 

    def help_match(self):
        pass

    def help_exit(self):
        pass

    def default(self, arg):
        if arg == 'q':
            return self.do_exit(arg)

        print("Got '{0}'. Invalid input or not implemented.".format(arg))

    def __init__(self):
        super(DSTSPrompt, self).__init__()

        # create/load environment here
