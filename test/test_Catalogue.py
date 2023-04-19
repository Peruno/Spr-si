from src.Catalogue import Catalogue


def test_get_height():
    name = "nozzle1"
    catalogue = Catalogue(name)
    height = catalogue.get_height()

    assert height == 20


def test_get_x_measurement():
    name = "nozzle1"
    catalogue = Catalogue(name)
    x_measurement = catalogue.get_x_measurement()

    assert x_measurement == [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]


def test_get_h_measurement():
    name = "nozzle1"
    catalogue = Catalogue(name)
    h_measurement = catalogue.get_h_measurement()

    assert h_measurement == [0, 5, 4, 4, 4, 4, 4, 4, 4, 5, 0]
