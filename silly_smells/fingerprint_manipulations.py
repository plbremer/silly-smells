import pandas as pd
import numpy as np
import base64

def hex_to_binary(hex_fp:str) -> str:
    """Convert a CACTVS fingerprint in hexadecimal format to binary format."""
    return bin(int(hex_fp, 16))[2:].zfill(len(hex_fp) * 4)

def hex_fp_to_binary_array(fingerprint:str) -> np.array:
    """
    """
    binary_fp=hex_to_binary(fingerprint)
    return np.array([char for char in binary_fp])

# https://chem.libretexts.org/Courses/Intercollegiate_Courses/Cheminformatics/06%3A_Molecular_Similarity/6.04%3A_Python_Assignment
def base_64_to_np_array(base_64_fp):
    decoded_bytes = base64.b64decode(base_64_fp)
    binary_string = ''.join(f'{byte:08b}' for byte in decoded_bytes)[32:913]
    return np.array([int(char) for char in binary_string])