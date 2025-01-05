# Bayesian Inference with Large Language Models Using BQA and COT Methods

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
cd BQAandCOT
```

## Usage

To query LLMs for Bayesian inference using BQA and COT methods, use the `main.py` script:
```bash
python main.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET] [--openaikey OPENAIKEY]
[--openaiorg OPENAIORG] [--replicatekey REPLICATEKEY] [--method {BQA,COT}] [--samplenum SAMPLENUM]
[--models MODEL [MODEL ...]] [--maxattempt MAXATTEMPT] [--CLADDER]
```

### Arguments

- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder to save the results (default: "../datasets/")
- `--openaikey`: OpenAI API key
- `--openaiorg`: OpenAI organization key
- `--replicatekey`: Replicate.ai API key (required for non-GPT models)
- `--method`: Method to solve the problem (choices: "BQA", "COT", default: "BQA")
- `--samplenum`: Number of instances of the dataset to read (default: 2)
- `--models`: Choose one or more models (choices: "gpt-3.5-turbo", "gpt-4-0613", "meta/meta-llama-3-70b-instruct", "mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat")
- `--maxattempt`: Max number of attempts after a failed prompt to OpenAI (default: 10)
- `--CLADDER`: Use CLADDER dataset (default: False)

**Note:** For non-GPT models (Llama, Mistral), you need to provide a Replicate.ai API key using the `--replicatekey` argument.

This program saves every answer after each prompt. If it terminates, run it again, and it will pick up where it left off.

### Testing LLMs for Bayesian Inference

To test LLMs using BQA and COT, use the `test.py` script:
```bash
python test.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET]
[--models MODEL [MODEL ...]] [--CLADDER]
```
- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder that has saved the results (default: "../datasets/")
- `--models`: Choose one or more models (same choices as main.py)
- `--CLADDER`: Use CLADDER dataset (default: False)

## Dataset

The code uses a test dataset specified by the `--testdataset` argument. By default, it uses the "../datasets/Colored_1000_examples.csv" dataset. If the `--CLADDER` flag is set, it uses the "../datasets/CLADDER_test.csv" dataset instead.

## Models

The code supports running Bayesian inference with the following LLMs:
- GPT-3.5-turbo
- GPT-4-0613
- Meta Llama 3 70B Instruct
- Mistral 7B Instruct v0.2
- Llama 2 70B Chat

You can specify one or more models to use with the `--models` argument.

## Output

The results of running Bayesian inference are saved in the dataset folder specified by the `--outputdataset` argument. The output files are named based on the arguments set in `main.py`.
