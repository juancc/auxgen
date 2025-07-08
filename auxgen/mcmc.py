"""
Generative design with Markov Chain Monte Carlo

Class implements the sampling from posterior build uppon the cost function

JCA
"""
import os

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


from auxgen.auxfunc import save_values

class MCMC():
    def __init__(self, 
                 cost_function, 
                 temperature=0.3, 
                 proposal_std=0.2,
                 
                 ):
        """Work with design values in range (0-1)"""
        
        self.temp = temperature
        self.cost_function = cost_function
        self.proposal_std = proposal_std

        self.costs = []
        self.designs = [] # Current design variables

    def sample(self):
        """Propone valores usando MCMCM"""
        x_proposal = np.random.normal(self.x_current, self.proposal_std)
        x_proposal = np.clip(x_proposal, 0, 1)

        cost_proposal = self.cost_function(x_proposal)

        # Compute likelihoods using Boltzmann formulation
        likelihood_proposal = np.exp(-cost_proposal / self.temp)

        # Compute acceptance ratio
        alpha = min(1, likelihood_proposal / self.likelihood_current)

        # Accept or reject the proposed sample
        u = np.random.rand()
        if u < alpha:
            self.x_current = x_proposal
            self.likelihood_current = likelihood_proposal

            # In MCMC when the proposal is rejected the current os added again
            # This construct the correct posterior distribution
            # But in generative design doesnt have sense
            # Instead only new currents are added
            return x_proposal.tolist(), cost_proposal

        return None
    
    def run(self, init_values, num_alternatives=100):
        """Run multiple generative iterations"""
        print(f' - Running MCMC: {num_alternatives} alternatives')
        self.x_current = init_values
        cost_proposal = self.cost_function(init_values)
        self.likelihood_current = np.exp(-cost_proposal / self.temp)

        self.costs = []
        self.designs = [] # Current design variables
        for i in tqdm(range(num_alternatives), total=num_alternatives):
            try:
                gen_vals = self.sample()
                if gen_vals:
                    curr_values, c = gen_vals

                # if self.save_path: 
                #     save_model_path = os.path.join( self.save_path, f'model{i}.stl')
                #     bot.export(save_model_path)

                self.costs.append(c)
                self.designs.append(curr_values)

            except Exception as e:
                # print(e)
                pass
        return self.designs, self.costs
        


    def save_results(self, save_path):
        """Save results in CSV file"""
        if not self.costs:
            print('Run generation first')
            return
        print(f' - Saving results {save_path}')
        savename = f'T{self.temp}-STD{self.proposal_std}'

        savefigpath = os.path.join(save_path, f'{savename}.pdf')

        save_results_path = os.path.join(save_path, f'{savename}.csv')
        values = { 'designs': self.designs, 'costs':self.costs}

        save_values(values, save_results_path)
  
        

    def plot_results(self, figsize=(10,6)):
        """Plot cost distribution if generation process ran"""
        if not self.costs:
            print('Run generation first')
            return

        # Save designs and plot
        plt.figure(figsize=figsize)

        res = plt.hist(self.costs, label=f'T{self.temp} | STD: {self.proposal_std} | Samples:{len(self.costs)}')
        plt.vlines(np.mean(self.costs), 0, np.max(res[0]),  linestyles='dashed', color='black')

        plt.title(f'Alternatives Cost Distribution')
        plt.xlabel('Cost')
        plt.ylabel('Number of alternatives')
        plt.legend()

        plt.show()