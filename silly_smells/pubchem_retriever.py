import requests
from pprint import pprint
import json
from typing import List,Any
import pandas as pd
from time import sleep
from math import floor
import urllib
import os

def fetch_pubchem_data(compound_identifiers:List[int],style=str) ->List[dict[str,Any]]:
    
    
    if style=="cid":
        params = {
            "cid": ",".join(map(str, compound_identifiers))  # Convert list of CIDs to a comma-separated string
        }
        base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/property/IsomericSMILES,InChI,Fingerprint2D/JSON"
    elif style=="inchikey":
        # encoded_identifiers=[urllib.parse.quote(inchi) for inchi in compound_identifiers]
        
        params = {
            "inchikey": ",".join(map(str, compound_identifiers))  # Convert list of CIDs to a comma-separated string
        }
        base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/property/IsomericSMILES,InChI,Fingerprint2D/JSON"
    else:
        raise Exception('please define style as cid or inchikey')
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        try:
            data = response.json()
            compounds = data.get("PropertyTable", {}).get("Properties", [])
            
            results = []
            for compound in compounds:
                results.append({
                    "CID": compound.get("CID"),
                    "SMILES": compound.get("IsomericSMILES"),
                    "InChIKey": compound.get("InChIKey"),
                    "CACTVS_Fingerprint": compound.get("Fingerprint2D")
                })
            
            return results
        except json.JSONDecodeError:
            print('malformed json')
            return None
    else:
        print(f'response code {response.status_code}')
        return None


def wrap_pubchem_calls_for_msp_df(input_file_path:str,chunk_size:int,output_file_path:str):
    msp_inchikey_df=pd.read_csv(input_file_path,sep='\t')
    iterations=floor(len(msp_inchikey_df)/chunk_size)
    print(f'we are going to do {iterations}')
    
    current_chunk_results=[]
    for i in range(iterations):
        if i<=430:
            continue
        this_chunk_inchikeys=msp_inchikey_df.iloc[i*chunk_size:i*chunk_size+chunk_size,:]['inchikey'].tolist()
        pubchem_result=fetch_pubchem_data(this_chunk_inchikeys,'inchikey')
        if pubchem_result==None:
            print(f'failed for iteration {i}')
            continue
        else:
            current_chunk_results.extend(pubchem_result)
        if i%10==0 and i>0:
            print(f'on iteration {i}')
            temp=pd.DataFrame.from_records(current_chunk_results)
            temp.to_pickle(output_file_path+f'pubchem_results_starting_at_{i}.bin')
            current_chunk_results=[]
        sleep(10)

if __name__=="__main__":
    wrap_pubchem_calls_for_msp_df(
        '../data_results/nist_17_gcms_inchikeys.tsv',
        100,
        '../data_results/msp_pubchem_calls/'
    )