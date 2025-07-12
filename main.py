from core.population import simulate_population
from core.fitness import build_fitness_genes
import json


# ===== Main Program =======
if __name__ == "__main__":

    # === 1. Load Mutation Frequencies ===
    with open('data/mutation_frequencies.json', 'r') as f:
        gene_freqs = json.load(f)
    total = sum(gene_freqs.values()) 
    gene_probs = {gene: freq / total for gene, freq in gene_freqs.items()} # Normalize into probabilities


    fitness_genes=build_fitness_genes("data/CRISPRGeneEffect.csv")
    simulate_population(gene_probs, num_initial_cells=2, max_generations=100, mutation_rate=0.01, env_factor=2, fitness_genes=fitness_genes)
