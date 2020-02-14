# cc-agency-integration-tests

This repository contains programs that can be used to execute, fetch and evaluate experiments on a cc-agency. Furthermore there are scripts to fetch and process the results.

These experiments transfer a file from an ssh server to a docker container comparing the `sftp` protocol and the `sshfs` filesystem with a varying numbers of concurrent accesses on the ssh server.
In the container the file is read completely once.

The results of previously executed experiments are summarized in csv files located under the **results/** directory.
The python programs to execute, fetch and plot experiments are located under the **src/** directory.
The directory **experiment_templates/** contains [RED](https://www.curious-containers.cc/docs/red-format) files which are used as templates for the executed experiments.


## Dependencies

The required dependencies to execute the experiments are listed in `requirements.txt`. To install them execute `pip install -r requirements.txt`, possibly in a virtual environment.

To execute the experiments a running cc-agency installation is required.
More information on how to setup an agency can be found at the [Curious Containers Documentation](https://www.curious-containers.cc/docs/cc-agency-installation).

An ssh server (which is accessible using a password) is required to host the data.


## Execution

### Create test file
In order to transfer a file to a docker container a file named `~/test_data/infile.bin` has to be created on the ssh server.
To create a file filled with random data the following commands can be executed.

```
ssh user@my.ssh.hostname

# on the ssh server
mkdir ~/test_data
head -c 5GB /dev/urandom > ~/test_data/infile.bin
```

### Execute experiments

To execute experiments with different concurrent data accesses and protocols the `src/experiment_scheduler.py` program can be used.

```
python3 ./src/experiment_scheduler.py
```

In order to execute the experiments the *agency-hostname* of the agency on which the experiments are to be executed is asked, as well as the *agency-username* and corresponding *agency-password*.
To get access to the ssh server the *ssh-hostname*, the *ssh-username* and *ssh-password* are requested.

This will start a series of experiments that will copy 60 TB in total and can take a very long time to finish.
To speed up the process the number of experiments can be decreased.

```
python3 ./src/experiment_scheduler.py --iterations=2 --batches-per-experiment=10 --number-concurrent-batches=1,5,10

# more information with python3 ./src/experiment_scheduler.py --help
```

This will start fewer and smaller experiments so that in total 6 GB will be copied.

During the process there will be a status update that shows which experiment is currently executed and the state of this experiment.
If there are many *failed* entries, then there is probably something wrong with your configuration. Check the agency logs for more information.

#### Results

After executing the experiments there will be a `executed_experiments` directory, that contains experiment meta information.


### Fetch batch information

The program `src/create_csv.py` creates a compact representation of the executed batches.
To fetch the experiment information the agency authentication information is requested again. This can also take some minutes.
The result of this program are two csv files located inside a **results/** directory.


### Plot the results

To create a plot showing the processing times of the batches execute the program `src/plot_results.py`.
This will create the file `processing_times.pdf` inside the **results/** directory.
