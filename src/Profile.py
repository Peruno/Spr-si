class Profile:
    def __init__(self, line, nozzle):
        self.line = line
        self.nozzle = nozzle
        self.heights_of_points = {point: nozzle.get_profile(point.x, point.y) for point in line.get_points()}

    def get_heights(self):
        heights = [self.heights_of_points for point in self.line.get_points]