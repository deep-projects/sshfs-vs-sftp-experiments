#!/usr/bin/python3


import time
import os.path
import getpass
import argparse
import requests
from multiprocessing import Pool
from collections import defaultdict
from pprint import pprint


def get_arguments():
    parser = argparse.ArgumentParser(description='Prints status information about the given experiment')

    parser.add_argument('agency', type=str, help='The address of the agency')
    parser.add_argument('experimentId', type=str, help='The experiment id')

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
    args = get_arguments()

    username, pw = get_username_pw()

    run_while_working(args.agency, args.experimentid, username, pw)

    pprint(get_detailed_result(args.agency, args.experimentid, username, pw))


class BatchFetcher:
    def __init__(self, agency, username, password):
        self.agency = agency
        self.username = username
        self.password = password

    def __call__(self, batch):
        result = requests.get(
            os.path.join(self.agency, 'batches', batch['_id']),
            auth=(self.username, self.password)
        ).json()
        print('#', end='', flush=True)
        return result


def fetch_batches(batches, agency, username, pw):
    with Pool(5) as p:
        print('Fetching batches: [', end='', flush=True)
        batch_list = list(p.map(BatchFetcher(agency, username, pw), batches))
        print(']', flush=True)

    return batch_list


def get_batches(agency, username, pw, experiment_id):
    resp = requests.get(os.path.join(agency, 'batches'), auth=(username, pw))

    batches = list(filter(lambda b: b['experimentId'] == experiment_id, resp.json()))

    return batches


def get_state_dict(batches):
    state_dict = defaultdict(lambda: 0)
    for batch in batches:
        state_dict[batch['state']] += 1
    return dict(state_dict)


def check_finished(state_dict):
    return all(map(lambda k: k in ['succeeded', 'failed', 'cancelled'], state_dict.keys()))


def get_detailed_result(agency, experiment_id, username, pw):
    batches = get_batches(agency, username, pw, experiment_id)

    state_dict = get_state_dict(batches)

    batch_list = fetch_batches(batches, agency, username, pw)
    batch_histories = []
    for batch in batch_list:
        if batch['history']:
            batch_history = []
            for history_entry in batch['history']:
                batch_history.append({'state': history_entry['state'], 'time': history_entry['time']})
            batch_histories.append({'history': batch_history, 'node': batch['node']})

    return {
        'states': state_dict,
        'batchDurations': batch_histories
    }


def run_while_working(agency, experiment_id, username, pw):
    while True:
        batches = get_batches(agency, username, pw, experiment_id)
        state_dict = get_state_dict(batches)

        if check_finished(state_dict):
            return state_dict

        time.sleep(2)


if __name__ == '__main__':
    main()
