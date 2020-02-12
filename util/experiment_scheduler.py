import copy
import os

from batch_multiplier import load_data, multiply_batches, dump_data
from experiment_check import get_username_pw, run_while_working
from run_experiment import execute_experiment


EXECUTED_EXPERIMENTS_DIR = 'executed_experiments'

BATCH_CONCURRENCY_LIMITS = [1, 5, 10, 15, 20, 25]
BATCHES_PER_EXPERIMENT = 100
NUM_ITERATIONS = 10
EXPERIMENT_TEMPLATES = ['sftp_template.red', 'sshfs_template.red']


def main():
    username, pw = get_username_pw()

    if not os.path.isdir(EXECUTED_EXPERIMENTS_DIR):
        os.mkdir(EXECUTED_EXPERIMENTS_DIR)

    for iteration_index in range(NUM_ITERATIONS):
        for template in EXPERIMENT_TEMPLATES:
            run_template(template, username, pw, iteration_index)


def run_template(template_name, username, pw, iteration_index):
    data = load_data(template_name)

    # create new batches
    data_copy = copy.deepcopy(data)
    multiply_batches(data_copy, BATCHES_PER_EXPERIMENT)

    for concurrency_limit in BATCH_CONCURRENCY_LIMITS:
        run_concurrency_limit(concurrency_limit, data_copy, username, pw, template_name, iteration_index)


def dump_experiment_info(experiment_id, concurrency_limit, template, iteration_index):
    print('executing experiment {}\n\titeration: {}\n\ttemplate: {}\n\tconcurrencyLimit: {}'.format(
        experiment_id,
        iteration_index,
        template,
        concurrency_limit,
    ))
    info_data = {
        'experimentId': experiment_id,
        'concurrencyLimit': concurrency_limit,
        'template': template,
        'iterationIndex': iteration_index
    }

    dump_path = os.path.join(EXECUTED_EXPERIMENTS_DIR, experiment_id + '.yml')

    dump_data(dump_path, info_data)


def run_concurrency_limit(concurrency_limit, data, username, pw, template, iteration_index):
    set_batch_concurrency_limit(data, concurrency_limit)

    experiment_id = execute_experiment(data)

    dump_experiment_info(experiment_id, concurrency_limit, template, iteration_index)

    agency = data['execution']['settings']['access']['url']
    run_while_working(agency, experiment_id, username, pw, verbose=True)


def set_batch_concurrency_limit(batch_data, concurrency_limit):
    batch_data['execution']['settings']['batchConcurrencyLimit'] = concurrency_limit


if __name__ == '__main__':
    main()
