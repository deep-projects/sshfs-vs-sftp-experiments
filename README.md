# CC-Agency Integration Tests

This repository contains programs that can be used to execute, fetch and evaluate experiments using RED execution engine CC-Agency.

These experiments transfer a file from an SSH server to a docker container comparing the `sftp` protocol and the `sshfs` filesystem with a varying number of concurrent accesses on the SSH server.
In the container the file is read sequentially exactly once.

The results of previously executed experiments are summarized in CSV files located under the `results/` directory.
The python programs to execute, fetch and plot experiments are located under the `src/` directory.
The directory `experiment_templates/` contains [RED](https://www.curious-containers.cc/docs/red-format) files which are used as templates for the executed experiments.


## Dependencies

The required software dependencies to execute the experiments are listed in `requirements.txt`. To install them execute `pip install -r requirements.txt`, possibly in a virtual environment.

To execute the experiments a running CC-Agency installation is required.
More information on how to setup CC-Agency can be found at the [Curious Containers Documentation](https://www.curious-containers.cc/docs/cc-agency-installation).

An SSH server (which is accessible using a password) is required to host the data.


## Execution

### Create test file

In order to transfer a file to a Docker container a file named `~/test_data/infile.bin` has to be created on the SSH server.
To create a file filled with random data the following commands can be executed.

```bash
ssh user@my.ssh.hostname

# on the SSH server
mkdir ~/test_data
head -c 5GB /dev/urandom > ~/test_data/infile.bin
```

### Execute experiments

To execute experiments with different concurrent data accesses and protocols the `src/experiment_scheduler.py` program can be used.

```bash
python3 ./src/experiment_scheduler.py
```

In order to execute the experiments the *agency-url* of the agency on which the experiments are to be executed is asked, as well as the *agency-username* and corresponding *agency-password*.
The *agency-url* should look similar to `https://agency.example.de/cc`. You can test the *agency-url* be accessing it with you browser. This should return a hello world json object.

To get access to the SSH server the *ssh-hostname*, the *ssh-username* and *ssh-password* are requested.

This will start a series of experiments that will copy 60 TB in total and can take some days to finish.
To speed up the process the number of experiments can be decreased.

```bash
python3 ./src/experiment_scheduler.py --iterations=2 --batches-per-experiment=10 --number-concurrent-batches 1 5 10

# python3 ./src/experiment_scheduler.py --help  for more information
```

This will start fewer and smaller experiments so that in total 600 GB will be copied.
To further reduce the execution time, you can also reduce the file size of `~/test_data/infile.bin`.

During the process there will be a status update that shows which experiment is currently executed and the state of this experiment.
If there are many *failed* entries, then there is probably something wrong with your configuration.
Check the batch logs of the agency for more information (see [Agency API](https://www.curious-containers.cc/docs/cc-agency-api#get-experiments)).

#### Results

After executing the experiments there will be a `executed_experiments/` directory, that contains experiment meta information.

Make sure to remove this directory if you restart the experiment scheduler. Otherwise old experiments will be used for the following process.


### Fetch batch information

To create a compact representation of the executed experiments run the following program.

```
python3 ./src/create_csv.py
```

To fetch the experiment information the agency authentication information is requested again. This can also take some minutes.

The result of this program are two csv files located inside the `results/` directory.
Before the program is executed, these two csv files are already in the repository. They contain the results of previously executed experiments and will be overwritten.


### Plot the results

To create a plot showing the processing times of the batches execute the program

```
python3 ./src/plot_results.py
```

This will create the file `results/processing_times.pdf`.
