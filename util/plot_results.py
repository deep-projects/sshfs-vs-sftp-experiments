import argparse

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from experiment_check import get_username_pw
from show_result import get_detailed_result, get_state_durations

NUM_BATCHES_LABEL = 'number of batches'
PROCESSING_DURATION_LABEL = 'processing duration in seconds'
SCHEDULING_DURATION_LABEL = 'scheduling duration in seconds'

# noinspection SpellCheckingInspection
ECHO_EXPERIMENT_IDS = [
    '5e397444eeaf898b6e4b4353',  # 10
    '5e3975513fa6fb7dd4a35747',  # 100
    '5e397635eeaf898b6e4b4383',  # 1000
    '5e397850eeaf898b6e4b487c',  # 10000
]
# noinspection SpellCheckingInspection
CP_EXPERIMENT_IDS = [
    '5e3d440d422ca7d7b849ce8e',  # 5G 1
    '5e41475da167621fb065befb',  # 5G 5
    '5e3d48d87dd16bb7aba7d9b2',  # 5G 10
    '5e4148b5a167621fb065bf34',  # 5G 15
    '5e414bb5a167621fb065bf8f',  # 5G 20
]
# noinspection SpellCheckingInspection
SSHFS_EXPERIMENT_IDS = [
    '5e3d81c7a167621fb065bde9',  # 5G 1
    '5e4148331ea1eede9a9296d1',  # 5G 5
    '5e41461ea167621fb065bee3',  # 5G 10
    '5e414a3a1ea1eede9a92971c',  # 5G 15
    '5e3d8242a167621fb065bdf3',  # 5G 20
    # '5e3d82cea167621fb065be20',  # 5G 100
]
STATE = 'processing'

EXPERIMENT_IDS = SSHFS_EXPERIMENT_IDS + CP_EXPERIMENT_IDS


def get_arguments():
    parser = argparse.ArgumentParser(description='Plots the data given by experiment ids')

    parser.add_argument('agency', type=str, help='The address of the agency')

    return parser.parse_args()


def detailed_results_to_data_frame(detailed_results):
    data = {
        'experimentId': [],
        NUM_BATCHES_LABEL: [],
        SCHEDULING_DURATION_LABEL: [],
        PROCESSING_DURATION_LABEL: [],
        'mount': []
    }

    for experiment_id, detailed_result in detailed_results.items():
        num_batches = len(detailed_result['batchHistories'])
        scheduled_durations = get_state_durations(detailed_result['batchHistories'], 'scheduled')
        processing_durations = get_state_durations(detailed_result['batchHistories'], 'processing')

        assert(len(processing_durations) == num_batches)
        assert(len(scheduled_durations) == num_batches)

        data['experimentId'].extend([experiment_id] * num_batches)
        data[NUM_BATCHES_LABEL].extend([num_batches] * num_batches)
        data[SCHEDULING_DURATION_LABEL].extend(scheduled_durations)
        data[PROCESSING_DURATION_LABEL].extend(processing_durations)
        data['mount'].extend([detailed_result['mount']] * num_batches)

    return pd.DataFrame(data=data)


def main():
    args = get_arguments()
    username, pw = get_username_pw()

    detailed_results = {}
    for experiment_id in EXPERIMENT_IDS:
        detailed_results[experiment_id] = get_detailed_result(args.agency, experiment_id, username, pw)

    df = detailed_results_to_data_frame(detailed_results)

    fig, ax = plt.subplots(1, 1)

    sns.set(style="ticks", palette="pastel")
    sns.boxplot(x=NUM_BATCHES_LABEL, y=PROCESSING_DURATION_LABEL, hue='mount', palette=['m', 'g'], data=df, ax=ax)
    fig.savefig('plot.pdf', bibox_inches='tight')


if __name__ == '__main__':
    main()
