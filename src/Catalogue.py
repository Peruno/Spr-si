class Catalogue:
    catalogue = {
        "nozzle1": {
            "height": 20,
            "x_measurement": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
            "h_measurement": [0, 5, 4, 4, 4, 4, 4, 4, 4, 5, 0]}
    }

    def __init__(self, name):
        self.name = name

    def get_height(self):
        values = self.__get_values()
        return values.get("height")

    def get_x_measurement(self):
        values = self.__get_values()
        return values.get("x_measurement")

    def get_h_measurement(self):
        values = self.__get_values()
        return values.get("h_measurement")

    def __get_values(self):
        values = self.catalogue.get(self.name)
        if values is None:
            raise Exception("Name not contained in catalogue.")

        return values





