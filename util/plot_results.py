import argparse

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from experiment_check import get_username_pw
from show_result import get_detailed_result, get_state_durations

NUM_BATCHES_LABEL = 'number of batches'
PROCESSING_DURATION_LABEL = 'processing duration in seconds'
SCHEDULING_DURATION_LABEL = 'scheduling duration in seconds'

STATE = 'processing'

EXPERIMENT_IDS = []


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
