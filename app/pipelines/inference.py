from ..utils.io import load_model 
import numpy as np 
import logging 
from pathlib import Path
from ..model.classifier import CancerClassifier


class InferencePipeline(): 

    def __init__(self, model: CancerClassifier): 

        self.model = model 
    
    @classmethod
    async def create(cls, model_filepath): 

        if not Path(model_filepath).exists(): 
            logging.error(f"{model_filepath} not found")
            return None

        model = await load_model(model_filepath) 
        return cls(model) 
    

    async def predict(self, input_data: np.ndarray): 

        predictions = self.model.predict(input_data)

        return predictions 
    

    async def scores(self, input_data): 

        scores = self.model.get_confidence_score(input_data) 

        return scores 
    