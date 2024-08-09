# Racing Items
## Folder Structure
 * infra_setup - Components for use with EC2 image builder.
 * reward_funcs - Definitions of reward functions.
 * utils - Helpers, currently includes a metadata (action space) generator.

## Infra_Setup
The general design principle has been to ensure the training is always
running, even if the spot instance gets interrupted, or if there are
other application failures.

Some scripts and config files saved here as a record of the EC2 image that
was created. The way this works is somewhat complicated, but basically the
image contains a cron job that runs upon every reboot. That cron job downloads
another script from the S3 bucket, which contains the commands to start
the training.

If the training fails or freezes there is another process that tries to
detect this by periodically checking the S3 bucket for updates. If the
bucket is not receiving the expected updates then assume the process
has failed, stop the current training run, restart the server, and begin
a new training run.

If the spot instance gets interrupted, which can happen at some arbitrary
time, then the cron job that runs on reboot will start a new training run.

## Reward_Funcs
Use reward functions from here as required. However, note that the Deepracer
training only supports Python version 3.8 so care should be taken to use
only version 3.8 compatible statements.

## Utils
Currently, this contains a helper function to generate the action space
consisting of speeds and steering angles. Those can be used as part of
the metadata.


## Setup
Using Poetry to manage Python dependencies. Install Poetry following the
instructions for your platform:
[https://python-poetry.org/](https://python-poetry.org/)

Install the dependencies into the Poetry environment:
```shell
poetry install --sync --no-root
```

## Running
Generally you should run via Poetry so that the dependencies will be loaded.
For example, to run a Python file:
```shell
poetry run python utils/generate_metadata.py
```
Or to start a local server so you can view Jupyter notebooks:
```shell
poetry run jupyter notebook
```
then browse to `http://localhost:8888` or whichever other url the output
messages point you towards.
