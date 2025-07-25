import pandas as pd 
import sklearn 
import imblearn
import numpy as np 
import re 


def get_metadata(filepath: str) -> list: 

    try: 
        with open(filepath, 'r') as file: 
            lines = file.read().split("\n")

            return [line for line in lines if line.startswith("!")]
    except FileNotFoundError as fe: 
        print(f"file  {filepath} not found")


def filter_characteristic(metadata: list, keyword: str)-> list: 

    return list(filter(lambda x: keyword in x, metadata))

