import random
import json


def print_random_leader(data):
    seed = random.randint(0, len(data.keys()))
    random_id = list(data)[seed]
    leader = data[random_id]
    print(f'{leader["firstname"]} {leader["lastname"]} led MLB in...')
    for lead in leader['leads']:
        print(f'{lead["category"]} with {lead["value"]} in {lead["year"]} for {lead["team"]}')


def open_from_json(filename):
    in_file = open(filename, 'r', encoding='utf-8')
    data = json.load(in_file)
    in_file.close()
    return data


if __name__ == '__main__':
    data = open_from_json('playerData.json')
    print_random_leader(data)