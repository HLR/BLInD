# Probabilistic Reasoning in Generative Large Language Models

This repository is dedicated to the research and findings presented in the paper "Probabilistic Reasoning in Generative Large Language Models." Our study introduces the Bayesian Linguistic Inference Dataset (BLInD) and delves into the capabilities and limitations of Large Language Models (LLMs) in executing probabilistic reasoning with explicitly quantified uncertainties.

## Dataset Overview

The BLInD dataset is crafted to evaluate the probabilistic reasoning skills of LLMs, featuring:
- A foundational Bayesian Network for each instance.
- A textual description detailing the structure of the Bayesian Network.
- Probabilistic queries posed in natural language.
- Precise answers corresponding to these queries.

This dataset is produced through a systematic pipeline that constructs Bayesian Networks, populates Conditional Probability Tables (CPTs), formulates queries, and translates all components into natural language. The dataset files and the Python scripts used for generation are available in the [datasets directory](./datasets/).

## Methodological Approaches

Our paper investigates various methodologies to assess and enhance the probabilistic reasoning of LLMs:

1. **Baselines**:
   - [Basic Question Answering (BQA)](./BQAandCOT/)
   - [Chain of Thought (COT)](./BQAandCOT/)
2. **Subtasks**:
   - [Number Extraction (NE)](./NE/)
   - [Graph Generation (GG)](./GG/)
3. **Symbolic Computations**:
   - [Python code (PAL - Program Aided Language Models)](./PALandMC/)
   - [Monte Carlo algorithms (MC)](./PALandMC/)
   - [ProbLog](./Problog/).

## Repository Structure

- `datasets/`: Hosts the BLInD dataset and the Python scripts for its creation.
- `BQAandCOT/`: Contains scripts for testing BLInD with BQA and COT methodologies.
- `PALandMC/`: Includes scripts for employing PAL and MC techniques on BLInD.
- `Problog/`: Features scripts for applying ProbLog on BLInD.
- `NE/`: Provides scripts for the Number Extraction subtask.
- `GG/`: Offers scripts for the Graph Generation subtask.

## Dependencies

Ensure you have the following Python version and packages installed:
- Python 3.10.6
- openai 1.6.1
- problog 2.2.4
- pandas
- pgmpy
- networkx
- numpy

## Citation

To cite our work, please use the following BibTeX entry:

```bibtex
@misc{nafar2024probabilistic,
      title={Probabilistic Reasoning in Generative Large Language Models},
      author={Aliakbar Nafar and Kristen Brent Venable and Parisa Kordjamshidi},
      year={2024},
      eprint={2402.09614},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}