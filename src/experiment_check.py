#!/usr/bin/python3


import time
import getpass
import argparse

import requests
from collections import defaultdict


def get_arguments(description):
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('agency', type=str, help='The address of the agency')
    parser.add_argument('experiment', type=str, help='The experiment id')

    return parser.parse_args()


def get_username_pw():
    username = None
    pw = None
    try:
        # noinspection PyUnresolvedReferences
        import keyring
        username = keyring.get_password('red', 'agency_username')
        pw = keyring.get_password('red', 'agency_password')
        del keyring
    except ImportError:
        pass

    if username and pw:
        return username, pw

    username = input('agency username: ')
    pw = getpass.getpass('agency password: ')

    return username, pw


def main():
    args = get_arguments('Prints status information about the given experiment')

    username, pw = get_username_pw()

    run_while_working(args.agency, args.experiment, username, pw, verbose=True)


def get_batches(agency, username, pw, experiment_id):
    url = '{}/{}?experimentId={}'.format(agency, 'batches', experiment_id)
    resp = requests.get(url, auth=(username, pw))

    batches = list(filter(lambda b: b['experimentId'] == experiment_id, resp.json()))

    return batches


def get_state_dict(batches):
    state_dict = defaultdict(lambda: 0)
    for batch in batches:
        state_dict[batch['state']] += 1
    return dict(state_dict)


def check_finished(state_dict):
    return all(map(lambda k: k in ['succeeded', 'failed', 'cancelled'], state_dict.keys()))


def run_while_working(agency, experiment_id, username, pw, verbose=False):
    while True:
        batches = get_batches(agency, username, pw, experiment_id)
        state_dict = get_state_dict(batches)

        if check_finished(state_dict):
            if verbose:
                print('{: <100}'.format(str(state_dict)), flush=True)
            return state_dict
        elif verbose:
            print('{: <100}'.format(str(state_dict)), end='\r', flush=True)

        time.sleep(2)


if __name__ == '__main__':
    main()
