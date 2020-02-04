import os
from multiprocessing.pool import Pool
from pprint import pprint

import requests

from experiment_check import get_batches, get_state_dict, get_username_pw, get_arguments


def main():
    args = get_arguments('Shows the result of all batches.')

    username, pw = get_username_pw()

    pprint(get_detailed_result(args.agency, args.experiment, username, pw))


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
        'batchHistories': batch_histories
    }


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


if __name__ == '__main__':
    main()
