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

To query LLMs for Bayesian inference using BQA and COT methods , use the `main.py` script:
```bash
python main.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET] [--openaikey OPENAIKEY]
[--openaiorg OPENAIORG] [--method {BQA,COT}] [--samplenum SAMPLENUM]
[--models {gpt-3.5-turbo,gpt-4-0613,all}] [--maxattempt MAXATTEMPT] [--CLADDER]
```

- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder to save the results (default: "../datasets/")
- `--openaikey`: OpenAI API key
- `--openaiorg`: OpenAI organization key
- `--method`: Method to solve the problem (choices: "BQA", "COT", default: "BQA")
- `--samplenum`: Number of instances of the dataset to read (Max is 900)
- `--models`: Choose a model (choices: "gpt-3.5-turbo", "gpt-4-0613", "all", default: "all")
- `--maxattempt`: Max number of attempts after a failed prompt to OpenAI (default: 10)
- `--CLADDER`: Use CLADDER dataset (default: False)

This program saves every answer after each prompt. If it terminates, run it again, and it will pick up where it left off.

### Testing LLMs for Bayesian Inference


To test LLMs using BQA and COT, use the `test.py` script:
```bash
python test.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET]
[--models {gpt-3.5-turbo,gpt-4-0613,all}] [--CLADDER]
```
- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder that has saved the results (default: "../datasets/")
- `--models`: Choose a model (choices: "gpt-3.5-turbo", "gpt-4-0613", "all", default: "all")
- `--CLADDER`: Use CLADDER dataset (default: False)

## Dataset

The code uses a test dataset specified by the `--testdataset` argument. By default, it uses the "../datasets/Colored_1000_examples.csv" dataset. If the `--CLADDER` flag is set, it uses the "../datasets/CLADDER_test.csv" dataset instead.

## Models

The code supports running Bayesian inference with the following LLMs:
- GPT-3.5-turbo
- GPT-4-0613

You can specify the model(s) to use with the `--models` argument. By default, it runs inference with both models one after the other.

## Output

The results of running Bayesian inference are saved in the dataset folder specified by the `--outputdataset` argument. The output files are named based on the arguments set in `main.py`.

## Our Results

Here are our results using these methods detailed in the paper.
| Model | Method | V2 | V3 | V4 | V5 | V6 | V7 | V8 | V9 | V10 | V2-5 | V6-10 | V2-10 |
|-------|--------|----|----|----|----|----|----|----|----|-----|------|-------|------|
| **GPT3.5** | BQA ZS | 33 | 13 | 5 | 4 | 6 | 2 | 3 | 1 | 2 | 13 | 2 | 7 |
| | BQA FS | 3 | 0 | 1 | 1 | 2 | 2 | 1 | 1 | 0 | 1 | 1 | 1 |
| | COT ZS | 53 | 8 | 4 | 5 | 10 | 5 | 2 | 2 | 0 | 17 | 3 | 9 |
| | COT FS | 52 | 23 | 12 | 5 | 8 | 4 | 1 | 4 | 2 | 23 | 3 | 12 |
| **GPT4** | BQA ZS | 80 | 10 | 15 | 10 | 20 | 0 | 15 | 10 | 5 | 28 | 10 | 18 |
| | BQA FS | 75 | 10 | 30 | 25 | 35 | 15 | 5 | 5 | 0 | 35 | 12 | 22 |
| | COT ZS | 90 | 45 | 50 | 35 | 30 | 15 | 20 | 5 | 5 | 55 | 15 | 32 |
| | COT FS | 100 | 60 | 50 | 35 | 30 | 15 | 20 | 5 | 5 | 61 | 15 | 35 |

**Table**: GPT3.5 and GPT4 results for BQA and COT methods. The columns show the variable size of the tested dataset, while the rows show the prompting methods that are either BQA or COT. These methods are tested with zero-shot (ZS) and few-shot (FS) settings. The last three columns show the average accuracies over the $V_i$s.

