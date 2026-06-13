from ..utils.io import load_model 
import numpy as np 
import logging 
from pathlib import Path


class InferencePipeline(): 


    def __init__(self, model): 

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
    

    def scores(self, input_data): 

        decomposed_inputs = self.model.pca_components(input_data) 

        scores = self.model.svc.score(decomposed_inputs) 

        return scores 
    