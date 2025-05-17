from collections import Counter
import numpy as np

def count_based_confusion_matrix(true_ids, pred_ids, total):
    true_counts = Counter(true_ids)
    pred_counts = Counter(pred_ids)
    
    all_ids = set(true_counts.keys()) | set(pred_counts.keys())
    
    TP = 0
    FP = 0
    FN = 0
    
    for id_ in all_ids:
        t = true_counts.get(id_, 0)
        p = pred_counts.get(id_, 0)
        
        TP += min(t, p)       
        FN += max(t - p, 0)   
        FP += max(p - t, 0)   
    
    TN = total - (TP + FP + FN)
    if TN < 0:
        raise ValueError("Total is too small for given TP, FP, FN counts.")
    
    confusion = {
        "True Positive": TP,
        "False Positive": FP,
        "False Negative": FN,
        "True Negative": TN
    }
    
    return confusion

def cohens_kappa(confusion, total):
    TP = confusion['True Positive']
    FP = confusion['False Positive']
    FN = confusion['False Negative']
    TN = confusion['True Negative']
    
    p_o = (TP + TN) / total
    
    p_yes_true = (TP + FN) / total
    p_yes_pred = (TP + FP) / total
    p_no_true = (FN + TN) / total
    p_no_pred = (FP + TN) / total
    
    p_e = p_yes_true * p_yes_pred + p_no_true * p_no_pred
    
    if p_e == 1:
        return 1.0  # perfect agreement
    
    kappa = (p_o - p_e) / (1 - p_e)
    return kappa


def build_ratings_matrix_with_universe(evaluators_lists, all_items):
    """
    evaluators_lists: list of lists of IDs (found by each evaluator)
    all_items: list or set of all possible IDs (the universe)
    
    Returns:
        ratings_matrix: numpy array of shape (num_items, 2)
                        Column 0 = raters NOT finding the ID
                        Column 1 = raters finding the ID
        items: list of all_items in sorted order (row order)
    """
    M = len(evaluators_lists)
    all_items = sorted(all_items)
    
    ratings = []
    for item in all_items:
        found_count = sum(item in evaluator for evaluator in evaluators_lists)
        not_found_count = M - found_count
        ratings.append([not_found_count, found_count])
        
    ratings_matrix = np.array(ratings)
    return ratings_matrix, all_items

def fleiss_kappa(ratings_matrix):
    """
    ratings_matrix: numpy array of shape (N, k)
    N = number of items
    k = number of categories
    Each row sums to n = number of raters per item
    """
    N, k = ratings_matrix.shape
    n = ratings_matrix[0].sum()
    
    # 1. Compute P_i for each item
    P = (np.sum(ratings_matrix * (ratings_matrix - 1), axis=1)) / (n * (n - 1))
    
    # 2. Mean agreement
    P_bar = np.mean(P)
    
    # 3. Category proportions
    p = np.sum(ratings_matrix, axis=0) / (N * n)
    
    # 4. Expected agreement
    P_e = np.sum(p ** 2)
    
    # 5. Fleiss kappa
    kappa = (P_bar - P_e) / (1 - P_e)
    return kappa