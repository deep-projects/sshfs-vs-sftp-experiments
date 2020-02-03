#!/usr/bin/python3


import sys
import os.path
import copy
import yaml


def main():
    if len(sys.argv) != 3:
        print('usage: {} SOURCE_FILENAME NUM_BATCHES'.format(sys.argv[0]))
        return

    source_filename = sys.argv[1]
    data = load_data(source_filename)
    if data is None:
        return

    # create new batches
    first_batch = data['batches'][0]
    new_batches = []
    num_batches = int(sys.argv[2])
    for i in range(num_batches):
        new_batch = copy.deepcopy(first_batch)
        new_batch['outputs']['out_file']['connector']['access']['url'] = 'http://141.45.81.204:5000/remote_out{}.txt'.format(i)
        new_batches.append(new_batch)

    data['batches'] = new_batches
    target_filename = '{}_extended.yml'.format(os.path.splitext(source_filename)[0])
    dump_data(target_filename, data)


def dump_data(target_filename, data):
    with open(target_filename, 'w') as f:
        try:
            yaml.dump(data, f)
        except Exception:
            print('could not dump')


def load_data(source_filename):
    with open(source_filename, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except Exception:
            print('could not load file')
            return None
    return data


if __name__ == '__main__':
    main()
