import os
import argparse
import subprocess
from pprint import pprint

from ruamel.yaml import YAML

from batch_multiplier import multiply_batches, load_data, dump_data
from experiment_check import run_while_working, get_username_pw
from show_result import get_detailed_result

yaml = YAML(typ='safe')
yaml.default_flow_style = False


TMP_FILE_NAME = 'tmp_file'


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Runs an experiment described in the template experiment, inserts NUM_BATCHES batches'
    )

    parser.add_argument('template', type=str, help='The template RED file to execute')
    parser.add_argument('num-batches', type=int, help='The number of batches to execute')

    return parser.parse_args()


def main():
    args = get_arguments()

    data = load_data(args.template)
    multiply_batches(data, vars(args)['num-batches'])

    dump_data(TMP_FILE_NAME, data)

    execution_result = subprocess.run(
        ['faice', 'exec', 'tmp_file', '--debug', '--disable-retry'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )  # type: subprocess.CompletedProcess

    result_data = yaml.load(execution_result.stdout)
    experiment_id = result_data['response']['experimentId']

    print('experimentId: {}'.format(experiment_id), flush=True)

    agency = data['execution']['settings']['access']['url']

    username, pw = get_username_pw()
    print('waiting for the experiment to finish.', flush=True)
    run_while_working(agency, experiment_id, username, pw, verbose=True)

    # pprint(get_detailed_result(agency, experiment_id, username, pw)['states'])


if __name__ == '__main__':
    main()
