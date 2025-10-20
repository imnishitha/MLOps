# Apache Beam Pipeline – Sentence Analytics

## Overview

This Apache Beam project demonstrates a **longer pipeline** that reads an online text dataset, processes sentences, computes metrics, and filters sentences of interest.  

The pipeline is implemented using **Apache Beam Python SDK** and runs locally using the **DirectRunner**.

### Features

- Reads online dataset: *Pride and Prejudice* by Jane Austen  
- Cleans and normalizes text  
- Splits text into sentences  
- Filters out short sentences (< 5 words)  
- Computes **average word length per sentence**  
- Extracts sentences containing **“Elizabeth”** or **“Darcy”**  
- Writes formatted results to output files  


## Requirements

- Python 3.7+  
- Apache Beam Python SDK  

Install dependencies:

```bash
pip install apache-beam
```

## Files

- web_logs_analytics.py – Main Beam pipeline
- data/ – Folder for downloaded dataset
- output_sentences-* – Pipeline output

## How to Run
- Clone or download the repository
- Make sure you are in the project directory

## Run the pipeline:
- python web_logs_analytics.py

## After completion, check output files:
- ls output_sentences-*
- head -n 20 output_sentences-00000-of-00001

## Example Output
Elizabeth was determined to be happy. (avg_word_length=5.40)
Darcy was proud but honorable. (avg_word_length=5.20)
...

## Notes
- The pipeline uses a local DirectRunner, safe to run on macOS.
- The dataset is downloaded automatically from Project Gutenberg if not already present.
- Pipeline demonstrates map, filter, flatMap, and transformations beyond simple counting.