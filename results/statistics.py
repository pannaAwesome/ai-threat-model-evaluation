import math 

def cohens_kappa(rater1_labels, rater2_labels, labels):
    total = len(rater1_labels)
    agree = 0
    rater1_total = {key: 0 for key in labels}
    rater2_total = {key: 0 for key in labels}
    for label1, label2 in zip(rater1_labels, rater2_labels):
        if label1 == label2:
            agree += 1
        rater1_total[label1] += 1
        rater2_total[label2] += 1
    
    p_observed = agree/total
    
    p_expected = 0
    for label in labels:
        p_expected += (rater1_total[label] / total) * (rater2_total[label] / total)
    
    k = (p_observed - p_expected) / (1 - p_expected)
    se = _standard_error_ck(p_observed, p_expected, total)
    min_ck, max_ck = _confidence_interval_ck(k, se)
    
    return {
        "kappa": k,
        "meaning": translate_kappas(k),
        "SE": se,
        "min CI": min_ck,
        "max CI": max_ck
    }

def _standard_error_ck(p_observed, p_expected, no_subjects):
    return math.sqrt((p_observed (1 - p_observed)) / (no_subjects (1 - p_expected) **2))

def _confidence_interval_ck(k, se):
    return k - 1.96 * se, k + 1.96 * se

def fleiss_kappa(raters_labels:list, labels:list):
    m = len(raters_labels) # number of judges
    n = len(raters_labels[0]) # number of subjects
    
    p_expected = 0
    all_raters_labels = [rater_labels for sublist in raters_labels for rater_labels in sublist]
    raters_total = len(all_raters_labels)
    for label in labels:
        sum_label = sum(1 if rater_label == label else 0 for rater_label in all_raters_labels)
        p_expected += (sum_label / raters_total) ** 2

    label_subjects = [[0] * n] * len(labels)
    for rater_labels in raters_labels:
        for idx, rating in enumerate(rater_labels):
            idx_label = labels.index(rating)
            label_subjects[idx_label][idx] += 1
            
    label_sum = sum(no_ratings ** 2 for sublist in label_subjects for no_ratings in sublist)
        
    p_observed = (1 / (n * m * (m - 1))) * (label_sum - n * m)
    
    return (p_observed - p_expected) / (1 - p_expected)

def translate_kappas(k):
    if k > 0.8:
        return "Almost Perfect"
    elif k > 0.6:
        return "Substantial"
    elif k > 0.4:
        return "Moderate"
    elif k > 0.2:
        return "Fair"
    elif k > 0:
        return "Slight"
    else:
        return "No Agreement"