import requests
import json
import random


def import_counties():
    '''Fetches counties from Taxonomy rest endpoint'''
    r = requests.get('https://sokannonser.dev.services.jtech.se/vf/search?offset=0&limit=100&type=county', headers={'api-key': 'apa'})
    data = r.json()
    lan = []
    for l in data['result']:
        lan.append([l['id']])
    return lan


def import_municipalities():
    '''Fetches municipalities from Taxonomy rest endpoint'''
    r = requests.get('https://sokannonser.dev.services.jtech.se/vf/search?offset=0&limit=1000&type=municipality', headers={'api-key': 'apa'})
    data = r.json()
    muni = []
    for m in data['result']:
        muni.append([m['id']])
    return muni


def import_occupation_groups():
    '''Fetches occupation groups from taxonomy rest endpoint'''
    r = requests.get('https://sokannonser.dev.services.jtech.se/vf/search?offset=0&limit=1000&type=occupation-group', headers={'api-key': 'apa'})
    data = r.json()
    jg = []
    for j in data['result']:
        jg.append([j['id']])
    return jg


def generate_offset(limit):
    offset = []
    for x in range(10):
        offset.append([str(x*limit)])
    return offset


def generate_variable_dict(**kwargs):
    '''
    Generates a dictionary with the variables of the key and values sent in. Key should be a the type and values a list of list of string.
    ex: generate_variable_dict(municipality=[['1100'],['0210']])
    '''
    payload = {"version": 1}
    variables = []
    for key, valuelist in kwargs.items():
        variables.append({"names": [key], "values": valuelist})
    payload['variables'] = variables
    return payload


def generate_key_value_dict(size, **kwargs):
    '''
    Generates a dictionary in the loader.io key/value format
    '''
    payload = {}
    param_keys = []
    param_values = []
    for key, _ in kwargs.items():
        param_keys.append(key)
    for i in range(size):
        rand_list = []
        for key, valuelist in kwargs.items():
            v = random.randint(0, len(valuelist)-1)
            rand_list.append(valuelist[v][0])
        param_values.append(rand_list)
    payload['keys'] = param_keys
    payload['values'] = param_values
    return payload


def to_file(j, filename):
    with open(filename, "w") as fp:
        json.dump(j, fp)


if __name__ == "__main__":
    muni = import_municipalities()
    lan = import_counties()
    j_group = import_occupation_groups()
    offset_10 = generate_offset(10)
    offset_100 = generate_offset(100)
    to_file(generate_variable_dict(region=lan), "test_variable_region.json")
    to_file(generate_variable_dict(municipality=muni), "test_variable_municipality.json")
    to_file(generate_variable_dict(occupation_group=j_group), "test_variable_occ_group.json")
    to_file(generate_variable_dict(region=lan, group=j_group, offset=offset_100), "test_bulk_variable_region_occ_group.json")
    to_file(generate_variable_dict(municipality=muni, group=j_group, offset=offset_10), "test_variable_municipality_occ_group.json")
    to_file(generate_key_value_dict(1000, municipality=muni, group=j_group), "test_key_value_municipality_occ_group_1000.json")
    to_file(generate_key_value_dict(1000, region=lan, group=j_group), "test_key_value_region_occ_group_1000.json")
    to_file(generate_key_value_dict(1000, municipality=muni), "test_key_value_municipality_1000.json")
