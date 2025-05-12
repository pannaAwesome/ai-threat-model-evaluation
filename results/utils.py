import csv

import pandas as pd

def make_truth_labels(results, full_set):
    return [1 if idx in results else 0 for idx in full_set]

def extract_ids_from_tuples(results_tuples:list, tuple_idx) -> list:
    return [pair[tuple_idx] for pair in results_tuples]

def read_files_to_dataframe(files):
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        df["file"] = file
        dfs.append(df)
    
    return pd.concat(dfs)

def save_results(result_folder, results, prefix=""):
    for metric,result in results.items():
        with open(f"{result_folder}/{prefix}_{metric}.csv", "w", newline='', encoding='utf-8') as csvfile:
            fieldnames = result[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(result)