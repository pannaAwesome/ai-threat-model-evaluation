from stats.compare_human_ai import *
from stats.compare_self import *
from stats.files import *

import json

application = "fake"
tool = "fake"
actual_threats = 3
tool_threats = 5
iterations = 5
stats_folder = f"stats/{tool}"
reset_stats_folder(stats_folder)

threat_files = get_threat_files(f"results/{application}", f"{tool}_reverse")
hallucination_files = get_hallucination_files(f"results/{application}", tool)

hallucinations = []
for file in hallucination_files:
    kappa = hallucinations_compare_human_ai(f"human_evaluation/{tool}/hallucinations.csv", file, actual_threats*tool_threats)
    hallucinations.append(kappa)

with open(f"{stats_folder}/human_ai_hallucinations.json", "w") as f:
    json.dump(hallucinations, f, indent=4)

threats = []
for file in threat_files:
    kappa = threat_compare_human_ai(f"human_evaluation/{tool}/threats.csv", file, 57*13)
    threats.append(kappa)

with open(f"{stats_folder}/human_ai_threats.json", "w") as f:
    json.dump(threats, f, indent=4)
    
files = read_threat_reverse_pairs(f"results/{application}")

reverse = []
for model, df1, df2 in files:
    kappa = threats_ai_position_bias(model, df1, df2, tool_threats*actual_threats*iterations)
    reverse.append(kappa)
    
with open(f"{stats_folder}/position_bias.json", "w") as f:
    json.dump(reverse, f, indent=4)
    
repetition = []
possible_ids = range(tool_threats*actual_threats)
for file in threat_files:
    kappa = threats_ai_repetition(file, possible_ids)
    repetition.append(kappa)
    
with open(f"{stats_folder}/stability.json", "w") as f:
    json.dump(repetition, f, indent=4)