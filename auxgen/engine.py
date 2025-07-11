"""
Generation loops 

Requires:
- tqdm

JCA
"""
import os
from tqdm import tqdm

def simple_loop(model_fn, alternatives, save_path, save_format='stl', model_args=None, model_kwarks=None):
    """Generate design alternatives using the model_fn to create instances"""
    err = []
    for i in tqdm(range(alternatives), total=alternatives):
        try:
            model_args = model_args if model_args else []
            model_kwarks = model_kwarks if model_kwarks else {}
            alt = model_fn(*model_args, **model_kwarks)
        except Exception as e:
            err.append(e)
            continue
        
        filepath = os.path.join(save_path, f'model-{i}.{save_format}')
        alt.export(filepath)
    
    print(f' - {len(err)} Errors generating alternatives')
    
