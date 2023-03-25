import csv

data = None

truck_sizes = {
    "small": {"capacity": 1000, "cost": 4.87},
    "medium": {"capacity": 4000, "cost": 11.92},
    "large": {"capacity": 10000, "cost": 27.44},
}

transports = []
next_transport_id = 1


def read_data():
    global data
    if data is None:
        with open("DNIT-Distancias.csv", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            header = next(reader)
            data = []
            for row in reader:
                data.append(row)
            distances = []
            for city in header:
                distance = [city, header.index(city), data[header.index(city)]]
                distances.append(distance)
            data = distances
    return data


def check_distance_between_cities(start, end):
    distances = read_data()
    start_index = -1
    end_index = -1
    km = 0
    for distance in distances:
        if start == distance[0]:
            start_index = distance[1]
        if end == distance[0]:
            end_index = distance[1]
    if start_index < 0 or end_index < 0:
        print(
            f"O nome de alguma das cidades não existe. Não foi possível encontrar uma rota de {start} até {end}."
        )
        return
    if start_index > end_index:
        start_index, end_index = end_index, start_index
    km = int(distances[start_index][2][end_index])
    if km:
        print(f"A viagem de {start} até {end} tem {km} km de distância.")
        return km
    else:
        print(f"Não foi possível encontrar uma rota de {start} até {end}.")


def get_city_list():
    cities = []
    print("Forneça a lista, em ordem, da sua rota. ")
    while True:
        city = input("Insira o nome da cidade (ou 'pronto' para finalizar): ").upper()
        if city == "PRONTO":
            print("Sua rota é:", " - ".join(cities))
            return cities
        cities.append(city)


def get_routes_and_km(cities):
    distances = []
    for i in range(len(cities) - 1):
        start = cities[i]
        end = cities[i + 1]
        distance = check_distance_between_cities(start, end)
        if distance:
            distances.append([start, end, distance])

    if not distances:
        print("Não foi possível encontrar uma rota válida.")
        return None
    return distances


def get_list_of_items():
    items = {}
    while True:
        item = input("Insira o nome do item (ou 'pronto' para finalizar): ").upper()
        if item == "PRONTO":
            items_list = [f"{key}: {value} kg" for key, value in items.items()]
            print("Sua lista de itens é:", ", ".join(items_list))
            return items
        weight = float(input("Insira o peso do item (em kg): "))
        items[item] = weight


def choose_item_destination(items, destinations):
    destination_items = {}
    for destination in destinations:
        print(f"Destino: {destination}")
        print("Insira a lista de itens separada por vírgula para este destino.")
        # create a dictionary to store the items and their frequencies
    item_counts = {}
    # Prompt the user for a list of items, separated by commas
    items_list = input().upper().split(",")

    # Remove any leading or trailing whitespace from each item
    items_list = [item.strip() for item in items_list]

    # Create a formatted string listing the items
    formatted_list = "\n".join(f"- {item}" for item in items_list)

    # Print the formatted list
    print(f"List of items:\n{formatted_list}")
        # Count the frequency of each item
    for item in items_list:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1

    # Create a dictionary of items and their total weight for this destination
    destination_items[destination] = {}
    for item, count in item_counts.items():
        if item in items:
            weight = items[item] * count
            destination_items[destination][item] = weight

    # Print the total weight for each item at this destination
    item_weights = []
    for item, weight in destination_items[destination].items():
        item_weights.append(f"{item}: {weight} kg")
    print("Total weight for each item:")
    print(", ".join(item_weights))

    return destination_items


def calculate_cost(distance, truck_size, items, destinations):
    capacity = truck_sizes[truck_size]["capacity"]
    cost_per_km = truck_sizes[truck_size]["cost"]
    total_weight = sum(items.values())
    if total_weight > capacity:
        print(
            f"O peso total dos itens ({total_weight} kg) excede a capacidade do caminhão {truck_size} ({capacity} kg)."
        )
        return None
    total_cost = distance * cost_per_km
    for destination, items_dict in destinations.items():
        for item, weight in items_dict.items():
            item_cost = weight / total_weight * total_cost
            print(f"Custo para enviar {weight} kg de {item} para {destination}: R$ {item_cost:.2f}")
    print(f"Custo total: R$ {total_cost:.2f}")
    return total_cost


def create_transport():
    global next_transport_id
    cities = get_city_list()
    routes_and_km = get_routes_and_km(cities)
    items = get_list_of_items()
    destinations = choose_item_destination(items, cities)
    if not routes_and_km or not items or not destinations:
        return None
    distance =