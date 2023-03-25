import csv


class City(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name

    def __str__(self):
        return self.name

    @classmethod
    def from_input(cls):
        name = input("Nome da cidade:").upper()
        if name == "":
            return None
        return cls(name)


class Cargo(object):
    def __init__(self):
        self.quantities = {}

    def add(self, item, quantity):
        self.quantities[item.name] = quantity

    def get(self, item):
        return self.quantities[item.name]


class Leg(object):
    def __init__(self, origin, destination, cargo):
        self.origin = origin
        self.destination = destination
        self.cargo = cargo


class Truck(object):
    def __init__(self, type, capacity, price_per_km):
        self.type = type
        self.capacity = capacity
        self.price_per_km = price_per_km


class CargoItem(object):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name

    def __str__(self):
        return f"{self.name} ({self.weight})"

    def __repr__(self):
        return f"{self.name} ({self.weight}kg)"

    @classmethod
    def from_input(cls):
        name = input("Item a ser transportado:").upper()
        if name == "":
            return None
        weight = float(input("Peso do item: "))
        return cls(name, weight)


class Transport(object):
    def __init__(self, legs, fleet):
        self.legs = legs
        self.fleet = fleet


class Transport(object):
    def __init__(self, trucks):
        self.trucks = trucks


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
        return self.data[origin.name][destination.name]


truck_info = {
    "small": {"capacity": 1000, "cost": 4.87},
    "medium": {"capacity": 4000, "cost": 11.92},
    "large": {"capacity": 10000, "cost": 27.44},
}


def check_distance_between_cities(start, end):
    start_index = -1
    end_index = -1
    km = 0

    for info in city_info:
        city_index = info[0]
        city_name = info[1]
        if start == city_name:
            start_index = city_index
        if end == city_name:
            end_index = city_index

    if start_index < 0 or end_index < 0:
        print(f"Erro: O nome de alguma das cidades não foi encontrado.")
        return None
    if start_index > end_index:
        start_index, end_index = end_index, start_index
    km = int(city_info[start_index][2][end_index])
    if km > 0:
        print(f"A viagem de {start} até {end} tem {km} km de distância.")
        return km
    if start_index == end_index:
        print("Erro: Cidade duplicada. Tente novamente")
    else:
        print(f"Erro: Não foi possível encontrar uma rota de {start} até {end}.")


def get_list_of_objects_and_weight():
    objects = {}
    while True:
        item = input("Insira o nome do item (ou aperte ENTER para finalizar): ").upper()
        if item == "":
            if not objects:
                print("Você deve inserir pelo menos um item.")
                return None
            return objects
        weight = float(input("Insira o peso do item (em kg): "))
        quantity = int(input("Insira a quantidade do item: "))
        objects[item] = {"peso": weight, "quantidade": quantity}


def get_pairs(city_list):
    pairs = []
    for i in range(len(city_list) - 1):
        start = city_list[i]
        end = city_list[i + 1]
        pairs.append((start, end))
    return pairs


def calculate_total_distance(distances):
    result = sum(distances)
    return result


def get_destination_for_objects(objects, cities):
    destination_for_objects = {}
    cities = cities[1:]  # remove first city
    for obj, obj_data in objects.items():
        print(f"Insira a cidade de destino para o item {obj}")
        for i, city in enumerate(cities):
            print(f"{i+1}: {city}")
        while True:
            choice = input("Escolha uma opção: ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(cities):
                    selected_city = cities[choice - 1]
                    print(
                        f"Você selecionou {selected_city} como destino do objeto {obj}."
                    )
                    if selected_city not in destination_for_objects:
                        destination_for_objects[selected_city] = {}
                    destination_for_objects[selected_city][obj] = obj_data
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Opção inválida. Tente novamente.")
    return destination_for_objects


def calculate_total_weight(objects_with_weight_and_destination):
    total_weight = 0
    for obj in objects_with_weight_and_destination.values():
        total_weight += obj["peso"] * obj["quantidade"]
    print(f"O peso total dos itens a serem transportados é de {total_weight} kg.")
    return total_weight


def calculate_total_weight_for_route(objects):
    total_weight = calculate_total_weight(objects)
    print(f"O peso total dos itens a serem transportados é de {total_weight} kg.")
    num_trucks_needed = 0
    print(
        f"São necessários {num_trucks_needed} caminhões para transportar todos os itens."
    )
    return total_weight, num_trucks_needed


def calculate_total_weight_for_destination(destination_objects):
    total_weight = 0
    for item, item_data in destination_objects.items():
        total_weight += item_data["peso"] * item_data["quantidade"]
    return total_weight


def get_truck_combination_for_route(destination_for_objects, trip_info):
    trucks_needed = {"small": 0, "medium": 0, "large": 0}
    global truck_info

    # Calculate the total weight of objects that need to be transported to each destination
    total_weights = {}
    for city, obj_data in destination_for_objects.items():
        total_weight = calculate_total_weight_for_destination(obj_data)
        total_weights[city] = total_weight

    truck_count = {
        "small": 1
    }  # Initialize with one minimun small truck required for transportation

    for city in total_weights:
        number_of_trucks = 0
        remaining_weight = float(total_weights[city])
        for truck, info in truck_info.items():
            number_of_trucks = truck_count.get(truck, 0)
            truck_capacity = info["capacity"]
            while remaining_weight > 0:
                if remaining_weight <= truck_capacity or (
                    remaining_weight >= truck_capacity and truck == "large"
                ):
                    number_of_trucks += 1
                    remaining_weight -= truck_capacity
            truck_count[truck] = number_of_trucks

    # Calculate the cost of transport for each destination
    total_distance = calculate_total_distance([info[2] for info in trip_info])
    cost_per_destination = {}
    minimum_cost_per_km = 4.87
    total_cost_per_km = 0
    if total_cost_per_km == 0:
        total_cost_per_km = minimum_cost_per_km

    # Return the cheapest way to transport all objects to all destinations
    cheapest_count = 0
    cheapest_sizes = []

    cheapest_sizes_str = ", ".join(cheapest_sizes)
    total_cost_for_transport = total_cost_per_km * total_distance
    return f"A maneira mais econômica de transportar todos os objetos é usar {cheapest_count} caminhão(ões) de tamanho(s) {cheapest_sizes_str}, por um custo de R${total_cost_per_km:.2f}/km. Ao todo, para percorrer {total_distance}km, o custo será de R${total_cost_for_transport:.2f}"


def get_list_of_cities():
    print("Forneça a lista, em ordem, da sua rota. ")
    cities = []
    while True:
        city = input(
            "Insira o nome da cidade (ou aperte ENTER para finalizar): "
        ).upper()
        if city == "":
            output = " - ".join(cities)
            if len(cities) <= 1:
                print("Erro: forneça pelo menos duas cidades.")
                continue
            print(f"Sua rota é: {output}")
            return cities
        if city in cities:
            print("Erro: Cidade duplicada.")
            continue
        cities.append(City(city))


def read_items():
    object_list = []
    item = CargoItem.from_input()
    while item is not None:
        if item not in object_list:
            object_list.append(item)
        else:
            print("Erro: objeto duplicado, e não pode ser inserido na lista.")
        item = CargoItem.from_input()
    return object_list


# --- OPTIONS ---
def main():
    print("Bem-vindo(a) ao Sistema de Transporte Interestadual de Cargas")
    while True:
        print("Digite a opção desejada:")
        print("1) Consultar trechos x modalidade")
        print("2) Cadastrar transporte")
        print("3) Dados estatísticos")
        print("4) Finalizar o programa")
        option = int(input("Opção: "))

        distances = Distances("DNIT-Distancias.csv")

        # Consultar trechos x modalidade
        if option == 1:
            start = City.from_input()
            end = City.from_input()
            d = distances.get(start, end)
            size = 0
            cost = 0
            print(
                f"Para ir da cidade {orig} até {dest} num caminhão de tamanho {size}, a distância é de {d}km, com um custo total de {cost}"
            )

        # Cadastrar transporte
        elif option == 2:
            cities = []
            print("Forneça a lista, em ordem, da sua rota. ")

            city = City.from_input()
            while city is not None:
                print("pressione ENTER para finalizar")
                if city not in cities:
                    cities.append(city)
                else:
                    print("Erro: cidade duplicada, não pode ser inserida na rota.")
                city = City.from_input()
            if len(cities) < 2:
                print("Erro: forneça pelo menos duas cidades.")
                return
            pairs = get_pairs(cities)

            for orig, dest in pairs:
                dist = distances.get(orig, dest)

                print(
                    f"Para ir da cidade {orig} até {dest}, a distância é de {dist}km."
                )

            print("Forneça a lista dos objetos. ")
            print("pressione ENTER para finalizar")

            object_list = read_items()
            cargo = Cargo()
            for object in object_list:
                quantity = input("Insira a quantidade do objeto {object}:")
                if quantity == "":
                    cargo.add(object, int(quantity))

            get_list_of_objects_and_weight(object, quantity)

            destination_for_objects = get_destination_for_objects(object_list, cities)
            trucks = get_truck_combination_for_route(destination_for_objects, distances)

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
