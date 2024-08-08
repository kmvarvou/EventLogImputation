import pm4py
import os
import sys


def split_traces_by_length(event_log):
    traces_by_length = {}
    for trace in event_log:
        trace_length = len(trace)
        if trace_length not in traces_by_length:
            traces_by_length[trace_length] = []
        traces_by_length[trace_length].append(trace)
    return traces_by_length


def save_sub_logs(traces_by_length, output_dir, log_name):
    for trace_length, traces in traces_by_length.items():
        if len(traces) > 0:
            sub_log = pm4py.objects.log.obj.EventLog()
            for trace in traces:
                sub_log.append(trace)
            output_file_path = os.path.join(output_dir, f"{log_name}_length_{trace_length}.xes")
            pm4py.write_xes(sub_log, output_file_path)
            print(f"Saved sub-log with trace length {trace_length} to {output_file_path}")

def extract_duration_values(traces):
    durations = []
    for trace in traces:
        trace_durations = []
        for event in trace:
            if 'duration_day' in event:
                trace_durations.append(event['duration_day'])
            else:
                trace_durations.append(0)  # Handle missing 'duration_day' values
        durations.append(trace_durations)
    return durations


def save_durations_to_txt(durations, output_dir, file_name):
    # Transpose the list of durations to align events by index
    transposed_durations = list(zip(*durations))

    # Create output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Prepare the output file path
    output_file_path = os.path.join(output_dir, f"{file_name}_normal.txt")

    # Write durations to the text file
    with open(output_file_path, 'w') as f:
        for line in transposed_durations:
            f.write(' '.join(map(str, line)) + '\n')

    #print(f"Saved durations to {output_file_path}")


def main(input_file_name):
    # Determine the path to the input log file
    script_dir = os.path.dirname(__file__)
    input_log_path = os.path.join(script_dir, "input", input_file_name)

    # Check if the input file exists
    if not os.path.exists(input_log_path):
        print(f"Error: The file {input_log_path} does not exist.")
        sys.exit(1)

    print(f"Reading event log from {input_log_path}")

    # Read the event log
    try:
        event_log = pm4py.read_xes(input_log_path,"iterparse",True)
    except Exception as e:
        print(f"Error reading event log: {e}")
        sys.exit(1)

    # Split the traces by their length
    traces_by_length = split_traces_by_length(event_log)

    # Create an output directory
    log_name = os.path.splitext(os.path.basename(input_log_path))[0]
    output_main_dir = os.path.join(script_dir, f"{log_name}_length_variant_output")
    os.makedirs(output_main_dir, exist_ok=True)

    # Save the sub-logs
    #save_sub_logs(traces_by_length, output_main_dir, log_name)

    for trace_length, traces in traces_by_length.items():
        if len(traces) > 2:
            # Extract durations
            durations = extract_duration_values(traces)

            # Define the sublog folder and file names
            sublog_folder = os.path.join(output_main_dir, f"{log_name}_length_{trace_length}")
            os.makedirs(sublog_folder, exist_ok=True)

            # Save durations to text file
            save_durations_to_txt(durations, sublog_folder, f"{log_name}_length_{trace_length}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python LogLengthExtraction.py <input_file_name>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    main(input_file_name)