import json


def references():
    # TODO: refactor references into YAML
    # TODO: refactor references data out into their own repo
    with open('./resource_data/growth_reference_repository.json') as json_file:
            references_data = json.load(json_file)
            json_file.close()
    return references_data