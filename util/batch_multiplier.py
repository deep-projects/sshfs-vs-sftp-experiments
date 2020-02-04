#!/usr/bin/python3


import argparse
import os.path
import copy
from ruamel.yaml import YAML, YAMLError

JSON_INDENT = 4

yaml = YAML(typ='safe')
yaml.default_flow_style = False


def get_arguments():
    parser = argparse.ArgumentParser(description='Multiply batches of a RED experiment.')

    parser.add_argument('infile', type=str, help='The template RED file whose batch is multiplied')
    parser.add_argument('num-batches', type=int, help='The number of batches in the result file')

    return parser.parse_args()


def main():
    args = get_arguments()

    data = load_data(args.infile)

    # create new batches
    first_batch = data['batches'][0]
    new_batches = []
    for i in range(vars(args)['num-batches']):
        new_batch = copy.deepcopy(first_batch)
        new_batches.append(new_batch)

    data['batches'] = new_batches
    target_filename = '{}_extended.yml'.format(os.path.splitext(args.infile)[0])
    dump_data(target_filename, data)


def dump_data(target_filename, data):
    with open(target_filename, 'w') as f:
        try:
            yaml.dump(data, f)
        except YAMLError:
            print('could not dump')


def load_data(infile):
    with open(infile, 'r') as f:
        try:
            data = yaml.load(f)
        except Exception:
            raise IOError('could not load file')
    return data


if __name__ == '__main__':
    main()
