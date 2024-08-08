import os
import pm4py
import sys
from collections import defaultdict


def read_xes_log(file_path):
    return pm4py.read_xes(file_path,"iterparse",True)


def get_trace_variants(log):
    variants = pm4py.get_variants(log)
    return variants


def extract_duration_days(traces):
    trace_durations = []
    max_length = 0
    for trace in traces:
        durations = [event['duration_day'] for event in trace if 'duration_day' in event]
        trace_durations.append(durations)
        max_length = max(max_length, len(durations))

    # Normalize the lengths by padding with None (or some placeholder)
    for durations in trace_durations:
        while len(durations) < max_length:
            durations.append(None)  # You can use a different placeholder if necessary

    return trace_durations


def save_to_txt(folder, file_prefix, variant_index, trace_durations):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{file_prefix}_trace_variant_{variant_index}_normal.txt")
    with open(file_path, 'w') as file:
        for row in zip(*trace_durations):
            file.write(' '.join(str(value) if value is not None else '' for value in row) + '\n')


def main(input_file_name):
    # Define the input folder and log file path
    script_directory = os.path.dirname(os.path.abspath(__file__))

    input_folder = os.path.join(script_directory, "input")
    input_file_path = os.path.join(input_folder, input_file_name)

    # Read the XES log
    log = read_xes_log(input_file_path)

    # Get the trace variants
    variants = get_trace_variants(log)

    # Create the main folder for output

    base_folder_name = os.path.splitext(input_file_name)[0] + "_trace_variant_output"

    base_folder = os.path.join(script_directory, base_folder_name)
    os.makedirs(base_folder,exist_ok=True)

    # Process each variant
    for variant_index, (variant, traces) in enumerate(variants.items()):
        if len(traces) >= 3:
            trace_durations = extract_duration_days(traces)
            if trace_durations:
                sub_folder_name = f"{os.path.splitext(input_file_name)[0]}_trace_variant_{variant_index}"
                folder = os.path.join(base_folder, sub_folder_name)
                save_to_txt(folder, os.path.splitext(input_file_name)[0], variant_index, trace_durations)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python LogVariantExtraction.py <input_log_file.xes>")
    else:
        input_file_name = sys.argv[1]
        main(input_file_name)
