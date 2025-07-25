def get_metadata(filepath: str) -> list: 

    try: 
        with open(filepath, 'r') as file: 
            lines = file.read().split("\n")

            return [line for line in lines if line.startswith("!")]
    except FileNotFoundError as fe: 
        print(f"file  {filepath} not found")


def filter_characteristic(metadata: list, keyword: str)-> list: 

    return list(filter(lambda x: keyword in x, metadata))


def filter_diagnosis_string(diagnosis_str: str,  keyword: str = "diagnosis")-> list: 

    diagnosis_list  = list(filter(lambda x: keyword in x, diagnosis_str.split("\t")[1:]))

    diagnosis_list = list(map(lambda x: x.strip("\""), diagnosis_list))
    
    return diagnosis_list