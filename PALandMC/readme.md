# Bayesian Inference with Large Language Models Using PAL and MC

## Important Update

**Note:** The `gpt-3.5-turbo-0613` model is deprecated and replaced with `gpt-3.5-turbo`. Consequently, results obtained using `gpt-3.5-turbo` may differ from those reported in earlier experiments using `gpt-3.5-turbo-0613`.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HLR/BLInD.git
cd BLInD
```
2. Install the required dependencies:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
cd PALandMC
```

## Usage

To query LLMs for Bayesian inference using PAL and MC methods, use the `main.py` script:
```bash
python main.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET] 
[--openaikey OPENAIKEY] [--openaiorg OPENAIORG] [--replicatekey REPLICATEKEY]
[--method {PAL,MC}] [--samplenum SAMPLENUM] 
[--models MODEL [MODEL ...]] [--maxattempt MAXATTEMPT] [--CLADDER]
```

### Arguments

- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder to save the results (default: "../datasets/")
- `--openaikey`: OpenAI API key
- `--openaiorg`: OpenAI organization key
- `--replicatekey`: Replicate.ai API key (required for non-GPT models)
- `--method`: Method to solve the problem (choices: "PAL", "MC", default: "PAL")
- `--samplenum`: Number of instances of the dataset to read (default: 2000)
- `--models`: Choose one or more models from:
  - gpt-3.5-turbo
  - gpt-4-0613
  - meta/meta-llama-3-70b-instruct
  - mistralai/mistral-7b-instruct-v0.2
  - meta/llama-2-70b-chat
- `--maxattempt`: Max number of attempts after a failed prompt (default: 10)
- `--CLADDER`: Use CLADDER dataset (default: False)

**Note:** For non-GPT models (Llama, Mistral), you need to provide a Replicate.ai API key using the `--replicatekey` argument.

This program saves every answer after each prompt. If it terminates, run it again, and it will pick up where it left off. The program by default tests each method with and without NE and GG and saves their results separately.

### Testing LLMs for Bayesian Inference

To test LLMs using PAL and MC methods, use the `test.py` script:
```bash
python test.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET]
[--models MODEL [MODEL ...]] [--method {PAL,MC}] [--CLADDER]
```

- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder that has saved the results (default: "../datasets/")
- `--models`: Choose one or more models (same choices as main.py)
- `--method`: Method to test (choices: "PAL", "MC", default: "PAL")
- `--CLADDER`: Use CLADDER dataset (default: False)

## Dataset

The code uses a test dataset specified by the `--testdataset` argument. By default, it uses the "../datasets/Colored_1000_examples.csv" dataset. If the `--CLADDER` flag is set, it uses the "../datasets/CLADDER_test.csv" dataset instead.

## Models

The code supports running Bayesian inference with multiple LLMs:

- gpt-3.5-turbo
- gpt-4-0613
- meta/meta-llama-3-70b-instruct
- mistralai/mistral-7b-instruct-v0.2
- meta/llama-2-70b-chat

You can specify one or more models using the `--models` argument. For non-GPT models, make sure to provide your Replicate.ai API key.

## Output

The results of running Bayesian inference are saved in the dataset folder specified by the `--outputdataset` argument. The output files are named based on the arguments set in `main.py`.
