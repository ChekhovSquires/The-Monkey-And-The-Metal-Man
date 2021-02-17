from games.TMATMM.Piece import Assasin, Spotter
# from Piece import Assasin, Spotter


class Player:

    def __init__(self, ID, spotter_location, assasin_location,
                 spotter_direction, assasin_direction, agent_class, print_logs=True):

        self.ID = ID
        self.assasin = Assasin(assasin_location, assasin_direction)
        self.spotter = Spotter(spotter_location, spotter_direction)
        self.agent = agent_class(spotter_location, assasin_location,
                                 spotter_direction, assasin_direction, print_logs=print_logs)

    def check_alive(self):

        return self.assasin.get_status() or self.spotter.get_status()

    def __repr__(self):

        return "({}, {}, {}, {}, {}, {}, {})".format(self.ID, self.spotter.get_location(),
                                                     self.assasin.get_location(), self.spotter.get_direction(),
                                                     self.assasin.get_direction(), int(self.spotter.get_status()),
                                                     int(self.assasin.get_status()))

    def __iter__(self):

        yield ("agent id", self.ID)
        yield ("spotter alive", self.spotter.get_status())
        yield ("assasin alive", self.assasin.get_status())
        yield ("spotter location", self.spotter.get_location())
        yield ("assasin location", self.assasin.get_location())
        yield ("spotter direction", self.spotter.get_direction())
        yield ("assasin direction", self.assasin.get_direction())
