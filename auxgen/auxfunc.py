"""
Auxiliary functions 

JCA
"""
import os
import json
import random

import pandas as pd
from tqdm import tqdm

def unnormalize(val, low, high):
    """Return un-normalized value from its limits"""
    size = high-low
    return low + (val*size)


def save_values(values:dict, save_filepath, design_column='designs'):
    """Save dict in CSV. {colum_name: values}"""
    df = pd.DataFrame(values)
    df[design_column] = df[design_column].apply(json.dumps)
    df.to_csv(save_filepath, index=False) 


def get_best_designs(designs, costs, n):
    """
    Return the top `n` designs with the lowest costs.

    Parameters:
        costs (list of float): List of cost values.
        designs (list of list): List of corresponding design parameters.
        n (int): Number of top designs to return.

    Returns:
        tuple: (best_costs, best_designs), both lists of length `n`.
    """
    sorted_pairs = sorted(zip(costs, designs), key=lambda x: x[0])
    best_costs, best_designs = zip(*sorted_pairs[:n])
    return list(best_designs), list(best_costs)


def get_random_designs(costs, designs, n, seed=None):
    """
    Return `n` random designs and their associated costs.

    Parameters:
        costs (list of float): List of cost values.
        designs (list of list): List of corresponding design parameters.
        n (int): Number of random designs to return.
        seed (int, optional): Random seed for reproducibility.

    Returns:
        tuple: (random_costs, random_designs), both lists of length `n`.
    """
    if seed is not None:
        random.seed(seed)

    indices = random.sample(range(len(costs)), n)
    random_costs = [costs[i] for i in indices]
    random_designs = [designs[i] for i in indices]
    
    return random_costs, random_designs



def save_models_from_list(designs:list, build_model, save_path:str, format='stl'):
    """Save models in path using a building 3d model function"""
    n=len(designs)
    for x, i in tqdm(zip(designs, range(n)), total=n):
        model = build_model(x)

        savepath = os.path.join(save_path, f'model.{i}.{format}')
        model.export(savepath)