import argparse
import subprocess
import tempfile

from ruamel.yaml import YAML, YAMLError

from batch_multiplier import multiply_batches, load_data
from experiment_check import run_while_working, get_username_pw

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


def execute_experiment(data):
    with tempfile.NamedTemporaryFile(mode='w') as execution_file:
        try:
            yaml.dump(data, execution_file)
        except YAMLError:
            print('could not dump')

        execution_file.flush()

        execution_result = subprocess.run(
            ['faice', 'exec', execution_file.name, '--debug', '--disable-retry'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )  # type: subprocess.CompletedProcess

    try:
        return yaml.load(execution_result.stdout)['response']['experimentId']
    except Exception as e:
        print('failed to execute experiment. faice stdout: {}'.format(execution_result.stdout))
        raise e


def main():
    args = get_arguments()

    data = load_data(args.template)
    multiply_batches(data, vars(args)['num-batches'])

    experiment_id = execute_experiment(data)

    print('experimentId: {}'.format(experiment_id), flush=True)

    agency = data['execution']['settings']['access']['url']

    username, pw = get_username_pw()
    run_while_working(agency, experiment_id, username, pw, verbose=True)


if __name__ == '__main__':
    main()
