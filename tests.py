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
        banana = CargoItem("BANANA", 1)
        uva = CargoItem("UVA", 2)
        cargo = Cargo()
        cargo.add(banana, 1000)
        cargo.add(uva, 2000)

        leg = Leg(origin, destination, cargo)

        truck_combinations = Truck.get_trucks_for_leg(leg)

        combinations = [
            {"PEQUENO": 1},
            {"MEDIO": 1},
            {"GRANDE": 1},
            {"PEQUENO": 2},
            {"PEQUENO": 1, "MEDIO": 1},
            {"PEQUENO": 1, "GRANDE": 1},
            {"MEDIO": 2},
            {"MEDIO": 1, "GRANDE": 1},
            {"GRANDE": 2},
            {"PEQUENO": 3},
            {"PEQUENO": 2, "MEDIO": 1},
            {"PEQUENO": 2, "GRANDE": 1},
            {"PEQUENO": 1, "MEDIO": 2},
            {"PEQUENO": 1, "MEDIO": 1, "GRANDE": 1},
            {"PEQUENO": 1, "GRANDE": 2},
            {"MEDIO": 3},
            {"MEDIO": 2, "GRANDE": 1},
            {"MEDIO": 1, "GRANDE": 2},
            {"GRANDE": 3},
            {"PEQUENO": 4},
            {"PEQUENO": 3, "MEDIO": 1},
            {"PEQUENO": 3, "GRANDE": 1},
            {"PEQUENO": 2, "MEDIO": 2},
            {"PEQUENO": 2, "MEDIO": 1, "GRANDE": 1},
            {"PEQUENO": 2, "GRANDE": 2},
            {"PEQUENO": 1, "MEDIO": 3},
            {"PEQUENO": 1, "MEDIO": 2, "GRANDE": 1},
            {"PEQUENO": 1, "MEDIO": 1, "GRANDE": 2},
            {"PEQUENO": 1, "GRANDE": 3},
            {"MEDIO": 4},
            {"MEDIO": 3, "GRANDE": 1},
            {"MEDIO": 2, "GRANDE": 2},
            {"MEDIO": 1, "GRANDE": 3},
            {"GRANDE": 4},
            {"PEQUENO": 5},
            {"PEQUENO": 4, "MEDIO": 1},
            {"PEQUENO": 4, "GRANDE": 1},
            {"PEQUENO": 3, "MEDIO": 2},
            {"PEQUENO": 3, "MEDIO": 1, "GRANDE": 1},
            {"PEQUENO": 3, "GRANDE": 2},
            {"PEQUENO": 2, "MEDIO": 3},
            {"PEQUENO": 2, "MEDIO": 2, "GRANDE": 1},
            {"PEQUENO": 2, "MEDIO": 1, "GRANDE": 2},
            {"PEQUENO": 2, "GRANDE": 3},
            {"PEQUENO": 1, "MEDIO": 4},
            {"PEQUENO": 1, "MEDIO": 3, "GRANDE": 1},
            {"PEQUENO": 1, "MEDIO": 2, "GRANDE": 2},
            {"PEQUENO": 1, "MEDIO": 1, "GRANDE": 3},
            {"PEQUENO": 1, "GRANDE": 4},
            {"MEDIO": 5},
            {"MEDIO": 4, "GRANDE": 1},
            {"MEDIO": 3, "GRANDE": 2},
            {"MEDIO": 2, "GRANDE": 3},
            {"MEDIO": 1, "GRANDE": 4},
            {"GRANDE": 5},
        ]

        valid_combos = [
            {"GRANDE": 1},
            {"PEQUENO": 1, "MEDIO": 1},
            {"PEQUENO": 1, "GRANDE": 1},
            {"MEDIO": 2},
            {"MEDIO": 1, "GRANDE": 1},
            {"GRANDE": 2},
            {"PEQUENO": 2, "MEDIO": 1},
            {"PEQUENO": 2, "GRANDE": 1},
            {"PEQUENO": 1, "MEDIO": 2},
            {"PEQUENO": 1, "MEDIO": 1, "GRANDE": 1},
            {"PEQUENO": 1, "GRANDE": 2},
            {"MEDIO": 3},
            {"MEDIO": 2, "GRANDE": 1},
            {"MEDIO": 1, "GRANDE": 2},
            {"GRANDE": 3},
            {"PEQUENO": 3, "MEDIO": 1},
            {"PEQUENO": 3, "GRANDE": 1},
            {"PEQUENO": 2, "MEDIO": 2},
            {"PEQUENO": 2, "MEDIO": 1, "GRANDE": 1},
            {"PEQUENO": 2, "GRANDE": 2},
            {"PEQUENO": 1, "MEDIO": 3},
            {"PEQUENO": 1, "MEDIO": 2, "GRANDE": 1},
            {"PEQUENO": 1, "MEDIO": 1, "GRANDE": 2},
            {"PEQUENO": 1, "GRANDE": 3},
            {"MEDIO": 4},
            {"MEDIO": 3, "GRANDE": 1},
            {"MEDIO": 2, "GRANDE": 2},
            {"MEDIO": 1, "GRANDE": 3},
            {"GRANDE": 4},
            {"PEQUENO": 5},
            {"PEQUENO": 4, "MEDIO": 1},
            {"PEQUENO": 4, "GRANDE": 1},
            {"PEQUENO": 3, "MEDIO": 2},
            {"PEQUENO": 3, "MEDIO": 1, "GRANDE": 1},
            {"PEQUENO": 3, "GRANDE": 2},
            {"PEQUENO": 2, "MEDIO": 3},
            {"PEQUENO": 2, "MEDIO": 2, "GRANDE": 1},
            {"PEQUENO": 2, "MEDIO": 1, "GRANDE": 2},
            {"PEQUENO": 2, "GRANDE": 3},
            {"PEQUENO": 1, "MEDIO": 4},
            {"PEQUENO": 1, "MEDIO": 3, "GRANDE": 1},
            {"PEQUENO": 1, "MEDIO": 2, "GRANDE": 2},
            {"PEQUENO": 1, "MEDIO": 1, "GRANDE": 3},
            {"PEQUENO": 1, "GRANDE": 4},
            {"MEDIO": 5},
            {"MEDIO": 4, "GRANDE": 1},
            {"MEDIO": 3, "GRANDE": 2},
            {"MEDIO": 2, "GRANDE": 3},
            {"MEDIO": 1, "GRANDE": 4},
            {"GRANDE": 5},
        ]

        total_weight = 5000

        self.assertEqual(leg.get_total_weight(), total_weight)
        self.assertEqual(truck_combinations, {"PEQUENO": 5, "MEDIO": 0, "GRANDE": 0})
        self.assertEqual(
            Truck.get_possible_combinations({"PEQUENO": 5, "MEDIO": 0, "GRANDE": 0}),
            combinations,
        )
        self.assertEqual(
            Truck.get_valid_combinations(combinations, total_weight), valid_combos
        )

        self.assertEqual(
            Truck.get_cheapest_combo(valid_combos), {"PEQUENO": 1, "MEDIO": 1}
        )

        cheapest_combo = {"PEQUENO": 1, "MEDIO": 1}

        distance = 1962

        self.assertEqual(Distances.calculate_cost(distance, cheapest_combo), 0)


unittest.main()
