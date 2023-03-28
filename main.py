import csv
import itertools
from itertools import combinations_with_replacement


class Distances(object):
    def __init__(self, csv_file):
        self.csv = csv_file
        data = {}
        with open(csv_file, newline="") as f:
            reader = csv.reader(f, delimiter=";")
            header = next(reader)

            for r, row in enumerate(reader):
                origin_city = header[r]
                data[origin_city] = {}
                for h in range(len(header)):
                    destination_city = header[h]
                    distance = int(row[h])
                    data[origin_city][destination_city] = distance
        self.data = data

    def get(self, origin, destination):
        try:
            return self.data[origin.name][destination.name]
        except KeyError:
            print("Cidade não encontrada.")
            return None

    def city_exists(self, city):
        return city.name in self.data

    def calculate_cost(self, leg, trucks):
        origin = leg.origin.name
        destination = leg.destination.name
        distance = self.data[origin][destination]
        cost = 0
        for truck in trucks:
            cost += truck.price_per_km * distance
        return cost


distances = Distances("DNIT-Distancias.csv")


class Truck(object):
    def __init__(self, type, capacity, price_per_km):
        self.type = type
        self.capacity = capacity
        self.price_per_km = price_per_km

    truck_info = {
        "PEQUENO": {"capacity": 1000, "cost": 4.87},
        "MEDIO": {"capacity": 4000, "cost": 11.92},
        "GRANDE": {"capacity": 10000, "cost": 27.44},
    }

    def __str__(self):
        type = self.type
        trucks = {}
        for type, info in cls.truck_info.items():
            trucks[type] = (info["capacity"], info["cost"])
        return trucks

    @classmethod
    def from_input(cls):
        while True:
            truck_type = input("Tamanho do caminhão (PEQUENO/MEDIO/GRANDE): ").upper()
            if truck_type in cls.truck_info:
                break
            print("Tamanho inválido, tente novamente.")
        info = cls.truck_info[truck_type]
        if truck_type == "":
            return None
        return cls(truck_type, info["capacity"], info["cost"])

    # use bruteforce to get combinations
    def get_possible_combinations(self, truck_counts):
        print("truck_counts: ", truck_counts)
        combinations_len = truck_counts["PEQUENO"]
        trucks = ["PEQUENO", "MEDIO", "GRANDE"]
        combinations = []
        for i in range(1, combinations_len + 1):
            for c in combinations_with_replacement(trucks, i):
                if len(c) == i:
                    combination_dict = {}
                    for truck in c:
                        if truck not in combination_dict:
                            combination_dict[truck] = 1
                        else:
                            combination_dict[truck] += 1
                    combinations.append(combination_dict)
        return combinations

    @classmethod
    def get_all_trucks(cls):
        trucks = {}
        for type, info in cls.truck_info.items():
            trucks[type] = (info["capacity"], info["cost"])
        return trucks

    @classmethod
    def get_trucks_for_leg(cls, leg):
        cls.leg = leg
        truck_counts = {"PEQUENO": 0, "MEDIO": 0, "GRANDE": 0}
        trucks = cls.get_all_trucks()
        small_capacity = trucks["PEQUENO"][0]
        weight = leg.get_total_weight()
        max_trucks = 0
        print("small:", small_capacity)
        print("weight:", weight)
        amount_of_small_ones = round(weight / small_capacity)
        print("amount_of_small_ones:", amount_of_small_ones)
        if amount_of_small_ones > 1:
            max_trucks = amount_of_small_ones
            truck_counts["PEQUENO"] = amount_of_small_ones
        else:
            truck_counts["PEQUENO"] = 1
        return truck_counts

    @classmethod
    def get_valid_combinations(cls, combinations, weight):
        valid_combos = []
        trucks = cls.get_all_trucks()
        print("trucks: ", trucks)
        for combination in combinations:
            print("combination: ", combination)
            print(combination.keys(), combination.values())
        print("trucks: ", trucks)
        return valid_combos

    @classmethod
    def get_capacity(cls):
        pass


class City(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) == str:
            return self.name == other

        return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def from_input(cls):
        name = input("Nome da cidade:").upper()
        if name == "":
            return None
        return cls(name)


class CargoItem(object):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __eq__(self, other):
        return self.name == other.name and self.weight == other.weight

    def __hash__(self):
        return hash((self.name, self.weight))

    def __str__(self):
        return f"{self.name} ({self.weight}kg)"

    def __repr__(self):
        return f"{self.name} ({self.weight}kg)"

    def get(self):
        return ({self.name}, {self.weight})


class Cargo(object):
    def __init__(self):
        self.items = []
        self.total_weight = 0
        self.quantity = 0

    def __str__(self):
        return str({item.name: item.weight for item in self.items})

    def add(self, item, quantity):
        for _ in range(quantity):
            self.items.append(item)
        print(f"{quantity} {item} adicionado(s) ao carregamento.")

    def get_items(self):
        return list(set(item.name for item in self.items))

    def get_weight(self):
        for item in self.items:
            self.total_weight += item.weight * self.quantity
        return self.total_weight


class Leg(object):
    def __init__(self, origin, destination, cargo):
        self.origin = origin
        self.destination = destination
        self.cargo = cargo

    def __str__(self):
        return f"{self.origin} - {self.destination}: {self.cargo}"

    def __repr__(self):
        return f"{self.origin} - {self.destination}: {self.cargo}"

    def get_total_weight(self):
        total_weight = 0.00
        print(f"cargo items: {self.cargo.get_weight()}")
        for item in self.cargo.items:
            total_weight += item.weight
        print(f"total weight: {total_weight}")
        return total_weight

    def get_distance(self):
        return distances.get(self.origin, self.destination)

    def get(self):
        return [self.origin, self.destination, self.get_total_weight()]


class Transport(object):
    def __init__(self, legs):
        self.legs = legs
        self.truck_counts = {"PEQUENO": 0, "MEDIO": 0, "GRANDE": 0}

    def calculate_cost(self, distances):
        total_cost = 0
        return total_cost


def get_pairs(city_list):
    pairs = []
    for i in range(len(city_list) - 1):
        start = city_list[i]
        end = city_list[i + 1]
        pairs.append((start, end))
    return pairs


def get_list_of_cities():
    print("Forneça a lista, em ordem, da sua rota. ")
    cities = []
    while True:
        city = input("Insira o nome da cidade (ENTER para finalizar): ").upper()
        if city == "":
            if len(cities) <= 1:
                print("Erro: forneça pelo menos duas cidades.")
                continue
            city_names = [c.name for c in cities]
            output = " - ".join(city_names)
            print(f"Sua rota é: {output}")
            return cities
        elif distances.city_exists(City(city)) == False:
            print(f"Erro: A cidade não existe. Tente novamente.")
            continue
        if city in cities:
            print("Erro: Cidade duplicada, não foi adicionada à lista.")
            continue
        cities.append(City(city))


def read_items():
    items = []
    while True:
        name = input("Item a ser transportado (ENTER para finalizar): ").upper()
        if name == "":
            break
        weight = input("Peso do item: ")
        if weight == "":
            print("Erro: peso não pode ser vazio")
            continue
        else:
            weight = float(weight)
        item = CargoItem(name, weight)
        if item not in items:
            items.append(item)
        else:
            print("Item já adicionado.")
    return items


# --- OPTIONS ---
def main():
    global distances
    print("Bem-vindo(a) ao Sistema de Transporte Interestadual de Cargas!")
    while True:
        print("Digite a opção desejada:")
        print("1) Consultar trechos x modalidade")
        print("2) Cadastrar transporte")
        print("3) Dados estatísticos")
        print("4) Finalizar o programa")
        option = int(input("Opção: "))

        # Consultar trechos x modalidade
        if option == 1:
            start = City.from_input()
            end = City.from_input()
            d = distances.get(start, end)
            truck = Truck.from_input()
            cost = truck.price_per_km
            total_cost = cost * d
            if d == None:
                print("Erro: A rota solicitada não existe. Tente novamente")
            else:
                print(
                    f"Para ir da cidade {start} até {end} num caminhão de tamanho {truck}, a distância é de {d}km, com um custo total de R${total_cost:.2f}"
                )

        # Cadastrar transporte
        elif option == 2:

            cargo = Cargo()
            cities = get_list_of_cities()
            origin = cities[0]
            items = read_items()
            legs = []

            if len(items) == 0:
                print("Erro: Insira pelo menos um item.")
                return
            for item in items:
                while True:
                    print(f"Destino para o item {item.name}")
                    possible_destinations = [city for city in cities[1:]]
                    for i, destination in enumerate(possible_destinations):
                        print(f"{i+1}. {destination.name}")
                    choice = input("Escolha o número do destino desejado: ")
                    try:
                        choice = int(choice)
                        destination = possible_destinations[choice - 1]
                        break
                    except (ValueError, IndexError):
                        print("Erro: Escolha inválida.")
                quantity = int(input(f"Quantidade do item {item.name}: "))
                cargo.add(item, quantity)
                print("Cargo information:")
                for i, item in enumerate(cargo.get_items()):
                    print(
                        f"Item {i+1}: {item}, destino: {destination}, quantidade: {quantity}"
                    )
                leg = Leg(origin, destination, cargo)
                legs.append(leg)

            transport = Transport(legs)

            trucks = transport.calculate_trucks()

            total_cost = transport.calculate_cost(distances)

            print(legs, transport, total_cost)

            for leg in transport.legs:
                total_weight = leg.get_total_weight()
                trucks = 0
                truck_counts = truck.get_trucks_for_leg(leg)
                combinations = truck.get_possible_combinations(truck_counts)
                valid_combos = truck.get_valid_combinations(combinations, total_weight)
                distance = distances.get(leg.origin, leg.destination)
                cost = distances.calculate_cost(leg, trucks)
                print(
                    f"Rota: {leg.origin} - {leg.destination}, peso total = {total_weight}kg, "
                    f"serão necessários {len(trucks)} caminhões do tamanho {truck_type}, cada um percorrerá "
                    f"uma distancia de {distance}km, totalizando R${cost:.2f}"
                )

        # Dados estatísticos
        elif option == 3:
            pass

        # Finalizar programa
        elif option == 4:
            print("Obrigado por utilizar nosso serviço!")
            break
        else:
            pass


# Check whether the module is being run as the main program
if __name__ == "__main__":
    main()

# TODO: trocar pronto por ok, mais rapido
# fazer testes
