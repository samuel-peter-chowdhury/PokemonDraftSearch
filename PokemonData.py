import urllib.request
import json
import csv
import numpy as np

from Database import session, PokemonModel, PokemonTypeModel, PokemonAbilityModel, PokemonMoveModel, PokemonTypeEffectiveModel


class DexData:
    def __init__(self, data: {}):
        if data is not None:
            self.dex_number = data['dex_number']
            self.evolutions = data['evos']
            self.alts = data['alts']
            self.gen_family = data['genfamily']


class Pokemon:
    def __init__(self, data: {}):
        self.name = data['name']
        self.hp = data['hp']
        self.attack = data['atk']
        self.defense = data['def']
        self.special_attack = data['spa']
        self.special_defense = data['spd']
        self.speed = data['spe']
        self.weight = data['weight']
        self.height = data['height']
        self.types = data['types']
        self.abilities = data['abilities']
        self.formats = data['formats']
        self.is_non_standard = data['isNonstandard']
        self.oob = DexData(data['oob'])
        self.moves = []
        self.special_moves = {}
        self.type_effective = {}
        self.point_value = None
        self.sprite = f'=IMAGE(\"https://www.smogon.com/dex/media/sprites/xy/{transform_pokemon_name(self.name)}.gif\")'


def transform_pokemon_name(pokemon_name: str):
    return pokemon_name.replace(' ', '-').lower()


def fetch_pokemon_data():
    pokemon_list = []
    response = str(urllib.request.urlopen('https://www.smogon.com/dex/sv/pokemon/').read())
    response = response.split(',{"pokemon":')[1].split(',"formats":[{"name"')[0].replace('\\', '')
    json_response = json.loads(response)
    for data in json_response:
        pokemon_obj = Pokemon(data)
        if pokemon_obj.is_non_standard.lower() == 'standard':
            pokemon_list.append(pokemon_obj)
    return pokemon_list


def fetch_pokemon_move_data(pokemon_obj: Pokemon):
    url = f'https://www.smogon.com/dex/sv/pokemon/{transform_pokemon_name(pokemon_obj.name)}/'
    response = str(urllib.request.urlopen(url).read())
    response = response.split(',"learnset":')[1].split(',"strategies":[')[0].replace('\\', '')
    pokemon_obj.moves = json.loads(response)


def fetch_special_move_data():
    file = open('special_moves.json')
    return json.load(file)


def fetch_type_effective_data():
    type_effective = {}
    file = open('type_data.json')
    json_object = json.load(file)
    for obj in json_object:
        for i in obj['atk_effectives']:
            if i[0].lower() not in type_effective:
                type_effective[i[0].lower()] = {}
            type_effective[i[0].lower()][obj['name'].lower()] = i[1]
    return type_effective


def fetch_point_value_data():
    point_value = {}
    filename = open('Season 8 - Tier List.csv', 'r')
    file = csv.DictReader(filename)
    reverse_point_value = {}
    values = np.arange(start=1, stop=21)
    for col in file:
        for value in values:
            if value not in reverse_point_value:
                reverse_point_value[value] = []
            cell = col[str(value)]
            if cell != '' and cell is not None:
                reverse_point_value[value].append(cell)
    for key, value in reverse_point_value.items():
        for pokemon in value:
            point_value[pokemon.lower()] = int(key)
    return point_value


def initialize_special_moves(pokemon_obj: Pokemon, data: dict):
    pokemon_moves = [move.lower() for move in pokemon_obj.moves]
    for key, value in data.items():
        pokemon_obj.special_moves[key] = []
        for move in value:
            if move in pokemon_moves:
                pokemon_obj.special_moves[key].append(move)


def initialize_type_effective(pokemon_obj: Pokemon, data: dict):
    pokemon_obj.type_effective = dict(data[pokemon_obj.types[0].lower()])
    if len(pokemon_obj.types) == 2:
        for key, value in pokemon_obj.type_effective.items():
            pokemon_obj.type_effective[key] = value * data[pokemon_obj.types[1].lower()][key]


def export_pokemon_to_tsv(pokemon: []):
    with open('pokemon_data.tsv', 'w', newline='') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
        writer.writerow(['sprite', 'name', 'type 1', 'type 2', 'abilities', 'hp', 'attack', 'defense', 'special attack',
                         'special defense', 'speed', 'weight', 'height', 'moves', 'momentum', 'recovery', 'cleric',
                         'hazard', 'hazard removal', 'disruption', 'damage reduction', 'set up', 'priority',
                         'item removal', 'status'])
        for p in pokemon:
            type_2 = p.types[1] if len(p.types) == 2 else None
            print(p.special_moves)
            writer.writerow([p.sprite, p.name, p.types[0], type_2, ', '.join(p.abilities), p.hp, p.attack, p.defense,
                             p.special_attack, p.special_defense, p.speed, p.weight, p.height, ', '.join(p.moves),
                             ', '.join(p.special_moves['momentum']), ', '.join(p.special_moves['recovery']),
                             ', '.join(p.special_moves['cleric']), ', '.join(p.special_moves['hazard']),
                             ', '.join(p.special_moves['hazard removal']), ', '.join(p.special_moves['disruption']),
                             ', '.join(p.special_moves['damage reduction']), ', '.join(p.special_moves['set up']),
                             ', '.join(p.special_moves['priority']), ', '.join(p.special_moves['item removal']),
                             ', '.join(p.special_moves['status'])])


def initialize_database():
    pokemon = fetch_pokemon_data()
    special_moves = fetch_special_move_data()
    type_effective = fetch_type_effective_data()
    point_value = fetch_point_value_data()
    pokemon_count = len(pokemon)
    for i, p in enumerate(pokemon):
        print(f'{i}/{pokemon_count}')
        fetch_pokemon_move_data(p)
        initialize_special_moves(p, special_moves)
        initialize_type_effective(p, type_effective)
        if p.name.lower() in point_value:
            p.point_value = point_value[p.name.lower()]
        pokemon_model = PokemonModel(p)
        session.add(pokemon_model)
        session.commit()
        for t in p.types:
            pokemon_type_model = PokemonTypeModel(pokemon_model.id, t)
            session.add(pokemon_type_model)
        for a in p.abilities:
            pokemon_ability_model = PokemonAbilityModel(pokemon_model.id, a)
            session.add(pokemon_ability_model)
        for m in p.moves:
            pokemon_move_model = PokemonMoveModel(pokemon_model.id, m, None)
            session.add(pokemon_move_model)
        for key, value in p.special_moves.items():
            for m in value:
                pokemon_move_model = PokemonMoveModel(pokemon_model.id, m, key)
                session.add(pokemon_move_model)
        for key, value in p.type_effective.items():
            pokemon_type_effective_model = PokemonTypeEffectiveModel(pokemon_model.id, key, value)
            session.add(pokemon_type_effective_model)
        session.commit()
