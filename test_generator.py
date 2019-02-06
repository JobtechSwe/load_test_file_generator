import requests
import json


def import_counties():
    r = requests.get('https://sokannonser.dev.services.jtech.se/vf/search?offset=0&limit=100&type=county', headers={'api-key': 'apa'})
    data = r.json()
    lan = data['result']
    return lan


def import_municipalities():
    r = requests.get('https://sokannonser.dev.services.jtech.se/vf/search?offset=0&limit=1000&type=municipality', headers={'api-key': 'apa'})
    data = r.json()
    muni = data['result']
    return muni


def generate_municipalities_file(muni):
    payload = {"version": 1,
               "variables": [{
                   "names": ["municipality"],
                   "values": []
               }
               ]}
    m_list = []
    for m in muni:
        m_list.append([m['legacyAmsTaxonomyId']])
    payload['variables'][0]['values'] = m_list
    return payload


def generate_municipalities_key_value(muni):
    payload = {"keys": ["municipality"],
               "values": []
               }
    m_list = []
    for m in muni:
        m_list.append([m['legacyAmsTaxonomyId']])
    payload['values'] = m_list
    return payload


def to_file(j, filename):
    with open(filename, "w") as fp:
        json.dump(j, fp)


if __name__ == "__main__":
    p = generate_municipalities_file(import_municipalities())
    to_file(p, "test_variableV2.json")
