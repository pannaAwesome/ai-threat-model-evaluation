
import json
from dotenv import load_dotenv

from llm_as_a_judge.prompts import THREAT_PROMPT
from llm_as_a_judge.vote import vote

def load_threat_models(application):
    """
    Load the threat models for the given application.
    """
    with open(f"threat_templates/{application}/threat_model.json", "r") as file:
        human_threat_model = json.load(file)
        
    # Load AI-generated threat model for STRIDEGPT
    ai_threat_model_path = f"results/{application}/stridegpt_model.json"
    with open(ai_threat_model_path, "r") as ai_file:
        ai_threat_model = json.load(ai_file)
    return { "STRIDEgpt": [human_threat_model, ai_threat_model] }

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    applications = ["message_queue_app"]
    result_folder = "results"
    
    for application in applications:
        print(f"Processing threat models for application: {application}")

        # Collect assets for the application
        assets_path = f"threat_templates/{application}/assets.json"
        with open(assets_path, "r") as assets_file:
            assets = json.load(assets_file)
        
        # Load threat models
        models = load_threat_models(application)
        
        vote(models, assets, THREAT_PROMPT, "")
        