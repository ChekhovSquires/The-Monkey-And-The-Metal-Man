class Piece:
    def __init__(self, location, direction):
        self.__location = tuple(location)
        self.__direction = tuple(direction)
        self.__alive = True

    def set_location(self, location):
        self.__location = location

    def set_direction(self, direction):
        self.__direction = direction

    def killed(self):
        self.__alive = False

    def get_location(self):
        return self.__location

    def get_direction(self):
        return self.__direction

    def get_status(self):
        return self.__alive

    def set_alive(self, alive):
        self.__alive = alive


class Assasin(Piece):

    def set_location(self, location):
        prev_location = self.get_location()
        assert (abs(prev_location[0]-location[0]) +
                abs(prev_location[1]-location[1])) <= 4
        return super().set_location(location)


class Spotter(Piece):

    def set_location(self, location):
        prev_location = self.get_location()
        assert (abs(prev_location[0]-location[0]) +
                abs(prev_location[1]-location[1])) <= 2
        return super().set_location(location)
