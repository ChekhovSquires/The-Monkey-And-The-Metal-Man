from Piece import Assasin, Spotter

class Player:

    def __init__(self, ID, spotter_location, assasin_location,
            spotter_direction, assasin_direction, agent_class):

        self.ID = ID
        self.assasin = Assasin(assasin_location, assasin_direction)
        self.spotter = Spotter(spotter_location, spotter_direction)
        self.agent = agent_class(spotter_location, assasin_location,
                        spotter_direction, assasin_direction)
    
    def check_alive(self):

        return self.assasin.get_status() or self.spotter.get_status()

    def __repr__(self):
        
        return "({}, {}, {}, {}, {}, {}, {})".format(self.ID, self.spotter.get_location(), 
            self.assasin.get_location(), self.spotter.get_direction(),
            self.assasin.get_direction(), int(self.spotter.get_status()), 
            int(self.assasin.get_status()))