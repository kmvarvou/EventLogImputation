import pandas as pd
import pm4py
from sklearn.cluster import AgglomerativeClustering
from os import listdir
from os.path import isfile, join
import os
import numpy as np
import LevenDistance
from Levenshtein import distance as lev
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
            #print(f"Saved sub-log with trace length {trace_length} to {output_file_path}")


def main(input_file_name):
    script_dir = os.path.dirname(__file__)
    input_log_path = os.path.join(script_dir, "input", input_file_name)

    # Check if the input file exists
    if not os.path.exists(input_log_path):
        print(f"Error: The file {input_log_path} does not exist.")
        sys.exit(1)

    print(f"Reading event log from {input_log_path}")

    # Read the event log
    try:
        event_log = pm4py.read_xes(input_log_path, "iterparse", True)
    except Exception as e:
        print(f"Error reading event log: {e}")
        sys.exit(1)

    # Split the traces by their length
    traces_by_length = split_traces_by_length(event_log)

    # Create an output directory
    log_name = os.path.splitext(os.path.basename(input_log_path))[0]
    output_main_dir = os.path.join(script_dir, f"{log_name}_sublogs")
    os.makedirs(output_main_dir, exist_ok=True)

    save_sub_logs(traces_by_length, output_main_dir, log_name)


    path = output_main_dir
    input_file_clean_name = input_file_name.replace(".xes","")
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    output_path = script_dir + "/" + input_file_clean_name + "_cluster_variant_output/"
    os.umask(0)
    os.makedirs(output_path, 0o777, True)


    count_trace = 0
    for file in onlyfiles:

        log = pm4py.read_xes(path + "/" + file, "iterparse", True)
        log_length = len(log)
        if (log_length == 1):
            continue
        log_variants = pm4py.get_variants(log)

        if len(log_variants) == 1:

            pm4py.write_xes(log, output_path + file)
            count_trace += len(log)
            continue
        i = 0
        j = 0
        rows = log_length
        cols = log_length
        mat = [[0 for w in range(cols)] for e in range(rows)]
        for k in log:
            temp_k = pm4py.convert_to_dataframe(k)

            trace_k = temp_k['concept:name'].tolist()

            a = [trace_k]
            a = np.array(a)
            a.flatten()
            for l in log:
                temp_l = pm4py.convert_to_dataframe(l)
                trace_l = temp_l['concept:name'].tolist()

                b = [trace_l]
                b = np.array(b)
                b.flatten()
                s1, s2 = LevenDistance.leven_preprocess(list(a.flatten()), list(b.flatten()))
                temp_value = lev(s1, s2)
                mat[i][j] = temp_value
                j += 1
            i += 1
            j = 0
        log_df = pm4py.convert_to_dataframe(log)
        trace_length = log_df['case:variant:length']
        threshold = int(trace_length[0] * 0.3)
        if threshold == 0:
            threshold = 1

        agg = AgglomerativeClustering(n_clusters=None, metric='precomputed', linkage='average',
                                      distance_threshold=threshold)
        mat_df = pd.DataFrame(mat)
        w = 0
        res = all(isinstance(ele, list) for ele in mat)
        mat_df.astype(np.int64)
        mat_array = mat_df.to_numpy()
        labels = agg.fit_predict(mat)
        unique_labels = np.unique(labels)
        df = pd.DataFrame()
        for a in unique_labels:
            test_log = pm4py.objects.log.obj.EventLog()
            for x in range(log_length):
                if labels[x] == a:
                    test_log.append(log[x])

            temp_file = file
            temp_file2 = temp_file.replace(".xes", "")
            test_log_folder = temp_file2 + "_" + str(a)
            test_log_out = output_path + temp_file2 + "_" + str(a) + "/" + temp_file2 + "_" + str(
                a) + "_normal" + ".txt"
            #test_log_out2 = output_path + temp_file2 + "_" + str(a) + "/" + temp_file2 + "_" + str(
              #  a) + "_variants" + ".txt"

            if len(test_log) > 2:
                os.umask(0)
                os.makedirs(output_path + temp_file2 + "_" + str(a) + "/", 0o777, True)

                count_trace += len(test_log)
                test_log_df = pm4py.convert_to_dataframe(test_log)
                test_log_df['CompleteTimestamp'] = pd.to_datetime(test_log_df['time:timestamp'], utc=True)
                test_log_df['CompleteTimestamp'] = test_log_df['CompleteTimestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")
                test_log_df.to_csv(test_log_out)
                trace_length = test_log_df['case:variant:length']
                durations = test_log_df['duration_day'].to_numpy()
                start = 0
                end = len(durations)
                step = trace_length[0]
                durations_per_trace = []
                for p in range(start, end, step):
                    x = p
                    durations_per_trace.append(durations[x:x + step])
                output_array = np.array(durations_per_trace)
                output_array_transposed = output_array.transpose()
                np.savetxt(test_log_out, output_array_transposed)

                #output_array2 = np.array(list(set(test_log_df['case:concept:name'])))
                #np.savetxt(test_log_out2, output_array2, fmt='%s')




# Call the function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python LengthClustering.py <input_file_name>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    main(input_file_name)
