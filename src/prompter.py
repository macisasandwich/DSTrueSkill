import json
from cmd import Cmd

import trueskill

import glb
from Player import Player 

class DSTSPrompt(Cmd):
    prompt = 'DSTrueSKill> '
    intro = "Welcome! Type ? to list commands"
    TSEnv = None
    players = []

    def do_test(self, arg):
        print(arg)

    def do_add(self, arg):
        # adds player through CSV provided as part of arg
        glb.print_debug("Got arg {0}".format(arg))

        # vals[0] should = name, vals[1] = mu, vals[2] = sigma
        # vals[0] should always be present, the other 2 are optional
        vals = [val.strip() for val in arg.split(',')]
        
        rating = TSEnv.create_rating(vals[1] if len(vals) >= 2 else None, vals[2] if len(vals) >= 3 else None)

        self.players.append(Player(vals[0], rating))

    def do_list(self, arg):
        # lists existing players in the environment
        glb.print_debug("List called")
        
        for player in self.players:
            print(player)

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
        with open(glb.dataFile, 'r') as f:
            try:
                data = json.load(f)
            except:
                print("Cannot load {0}. Exiting.".format(glb.dataFile))
                exit(1)

            # for now just assume the json file won't be malformatted. famous last words
            self.TSEnv = trueskill.TrueSkill(mu=data['env']['mu'],
                                             sigma=data['env']['sigma'],
                                             beta=data['env']['beta'],
                                             tau=data['env']['tau'],
                                             draw_probability=data['env']['draw'])

            for player in data['players']:
                self.do_add("{0}, {1}, {2}".format(player['name'], player['mu'], player['sigma']))
