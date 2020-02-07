import argparse

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from experiment_check import get_username_pw
from show_result import get_detailed_result, get_state_durations

EXPERIMENT_IDS = ['5e397444eeaf898b6e4b4353', '5e3975513fa6fb7dd4a35747', '5e397635eeaf898b6e4b4383']
STATE = 'processing'


def get_arguments():
    parser = argparse.ArgumentParser(description='Plots the data given by experiment ids')

    parser.add_argument('agency', type=str, help='The address of the agency')

    return parser.parse_args()


def detailed_results_to_data_frame(detailed_results):
    data = {
        'experimentId': [],
        'numBatches': [],
        'scheduledDurations': [],
        'processingDurations': [],
        'mount': []
    }

    for experiment_id, detailed_result in detailed_results.items():
        num_batches = len(detailed_result['batchHistories'])
        scheduled_durations = get_state_durations(detailed_result['batchHistories'], 'scheduled')
        processing_durations = get_state_durations(detailed_result['batchHistories'], 'processing')

        assert(len(processing_durations) == num_batches)
        assert(len(scheduled_durations) == num_batches)

        data['experimentId'].extend([experiment_id] * num_batches)
        data['numBatches'].extend([num_batches] * num_batches)
        data['scheduledDurations'].extend(scheduled_durations)
        data['processingDurations'].extend(processing_durations)
        data['mount'].extend([False] * num_batches)

    return pd.DataFrame(data=data)


def main():
    args = get_arguments()
    username, pw = get_username_pw()

    detailed_results = {}
    for experiment_id in EXPERIMENT_IDS:
        detailed_results[experiment_id] = get_detailed_result(args.agency, experiment_id, username, pw)

    df = detailed_results_to_data_frame(detailed_results)
    print(df)

    fig, ax = plt.subplots(1, 1)

    sns.set(style="ticks", palette="pastel")
    sns.boxplot(x='numBatches', y='processingDurations', hue='mount', palette=['m', 'g'], data=df, ax=ax)
    fig.savefig('plot.pdf', bibox_inches='tight')


if __name__ == '__main__':
    main()
