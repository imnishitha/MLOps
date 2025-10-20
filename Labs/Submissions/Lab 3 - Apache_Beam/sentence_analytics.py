import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import urllib.request
import os
import re


# Download dataset
URL = "https://www.gutenberg.org/files/1342/1342-0.txt" 
LOCAL_FILE = "data/pride_prejudice.txt"
os.makedirs("data", exist_ok=True)

if not os.path.exists(LOCAL_FILE):
    print("Downloading dataset...")
    urllib.request.urlretrieve(URL, LOCAL_FILE)
    print("Download complete!")


# Helper functions
def normalize_text(line):
    return re.sub(r"[^a-zA-Z0-9\s\.!?]", "", line)

def split_sentences(line):
    return [s.strip() for s in re.split(r'[.!?]', line) if s.strip()]

def filter_short_sentences(sentence):
    return len(sentence.split()) > 5

def avg_word_length(sentence):
    words = sentence.split()
    return (sentence, sum(len(w) for w in words) / len(words))

def contains_names(sentence):
    # Check if sentence mentions Elizabeth or Darcy
    return 'Elizabeth' in sentence or 'Darcy' in sentence

def format_output(sentence, avg_len):
    return f"{sentence} (avg_word_length={avg_len:.2f})"


options = PipelineOptions([
    '--runner=DirectRunner'
])

with beam.Pipeline(options=options) as p:

    sentences = (
        p
        | "Read Text" >> beam.io.ReadFromText(LOCAL_FILE)
        | "Normalize Text" >> beam.Map(normalize_text)
        | "Split Sentences" >> beam.FlatMap(split_sentences)
        | "Filter Short Sentences" >> beam.Filter(filter_short_sentences)
    )

    # Compute average word length per sentence
    avg_lengths = sentences | "Compute Avg Word Length" >> beam.Map(avg_word_length)

    # Filter sentences mentioning main characters
    character_sentences = avg_lengths | "Filter by Names" >> beam.Filter(lambda s_avg: contains_names(s_avg[0]))

    # Format and write results
    formatted = character_sentences | "Format Output" >> beam.Map(lambda s_avg: format_output(s_avg[0], s_avg[1])) \
                                   | "Write Results" >> beam.io.WriteToText("output_sentences")

print("Pipeline finished. Output written to output_sentences-*")
