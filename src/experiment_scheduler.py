import copy
import os
from getpass import getpass
import argparse

from batch_multiplier import load_data, multiply_batches, dump_yaml
from experiment_check import run_while_working
from run_experiment import execute_experiment


EXECUTED_EXPERIMENTS_DIR = 'executed_experiments'

DEFAULT_BATCH_CONCURRENCY_LIMITS = [1, 5, 10, 15, 20, 25]
DEFAULT_BATCHES_PER_EXPERIMENT = 100
DEFAULT_NUM_ITERATIONS = 10
EXPERIMENT_TEMPLATES = ['sftp_template.red', 'sshfs_template.red']


class AuthenticationInfo:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    @staticmethod
    def agency_from_user_input():
        hostname = input('agency url: ')
        username = input('agency username: ')
        password = getpass('agency password: ')

        return AuthenticationInfo(hostname, username, password)

    @staticmethod
    def ssh_from_user_input():
        hostname = input('ssh server hostname: ')
        username = input('ssh username: ')
        password = getpass('ssh password: ')

        return AuthenticationInfo(hostname, username, password)


def get_arguments():
    parser = argparse.ArgumentParser(description='Executes several experiments with different configurations.')

    parser.add_argument(
        '--iterations', type=int, default=DEFAULT_NUM_ITERATIONS,
        help='How often to repeat the whole process.'
    )
    parser.add_argument(
        '--batches-per-experiment', type=int, default=DEFAULT_BATCHES_PER_EXPERIMENT,
        help='The number of batches to execute for every experiment.'
    )
    parser.add_argument(
        '--number-concurrent-batches', type=int, nargs='+', default=DEFAULT_BATCH_CONCURRENCY_LIMITS,
        help='List of integers. Every integer defines a new experiment in which this integer is used as the number of '
             'concurrent batches'
    )

    return parser.parse_args()


def main():
    args = get_arguments()

    agency_auth_info = AuthenticationInfo.agency_from_user_input()
    ssh_auth_info = AuthenticationInfo.ssh_from_user_input()

    if not os.path.isdir(EXECUTED_EXPERIMENTS_DIR):
        os.mkdir(EXECUTED_EXPERIMENTS_DIR)

    for iteration_index in range(args.iterations):
        for template in EXPERIMENT_TEMPLATES:
            template_path = os.path.join('experiment_templates', template)
            run_template(
                template_path, agency_auth_info, ssh_auth_info, iteration_index, args.batches_per_experiment,
                args.number_concurrent_batches
            )


def set_authentication_info(data, agency_auth_info, ssh_auth_info):
    data['execution']['settings']['access']['url'] = agency_auth_info.hostname
    data['execution']['settings']['access']['auth']['username'] = agency_auth_info.username
    data['execution']['settings']['access']['auth']['password'] = agency_auth_info.password

    if 'indir' in data['batches'][0]['inputs']:
        data['batches'][0]['inputs']['indir']['connector']['access']['host'] = ssh_auth_info.hostname
        data['batches'][0]['inputs']['indir']['connector']['access']['auth']['username'] = ssh_auth_info.username
        data['batches'][0]['inputs']['indir']['connector']['access']['auth']['password'] = ssh_auth_info.password
    else:
        data['batches'][0]['inputs']['infile']['connector']['access']['host'] = ssh_auth_info.hostname
        data['batches'][0]['inputs']['infile']['connector']['access']['auth']['username'] = ssh_auth_info.username
        data['batches'][0]['inputs']['infile']['connector']['access']['auth']['password'] = ssh_auth_info.password


def run_template(template_name, agency_auth_info, ssh_auth_info, iteration_index, num_batches, num_concurrent_batches):
    data = load_data(template_name)

    # create new batches
    data_copy = copy.deepcopy(data)

    set_authentication_info(data_copy, agency_auth_info, ssh_auth_info)

    multiply_batches(data_copy, num_batches)

    for concurrency_limit in num_concurrent_batches:
        run_concurrency_limit(concurrency_limit, data_copy, agency_auth_info, template_name, iteration_index)


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

    dump_yaml(dump_path, info_data)


def run_concurrency_limit(concurrency_limit, data, agency_auth_info, template, iteration_index):
    set_batch_concurrency_limit(data, concurrency_limit)

    experiment_id = execute_experiment(data)

    dump_experiment_info(experiment_id, concurrency_limit, template, iteration_index)

    run_while_working(
        agency_auth_info.hostname, experiment_id, agency_auth_info.username, agency_auth_info.password, verbose=True
    )


def set_batch_concurrency_limit(batch_data, concurrency_limit):
    batch_data['execution']['settings']['batchConcurrencyLimit'] = concurrency_limit


if __name__ == '__main__':
    main()
