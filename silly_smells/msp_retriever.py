import pandas as pd
from typing import List

def msp_to_inchis(file_path:str)->List[str]:
    inchis=[]
    with open(file_path,'r') as temp_file:
        for line in temp_file:
            line_parts=line.split(': ')
            if line_parts[0]=='InChIKey':
                inchis.append(line_parts[1][:27])
    return inchis

def msp_to_inchi_df(input_file_path:str,output_file_path:str)->None:
    assert output_file_path[-4:]=='.tsv'
    inchis=msp_to_inchis(input_file_path)
    output=pd.DataFrame.from_dict({
        'inchikey':inchis
    })
    output.to_csv(output_file_path,sep='\t')


if __name__=="__main__":
    input_path='../data_resources/mainlib.msp'
    output_path='../data_results/nist_17_gcms_inchikeys.tsv'
    msp_to_inchi_df(input_path,output_path)
