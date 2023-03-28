import unittest
from main import Distances, City, get_pairs, read_items, Leg, CargoItem, Cargo, Truck


class Test(unittest.TestCase):
    def test_distances_class(self):
        distances = Distances("DNIT-Distancias.csv")
        origin = City("SAO PAULO")
        destination = City("SALVADOR")
        distance = 1962
        self.assertEqual(distances.get(origin, destination), distance)

        origin = City("LONDRES")
        destination = City("SAO PAULO")
        distance = None
        distance = distances.get(origin, destination)
        self.assertIsNone(distance)

    def test_get_pairs(self):
        self.assertEqual(get_pairs([1, 2, 3]), [(1, 2), (2, 3)])

    def test_city_equality(self):
        sp1 = City("SP")
        sp2 = City("SP")
        self.assertEqual(sp1, sp2)

    def test_get_trucks_for_leg(self):
        global Truck
        origin = City("SAO PAULO")
        destination = City("SALVADOR")
        banana = CargoItem("A", 1)
        uva = CargoItem("B", 2)
        cargo = Cargo()
        cargo.add(banana, 10)
        cargo.add(uva, 5)

        leg = Leg(origin, destination, cargo)

        truck_combinations = Truck.get_trucks_for_leg(leg)

        total_weight = 20

        self.assertEqual(leg.get_total_weight(), total_weight)


unittest.main()
