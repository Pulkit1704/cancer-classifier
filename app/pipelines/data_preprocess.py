import pandas as pd 
import logging 
from typing import BinaryIO
from fastapi import UploadFile, HTTPException


dp_logger = logging.getLogger("data_processing_logger")

dp_logger.parent = logging.getLogger("uvicorn.error")
dp_logger.setLevel(logging.INFO)


class PreProcessor(): 

    def load_frame(self, file: BinaryIO, file_ext): 

        if file_ext == 'csv': 

            frame = pd.read_csv(file, sep = ',', comment = '!')
        elif file_ext in ['tsv', 'txt']: 
            
            file.seek(0) 
            first_line = file.readline().decode('utf-8')
            file.seek(0) 

            if first_line.startswith('!'): 
                frame = pd.read_csv(file, sep = "\t", comment = '!')
            else: 
                frame = pd.read_csv(file, sep = "\t")

        return frame 

    def identify_gene_column(self, frame: pd.DataFrame, gene_list: list): 

        gene_list = list(map(str.lower, gene_list)) 

        if frame.columns.str.lower().isin(gene_list).any(): 

            dp_logger.info("Found gene names in columns. Searching for Sample ID column...")
        
            for col in frame.columns:
                if col.lower() in gene_list:
                    continue
                    
                if frame[col].dtype == 'object' or isinstance(frame[col].iloc[0], str):
                    dp_logger.info(f"Setting column '{col}' as the Sample ID row index.")
                    frame = frame.set_index(col, drop=True)
                    break

            return frame 

        if frame.index.str.lower().isin(gene_list).any(): 
            dp_logger.info("found gene names in the index, transposing the frame...")
            return frame.transpose()
        
        for col in frame.columns: 

            col_contents = frame.loc[:, col] 
            if col_contents.str.lower().isin(gene_list).any(): 
                dp_logger.info(f"found gene names in {col}, setting it as column index")

                frame = frame.set_index(col, drop = True) 
                return frame.transpose() 
            
        dp_logger.error(f"No gene names found in the frame") 

        return None 

    def aggregate_duplicates(self, frame: pd.DataFrame): 

        if not frame.columns.duplicated().any(): 
            dp_logger.info(f"No duplicate gene names found")
            return frame

        frame_aggregated = frame.groupby(frame.columns, axis = 1).mean() 

        return frame_aggregated


    def impute_missing_genes(self, frame: pd.DataFrame, gene_list: list, pseudo_count = 0.01):

        frame_imputed = frame.reindex(gene_list, axis = 1, fill_value=pseudo_count) 

        return frame_imputed 
    
    def extract_numeric_features(self, frame: pd.DataFrame):
    
        numeric_frame = frame.select_dtypes(include='number')
    
        numeric_array = numeric_frame.to_numpy()
    
        return numeric_array
 

    async def process_file(self, 
                           fileobj: BinaryIO, 
                           training_gene_list: list, 
                           file_ext = 'csv'): 

        frame = self.load_frame(fileobj, file_ext) 

        frame = self.identify_gene_column(frame, training_gene_list) 

        if frame is None: 
            raise ValueError(f"No gene column identified in the frame") 

        sample_ids = frame.index.copy()

        frame = self.aggregate_duplicates(frame) 

        frame = self.impute_missing_genes(frame, training_gene_list) 

        frame = self.extract_numeric_features(frame)

        return frame, sample_ids 


class DataProcessingService:

    ALLOWED_FILE_TYPES = ['csv', 'tsv', 'txt'] 

    ALLOWED_FILE_MIME_TYPES = [
        'text/csv', 
        'text/tab-separated-values', 
        'text/plain'
    ]

    @staticmethod
    async def process(file: UploadFile, gene_list: list):

        if not await DataProcessingService.is_valid(file):
            raise HTTPException(status_code=400, detail="Invalid file")
            
        processor = PreProcessor()

        try: 
            return await processor.process_file(file.file, 
                                                gene_list, 
                                                file_ext = file.filename.split(".")[-1])
        except ValueError as ve: 
            dp_logger.error(f"error encountered when processing file: {ve}")
            return None

    @staticmethod
    async def is_valid(file: UploadFile) -> bool:

        await file.seek(0) 

        file_extension = file.filename.split(".")[-1] 

        has_valid_extension = file_extension in DataProcessingService.ALLOWED_FILE_TYPES 

        file_mime_type = file.content_type 

        has_valid_mimetype = file_mime_type in DataProcessingService.ALLOWED_FILE_MIME_TYPES 

        return has_valid_extension and has_valid_mimetype