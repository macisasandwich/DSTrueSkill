import json
from cmd import Cmd

import trueskill

import glb
from Player import Player 

class DSTSPrompt(Cmd):
    prompt = 'DSTrueSKill> '
    intro = "Welcome! Type ? to list commands"
    TSEnv = None
    players = {}

    def do_add(self, arg):
        # adds player through CSV provided as part of arg
        glb.print_debug("add got arg {0}".format(arg))

        # vals[0] should = name, vals[1] = mu
        # vals[0] should always be present, mu is optional
        vals = [val.strip() for val in arg.split(' ')]

        self.add_player(vals[0], vals[1] if len(vals) >= 2 else None)

        glb.print_debug("add done")

        return

    def do_list(self, arg):
        # lists existing players in the environment
        glb.print_debug("list called")

        leaderboard = sorted(self.players.items(), key=lambda x: self.TSEnv.expose(x[1]), reverse=True)
        
        for name, rating in leaderboard:
            print("{0}\t{1}".format(name, int(rating.mu)))
        
        glb.print_debug("list done")
        return

    def do_match(self, arg):
        # iteration 1: requires winner and loser predecided and enter in order
        # just updates MMR 
        glb.print_debug("match got arg {0}".format(arg))

        names = [val.strip() for val in arg.split(' ')]
        glb.print_debug("match got {0} players".format(len(names))) # should be 6

        # error checking
        if len(names) < 6:
            print("Got less than 6 players. Try entering again")
            return

        for name in names:
            if name not in self.players:
                print("{0} not in players list. Try entering again")
                return

        # first group = 3 winners, second group = 3 losers
        rgroup = [(self.players[names[0]], self.players[names[1]], self.players[names[2]]), 
                  (self.players[names[3]], self.players[names[4]], self.players[names[5]])]

        # update the players list
        rated = self.TSEnv.rate(rgroup)
        self.players[names[0]] = rated[0][0]
        self.players[names[1]] = rated[0][1]
        self.players[names[2]] = rated[0][2]
        self.players[names[3]] = rated[1][0]
        self.players[names[4]] = rated[1][1]
        self.players[names[5]] = rated[1][2]

        glb.print_debug("match done")

        return

    def do_exit(self, arg):
        # writes out environment and exit
        d = {"env": {}, "players": []}

        d["env"]["mu"] = self.TSEnv.mu
        d["env"]["sigma"] = self.TSEnv.sigma
        d["env"]["beta"] = self.TSEnv.beta
        d["env"]["tau"] = self.TSEnv.tau
        d["env"]["draw"] = self.TSEnv.draw_probability

        for name, rating in self.players.items():
            d["players"].append({
                                 "name": name, 
                                 "mu": rating.mu,
                                 "sigma": rating.sigma
                                })

        with open(glb.dataFile, 'w') as f:
            json.dump(d, f, indent=2)

        print("Data written out to {0}".format(glb.dataFile))
        return True

    def help_add(self):
        print("Adds a player into the tournament. Example: add mac <MMR>")
        print("If MMR field is left empty, the player will be created with the default MMR")

        return

    def help_list(self):
        print("Prints out the leaderboard")

        return 

    def help_match(self):
        print("Enter the results of a match to update ratings.")
        print("$> match <winner1> <winner2> <winner3> <loser1> <loser2> <loser3>")

        return

    def help_exit(self):
        print("What do you think?")

        return

    def default(self, arg):
        if arg == 'q':
            return self.do_exit(arg)

        print("Got '{0}'. Invalid input or not implemented.".format(arg))

    def add_player(self, name, mu=None, sigma=None):
        rating = self.TSEnv.create_rating(mu, sigma)

        self.players[name] = rating

    def __init__(self):
        super(DSTSPrompt, self).__init__()

        # create/load environment here
        try:
            with open(glb.dataFile, 'r') as f:
                data = json.load(f)

                # for now just assume the json file won't be malformatted. famous last words
                self.TSEnv = trueskill.TrueSkill(mu=data['env']['mu'],
                                                 sigma=data['env']['sigma'],
                                                 beta=data['env']['beta'],
                                                 tau=data['env']['tau'],
                                                 draw_probability=data['env']['draw'])

                for player in data['players']:
                    self.add_player(player['name'], player['mu'], player['sigma'])
        except:
            print("Cannot load {0}. Creating new environment with no players.".format(glb.dataFile))
            self.TSEnv = trueskill.TrueSkill()
            self.players = {}
                
        glb.print_debug(self.players)
