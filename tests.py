import unittest
from main import (
    check_distance_between_cities,
    get_destination_for_objects,
    get_truck_combination_for_route,
    Distances,
    City,
    get_pairs,
    read_items,
)


# Test for Option 1
class TestTransport(unittest.TestCase):
    def test_check_distance_between_cities(self):
        # Test case 1: Test a valid distance between two cities
        start = "SAO PAULO"
        end = "RIO DE JANEIRO"
        expected_distance = 429
        self.assertEqual(check_distance_between_cities(start, end), expected_distance)

        # Test case 2: Test an invalid distance between two cities
        start = "SAO PAULO"
        end = "LONDRES"
        expected_output = None
        self.assertEqual(check_distance_between_cities(start, end), expected_output)

        # Test case 3: Test an invalid distance between same city
        start = "SAO PAULO"
        end = "SAO PAULO"
        expected_output = None
        self.assertEqual(check_distance_between_cities(start, end), expected_output)

    def test_get_destination_for_objects(self):
        items = {"MAMAO": 300.0}
        cities = ["SAO PAULO", "BELEM"]
        expected_output = {"BELEM": {"MAMAO": 300.0}}
        self.assertEqual(
            get_destination_for_objects(items, cities),
            expected_output,
        )

        items = {"CEBOLA": 400.0, "CHUCHU": 500.0, "CARAMBOLA": 20.0}
        cities = ["PORTO ALEGRE", "SAO LUIS", "BELEM"]
        expected_output = {
            "SAO LUIS": {"CEBOLA": 400.0},
            "BELEM": {"CHUCHU": 500.0, "CARAMBOLA": 20},
        }
        self.assertEqual(
            get_destination_for_objects(items, cities),
            expected_output,
        )

    def test_get_truck_combination_for_route(self):
        destination_for_objects = {
            "SALVADOR": {"CEBOLA": {"peso": 2.0, "quantidade": 30}}
        }
        trip_info = [["SAO PAULO", "SALVADOR", 1962]]
        expected_num_of_trucks = 1
        expected_truck_sizes = "small"
        expected_km = 1962
        expected_cost_per_km = 4.87
        expected_total_cost = 9554.94
        self.assertEqual(
            get_truck_combination_for_route(destination_for_objects, trip_info),
            f"A maneira mais econômica de transportar todos os objetos é usar 0 caminhão(ões) de tamanho(s) , por um custo de R$0.00/km. Ao todo, para percorrer {expected_km}km, o custo será de R${expected_total_cost}",
        )

    def test_distances_class(self):
        distances = Distances("DNIT-Distancias.csv")
        origin = City("SAO PAULO")
        destination = City("SALVADOR")
        distance = 1962
        self.assertEqual(distances.get(origin, destination), distance)

    def test_get_pairs(self):
        self.assertEqual(get_pairs([1, 2, 3]), [(1, 2), (2, 3)])

    def test_city_equality(self):
        sp1 = City("SP")
        sp2 = City("SP")
        self.assertEqual(sp1, sp2)

    def test_read_items(self):
        items = read_items()
        print(items)


unittest.main()
