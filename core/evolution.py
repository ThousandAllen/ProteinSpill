import random
from core.simulate_cell import simulate_cell
from core.mutate_cell import mutate_cell

GENE_LIST = [
    "TP53", "KRAS", "BRCA1", "PTEN",
    "EGFR", "PIK3CA", "RB1", "CDKN2A",
    "ATM", "MYC"
]

def create_initial_population(n=100):
    pop = []
    for _ in range(n):
        pop.append({
            "genes": {g: random.choice(["wildtype", "mutated"]) for g in GENE_LIST}
        })
    return pop

def evolve_population(population, drugs=None, generations=10, threshold=0.5):
    history = []
    for gen in range(1, generations+1):
        scores = [(cell, simulate_cell(cell, drugs)[1]) for cell in population]
        survivors = [c for c, f in scores if f >= threshold]
        population = [
            mutate_cell(c) for c in survivors for _ in range(2)
        ][:len(population)]
        avg_fit = round(sum(f for _, f in scores) / len(scores), 3)
        history.append({"gen": gen, "avg_fitness": avg_fit, "survivors": len(survivors)})
    return history