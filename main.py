from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse 
from pathlib import Path
from app.pipelines.data_preprocess import DataProcessingService
from app.pipelines.inference import InferencePipeline

from app.utils.io import read_gene_list
import logging

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", summary="Serve frontend landing page")
def serve_frontend():
    html_path = Path("app", "static", "index.html")
    
    if not Path(html_path).exists():
        raise HTTPException(status_code=404, detail="Frontend index.html file not found in static/ directory.")
        
    return FileResponse(html_path)


@app.post("/predict")
async def predict(file: UploadFile = File(...)): 

    """ ingest and process the raw csv file and make predictions to send back"""

    gene_list_path = "./app/trained_model/gene_list.pkl" 

    gene_list = await read_gene_list(gene_list_filepath=gene_list_path)

    processed_data, sample_ids = await DataProcessingService.process(file, gene_list) 

    if processed_data is None: 
        logging.error("file processing failed") 
        return {
            "status": "failed", 
            "predictions": None
        }

    inference_model = await InferencePipeline.create("./app/trained_model/classifier.pkl")

    if inference_model is None: 
        logging.error(f"failed to load model")
        return 

    predictions = await inference_model.predict(processed_data)
    prediction_probabilities = await inference_model.scores(processed_data)

    formatted_results = []
    for sample_id, pred, prob in zip(sample_ids, predictions.tolist(), prediction_probabilities.tolist()):
        formatted_results.append({
            "sample_id": sample_id,
            "prediction": pred,
            "confidence": prob  
        })

    return formatted_results

if __name__ == '__main__':

    import uvicorn 

    uvicorn.run("main:app", 
                host = 'localhost',
                port = 8000, 
                reload = True,
                log_level = "info")

