# Number Extraction with Large Language Models (NE Subtask)

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
cd GG
```

## Usage

To query LLMs for GG, use the `main.py` script:
```bash
python main.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET] [--openaikey OPENAIKEY]
[--openaiorg OPENAIORG] [--samplenum SAMPLENUM]
[--models {gpt-3.5-turbo,gpt-4-0613,all}] [--maxattempt MAXATTEMPT] [--reversed]
```

- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder to save the results (default: "../datasets/")
- `--openaikey`: OpenAI API key
- `--openaiorg`: OpenAI organization key
- `--samplenum`: Number of instances of the dataset to read (Max is 900)
- `--models`: Choose a model (choices: "gpt-3.5-turbo", "gpt-4-0613", "all", default: "all")
- `--maxattempt`: Max number of attempts after a failed prompt to OpenAI (default: 10)
- `--reversed`: Whether to reverse the order of operations by including the graph first. (default: False)

This program saves every answer after each prompt. If it terminates, run it again, and it will pick up where it left off. This code also tries different combinations of NE and GG together.

### Testing LLMs for Bayesian Inference

To test LLMs for GG, use the `test.py` script:
```bash
python test.py [--testdataset TESTDATASET] [--outputdataset OUTPUTDATASET]
[--models {gpt-3.5-turbo,gpt-4-0613,all}] [--reversed]
```

- `--testdataset`: Input test dataset (default: "../datasets/Colored_1000_examples.csv")
- `--outputdataset`: Dataset folder that has saved the results (default: "../datasets/")
- `--models`: Choose a model (choices: "gpt-3.5-turbo", "gpt-4-0613", "all", default: "all")
- `--reversed`: Whether to reverse the order of operations by including the graph first. (default: False)

  
## Dataset

The code uses a test dataset specified by the `--testdataset` argument. By default, it uses the "../datasets/Colored_1000_examples.csv" dataset.

## Models

The code supports running Bayesian inference with the following LLMs:
- gpt-3.5-turbo
- GPT-4-0613

You can specify the model(s) to use with the `--models` argument. By default, it runs inference with both models one after the other.

## Output

The results of running Bayesian inference are saved in the dataset folder specified by the `--outputdataset` argument. The output files are named based on the arguments set in `main.py`.

## Our Results

### GPT3.5

Here are our results for GPT3.5 using GG detailed in the paper.

| Criteria | Method      | V2  | V3  | V4  | V5  | V6  | V7  | V8  | V9  | V10 |
|----------|-------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| NE       | NE          | 100 | 100 | 100 | 100 | 96  | 95  | 98  | 94  | 94  |
| GG       | GG          | 100 | 95  | 92  | 93  | 84  | 75  | 79  | 73  | 78  |
| NE       | NE then GG  | 100 | 100 | 100 | 100 | 97  | 95  | 95  | 94  | 95  |
| GG       | NE then GG  | 100 | 100 | 99  | 96  | 92  | 87  | 78  | 70  | 76  |
| NE       | GG then NE  | 100 | 98  | 99  | 98  | 98  | 95  | 95  | 89  | 84  |
| GG       | GG and NE   | 100 | 97  | 100 | 96  | 92  | 87  | 87  | 77  | 82  |

**Table**: GG and NE subtask accuracies in isolation and then combined together. 

### GPT4

GPT4 achived 100% in all dataset splits.


