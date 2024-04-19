# Bayesian Inference with Large Language Models Using ProbLog Method

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
cd Problog
```

## Usage

To query LLMs for Bayesian inference, use the `main.py` script:
```bash
python main.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET] [--openaikey OPENAIKEY]
[--openaiorg OPENAIORG] [--samplenum SAMPLENUM]
[--models {gpt-3.5-turbo-0613,gpt-4-0613,all}] [--maxattempt MAXATTEMPT] [--CLADDER]
```

- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder to save the results (default: "../datasets/")
- `--openaikey`: OpenAI API key
- `--openaiorg`: OpenAI organization key
- `--samplenum`: Number of instances of the dataset to read (Max is 900)
- `--models`: Choose a model (choices: "gpt-3.5-turbo-0613", "gpt-4-0613", "all", default: "all")
- `--maxattempt`: Max number of attempts after a failed prompt to OpenAI (default: 10)
- `--CLADDER`: Use CLADDER dataset (default: False)

This program saves every answer after each prompt. If it terminates, run it again, and it will pick up where it left off. The program by default test each method with and without NE and GG and saves their results separately.

### Testing LLMs for Bayesian Inference


To test LLMs using ProbLog method, use the `test.py` script:
```bash
python test.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET]
[--models {gpt-3.5-turbo-0613,gpt-4-0613,all}] [--CLADDER]
```
- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder that has saved the results (default: "../datasets/")
- `--models`: Choose a model (choices: "gpt-3.5-turbo-0613", "gpt-4-0613", "all", default: "all")
- `--CLADDER`: Use CLADDER dataset (default: False)

## Dataset

The code uses a test dataset specified by the `--testdataset` argument. By default, it uses the "../datasets/Colored_1000_examples.csv" dataset. If the `--CLADDER` flag is set, it uses the "../datasets/CLADDER_test.csv" dataset instead.

## Models

The code supports running Bayesian inference with the following LLMs:
- GPT-3.5-turbo-0613
- GPT-4-0613

You can specify the model(s) to use with the `--models` argument. By default, it runs inference with both models one after the other.

## Output

The results of running Bayesian inference are saved in the dataset folder specified by the `--outputdataset` argument. The output files are named based on the method, model name, and whether few-shot learning is used.

## Our Results

Here are our results using these methods detailed in the paper.

| Model | Method   | V2 | V3 | V4 | V5 | V6 | V7 | V8 | V9 | V10 | V2-5 | V6-10 | V2-10 |
|-------|----------|----|----|----|----|----|----|----|----|-----|------|-------|------|
|  **GPT3.5**    | ProbLog   | 87 | 82 | 88 | 75 | 59 | 52 | 46 | 38 | 35  | 83   | 46    | 62   |
|  **GPT4**     | ProbLog   | 95 | 100| 100| 95 | 100| 95 | 100| 95 | 100 | 97   | 98    | 97   |

**Table**: GPT3.5 and GPT4 results for the ProbLog method. The last three columns show the average accuracies over the dataset splits.

