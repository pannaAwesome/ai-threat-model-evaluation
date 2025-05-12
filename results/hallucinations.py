import os
import csv

import pandas as pd

from glob import glob
from results.statistics import cohens_kappa, fleiss_kappa
from results.utils import *

def apply_cohens_kappa(result_series, full_set):
    pass

def individual_human(folder_path, combined_df, human_truth, idxs_ai_tm):
    # For categories
    categories_ai_human = []
    for file, ai, idxs in zip(combined_df["file"], combined_df["model"], combined_df["categories_ids"]):
        ai_truth = make_truth_labels(idxs, idxs_ai_tm)
        ck = cohens_kappa(ai_truth, human_truth, [0, 1])
        ck["file"] = file
        ck["model"] = ai
        categories_ai_human.append(ck)
    save_results(folder_path, categories_ai_human, "categories_individual")
    
    df_categories_ai_human = pd.DataFrame.from_dict(categories_ai_human)
    grouped_categories = df_categories_ai_human.groupby("model")["kappa"].agg(
        max_kappa="max",
        min_kappa="min",
        mean_kappa="mean"
    ).reset_index()
    grouped_categories.to_csv(f"{folder_path}/aggregated_categories_individual")
    
    # For assets
    assets_ai_human = []
    for file, ai, idxs in zip(combined_df["file"], combined_df["model"], combined_df["asset_ids"]):
        ai_truth = make_truth_labels(idxs, idxs_ai_tm)
        ck = cohens_kappa(ai_truth, human_truth, [0, 1])
        ck["file"] = file
        ck["model"] = ai
        assets_ai_human.append(ck)
    save_results(folder_path, assets_ai_human, "assets_individual")
    
    df_assets_ai_human = pd.DataFrame.from_dict(assets_ai_human)
    grouped_assets = df_assets_ai_human.groupby("model")["kappa"].agg(
        max_kappa="max",
        min_kappa="min",
        mean_kappa="mean"
    ).reset_index()
    grouped_assets.to_csv(f"{folder_path}/aggregated_categories_individual")

def hallucinations(folder_path: str, tool: str, ai_tm, human_truth=None):
    idxs_ai_tm = [threat["ID"] for threat in ai_tm]
    
    hallucination_files = list(glob(os.path.join(folder_path, f"{tool}*hallucinations*.csv")))
    combined_df = read_files_to_dataframe(hallucination_files)
    
    if human_truth:
        # Compare each individual AI's result with a human evaluator
        human_truth = make_truth_labels(human_truth, idxs_ai_tm)
        individual_human(folder_path, combined_df, human_truth, idxs_ai_tm)
    
    # # Compare AI with itself
    # if combined_df["file"].nunique() == 2:
    #     # We use Cohen Kappa for interrelation
        