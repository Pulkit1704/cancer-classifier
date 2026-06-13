import pickle 
from pathlib import Path 
import logging 
from app.model.classifier import CancerClassifier


async def read_gene_list(gene_list_filepath): 

    if not Path(gene_list_filepath).exists(): 
        logging.error(f"{gene_list_filepath} does not exist")
        return None 

    with open(gene_list_filepath, 'br') as file: 
        gene_list = pickle.load(file) 

    return gene_list 


async def load_model(classifier_filepath: str): 

    if not Path(classifier_filepath).exists(): 

        logging.error(f"{classifier_filepath} does not exist") 

    try: 
        with open(classifier_filepath, 'br') as file: 

            classifier = pickle.load(file) 

            return classifier 
    except Exception as e: 
        logging.error(f"error occured when reading file: {classifier_filepath}, {e}")

    return 


async def save_model(classifier: CancerClassifier, classifier_filepath: str): 

    path = Path(classifier_filepath) 
 
    path.parent.mkdir(parents= True, exist_ok= True)  

    with open(classifier_filepath, 'bw') as file: 
        pickle.dump(classifier, file)

    return 