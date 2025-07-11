import random

# Randomly mutate cells, given a mutation rate
def mutate_cell(cell, mutation_rate=0.1):
    new_genes = cell["genes"].copy()
    for gene in new_genes:
        if random.random() < mutation_rate:
            new_genes[gene] = (
                "mutated" if new_genes[gene] == "wildtype" else "wildtype"
            )
    return {"genes": new_genes}