from stats.compare_human_ai import *
from stats.compare_self import *
from stats.compare_other import *
from stats.files import *

import json

# MQ 13 S: 17 I: 57 T: 33
# WA 50 S: 17 I: 19 T: 14
# IO 12 S: 17 I: 87 T: 54

experiments = [
    {
        "name": "fake",
        "threats": 3,
        "human_eval": True,
        "tools": [{"name":"fake", "threats": 5}]
    },
    {
        "name": "message_queue_app",
        "threats": 13,
        "human_eval": True,
        "tools": [
            {
                "name": "stridegpt",
                "threats": 17 
            },
            {
                "name": "iriusrisk",
                "threats": 57
            },
            {
                "name": "threatcanvas",
                "threats": 33
            }
        ]
    },
    {
        "name": "web_app",
        "threats": 50,
        "human_eval": False,
        "tools": [
            {
                "name": "stridegpt",
                "threats": 17 
            },
            {
                "name": "iriusrisk",
                "threats": 19
            },
            {
                "name": "threatcanvas",
                "threats": 14
            }
        ]
    },
    {
    "name": "iot",
    "threats": 12,
    "human_eval": False,
    "tools": [
        {
            "name": "stridegpt",
            "threats": 17
        },
        {
            "name": "iriusrisk",
            "threats": 87
        },
        {
            "name": "threatcanvas",
            "threats": 54
        }
    ]
}
]

for experiment in experiments:
    application = experiment["name"]
    actual_threats = experiment["threats"]
    iterations = 10
    
    for tool_experiment in experiment["tools"]:
        tool = tool_experiment["name"]
        tool_threats = tool_experiment["threats"]

        threat_files = get_threat_files(f"results/{application}", f"{tool}")
        hallucination_files = get_hallucination_files(f"results/{application}", tool)
        
        if len(threat_files) > 0 and len(hallucination_files) > 0:
            stats_folder = f"stats/{tool}_{application}"
            reset_stats_folder(stats_folder)

            ######################### HUMAN & AI #########################
            ### Hallucinations
            if experiment["human_eval"]:
                hallucinations = []
                for file in hallucination_files:
                    kappa = hallucinations_compare_human_ai(f"human_evaluation/{tool}/hallucinations.csv", file, actual_threats*tool_threats)
                    hallucinations.append(kappa)

                with open(f"{stats_folder}/human_ai_hallucinations.json", "w") as f:
                    json.dump(hallucinations, f, indent=4)

                ### Threats
                threats = []
                for file in threat_files:
                    kappa = threat_compare_human_ai(f"human_evaluation/{tool}/threats.csv", file, 57*13)
                    threats.append(kappa)

                with open(f"{stats_folder}/human_ai_threats.json", "w") as f:
                    json.dump(threats, f, indent=4)

            ######################### POSITION BIAS #########################
            files = read_threat_reverse_pairs(f"results/{application}", tool)

            reverse = []
            for model, df1, df2 in files:
                kappa = threats_ai_position_bias(model, df1, df2, tool_threats*actual_threats*iterations)
                reverse.append(kappa)
                
            with open(f"{stats_folder}/position_bias.json", "w") as f:
                json.dump(reverse, f, indent=4)

            ######################### REPETITION STABILITY #########################
            repetition = []
            possible_ids = range(tool_threats*actual_threats)
            for file in threat_files:
                kappa = threats_ai_repetition(file, possible_ids)
                repetition.append(kappa)
                
            with open(f"{stats_folder}/stability_threats.json", "w") as f:
                json.dump(repetition, f, indent=4)
                
            repetition = []
            possible_ids = range(tool_threats*actual_threats)
            for file in hallucination_files:
                kappa = hallucinations_ai_repetition(file, possible_ids)
                repetition.append(kappa)
                
            with open(f"{stats_folder}/stability_hallucinations.json", "w") as f:
                json.dump(repetition, f, indent=4)
            
            ######################### JUDGE AGREEMENT #########################
            possible_ids = range(tool_threats*actual_threats*iterations)
            kappa = hallucinations_ai_ai(hallucination_files, possible_ids)
            with open(f"{stats_folder}/agreement_hallucinations.json", "w") as f:
                json.dump(kappa, f, indent=4)
                
            kappa = threats_ai_ai(threat_files, possible_ids)
            with open(f"{stats_folder}/agreement_threats.json", "w") as f:
                json.dump(kappa, f, indent=4)