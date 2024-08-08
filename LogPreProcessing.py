import os
import pm4py
import argparse
import subprocess
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime


# Function to calculate the length of each trace and add durations to each event
def calculate_trace_lengths_and_durations(event_log):
    for trace in event_log:
        trace_length = len(trace)
        trace.attributes['variant:length'] = trace_length

        # Calculate duration for each event
        for i, event in enumerate(trace):
            if i == 0:
                event['duration_day'] = 0
            else:
                timestamp_prev = trace[i - 1]['time:timestamp']
                timestamp_curr = event['time:timestamp']
                duration = (timestamp_curr - timestamp_prev).days
                event['duration_day'] = duration


# Main function to handle the workflow
def main(log_file_name):
    # Define the input folder path
    input_folder = os.path.join(os.path.dirname(__file__), 'input')

    # Path to the XES file in the input folder
    xes_file_path = os.path.join(input_folder, log_file_name)

    # Read the XES file
    event_log = xes_importer.apply(xes_file_path)

    # Calculate trace lengths and event durations
    calculate_trace_lengths_and_durations(event_log)

    # Save the modified log back to the same XES file
    pm4py.write_xes(event_log, xes_file_path)

    print(f"Trace lengths and event durations calculated and saved to '{xes_file_path}'.")
    return xes_file_path


# Function to call the appropriate preprocessing script
def call_preprocessing_script(preprocessed_file, flavor):
    script_map = {
        'trace_based': 'LogVariantExtraction.py',
        'cluster_based': 'LengthClustering.py',
        'length_based': 'LogLengthExtraction.py'
    }

    script_name = script_map.get(flavor)

    if script_name:
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        subprocess.run(['python', script_path, preprocessed_file], check=True)
    else:
        raise ValueError(f"Invalid preprocessing flavor: {flavor}")


if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Process an XES log file and add trace lengths and event durations.")
    parser.add_argument("log_file_name", type=str, help="The name of the XES log file in the input folder")
    parser.add_argument("preprocessing_flavor", type=str, choices=['trace_based', 'cluster_based', 'length_based'],
                        help="The preprocessing flavor to apply")
    args = parser.parse_args()

    # Call the main function with the provided log file name
    main(args.log_file_name)

    # Call the appropriate preprocessing script
    call_preprocessing_script(args.log_file_name, args.preprocessing_flavor)
