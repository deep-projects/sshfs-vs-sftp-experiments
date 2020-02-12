import argparse
import os
from collections import defaultdict

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from experiment_check import get_username_pw
from experiment_scheduler import EXECUTED_EXPERIMENTS_DIR
from show_result import get_state_durations, get_detailed_result_with_cache

NUM_CONCURRENT_BATCHES_LABEL = 'number of concurrent batches'
PROCESSING_DURATION_LABEL = 'processing duration in seconds'
SCHEDULING_DURATION_LABEL = 'scheduling duration in seconds'
NUM_FAILURES_LABEL = 'number of failures'
FAIL_PERCENTAGE_LABEL = 'failures in %'
MOUNT_LABEL = 'transfer method'


def get_arguments():
    parser = argparse.ArgumentParser(description='Plots the data given by experiment ids')

    parser.add_argument('agency', type=str, help='The address of the agency')

    return parser.parse_args()


def mount_to_transfer_method(mount):
    return 'sshfs' if mount else 'sftp'


def detailed_results_to_data_frame(detailed_results):
    data = {
        'experimentId': [],
        NUM_CONCURRENT_BATCHES_LABEL: [],
        SCHEDULING_DURATION_LABEL: [],
        PROCESSING_DURATION_LABEL: [],
        MOUNT_LABEL: [],
        'states': []
    }

    for experiment_id, detailed_result in detailed_results.items():
        num_batches = len(detailed_result['batchHistories'])
        num_concurrent_batches = detailed_result['numConcurrentBatches']

        try:
            scheduled_durations = get_state_durations(detailed_result['batchHistories'], 'scheduled')
            processing_durations = get_state_durations(detailed_result['batchHistories'], 'processing')
        except ValueError:
            raise ValueError('Failed to get durations for experiment "{}"'.format(experiment_id))

        assert(len(processing_durations) == num_batches)
        assert(len(scheduled_durations) == num_batches)

        transfer_method = mount_to_transfer_method(detailed_result['mount'])

        data['experimentId'].extend([experiment_id] * num_batches)
        data[NUM_CONCURRENT_BATCHES_LABEL].extend([num_concurrent_batches] * num_batches)
        data[SCHEDULING_DURATION_LABEL].extend(scheduled_durations)
        data[PROCESSING_DURATION_LABEL].extend(processing_durations)
        data[MOUNT_LABEL].extend([transfer_method] * num_batches)
        data['states'].extend(detailed_result['batchStates'])

    return pd.DataFrame(data=data)


def detailed_results_to_success_rate_data_frame(detailed_results):
    data = defaultdict(lambda: {NUM_FAILURES_LABEL: 0, 'numBatches': 0})

    for experiment_id, detailed_result in detailed_results.items():
        num_concurrent_batches = detailed_result['numConcurrentBatches']
        mount = detailed_result['mount']
        data[(num_concurrent_batches, mount)][NUM_FAILURES_LABEL] += detailed_result['states'].get('failed', 0)
        data[(num_concurrent_batches, mount)]['numBatches'] += len(detailed_result['batchHistories'])

    frame_data = {
        NUM_FAILURES_LABEL: [],
        MOUNT_LABEL: [],
        NUM_CONCURRENT_BATCHES_LABEL: [],
        'numBatches': [],
        FAIL_PERCENTAGE_LABEL: []
    }

    for key, value in data.items():
        num_concurrent_batches, mount = key
        transfer_method = mount_to_transfer_method(mount)
        num_failures = value[NUM_FAILURES_LABEL]
        num_batches = value['numBatches']

        frame_data[NUM_FAILURES_LABEL].append(num_failures)
        frame_data[MOUNT_LABEL].append(transfer_method)
        frame_data[NUM_CONCURRENT_BATCHES_LABEL].append(num_concurrent_batches)
        frame_data['numBatches'].append(num_batches)
        frame_data[FAIL_PERCENTAGE_LABEL].append((num_failures / num_batches) * 100)

    return pd.DataFrame(data=frame_data)


def get_experiment_ids_from_executed_experiments():
    experiment_ids = []
    for filename in os.listdir(EXECUTED_EXPERIMENTS_DIR):
        if os.path.isfile(os.path.join(EXECUTED_EXPERIMENTS_DIR, filename)):
            experiment_ids.append(os.path.splitext(filename)[0])

    return experiment_ids


def main():
    args = get_arguments()
    username, pw = get_username_pw()

    detailed_results = {}
    for experiment_id in get_experiment_ids_from_executed_experiments():
        detailed_results[experiment_id] = get_detailed_result_with_cache(args.agency, experiment_id, username, pw)

    processing_time_df = detailed_results_to_data_frame(detailed_results)
    success_rate_df = detailed_results_to_success_rate_data_frame(detailed_results)

    succeeded_df = processing_time_df[processing_time_df.states == 'succeeded']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))

    sns.set(style="ticks", palette="pastel")
    sns.boxplot(
        x=NUM_CONCURRENT_BATCHES_LABEL,
        y=PROCESSING_DURATION_LABEL,
        hue=MOUNT_LABEL,
        palette=['m', 'g'],
        data=succeeded_df,
        ax=ax1
    )
    sns.barplot(
        x=NUM_CONCURRENT_BATCHES_LABEL,
        y=FAIL_PERCENTAGE_LABEL,
        hue=MOUNT_LABEL,
        palette=['m', 'g'],
        data=success_rate_df,
        ax=ax2
    )
    fig.savefig('plot.pdf', bibox_inches='tight')


if __name__ == '__main__':
    main()
