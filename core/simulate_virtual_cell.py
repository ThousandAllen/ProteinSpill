# This is the main simulation file.
# Brings in gene probabilities from a json and predicts, of x many cells, how many genes will turn into cancer


import json
import random
import uuid

# === 1. Load Mutation Frequencies ===
with open('mutation_frequencies.json', 'r') as f:
    gene_freqs = json.load(f)

# Normalize into probabilities
total = sum(gene_freqs.values())
gene_probs = {gene: freq / total for gene, freq in gene_freqs.items()}

DRIVER_GENES = {
        "TP53", "PIK3CA", "BRCA1", "BRCA2", "PTEN", "KRAS", "BRAF", "CDKN2A", "RB1",
        "AKT1", "ERBB2", "EGFR", "ATM", "ARID1A", "SMAD4", "NF1", "NOTCH1", "IDH1",
        "CDH1", "FGFR3", "CCND1", "NFE2L2", "CREBBP", "CTNNB1", "GATA3", "MLH1",
        "MED12", "KMT2D", "KMT2C", "FOXA1", "SETD2", "TET2", "MPL", "MYC", "ASXL1",
        "RUNX1", "FLT3", "DNMT3A", "TERT", "APC", "VHL", "POLE", "SMARCA4", "SUZ12"
        } 

# === Placeholder fitness values ===
FITNESS_GENES = {
    "TP53": 0.3,
    "PIK3CA": 0.2,
    "BRCA1": 0.25,
    "KRAS": 0.35,
    "BRAF": 0.25,
    "EGFR": 0.3,
    "MYC": 0.2
}

# === 2. Virtual Cell Class ===+
class VirtualCell:
    def __init__(self, gene_probs, parent_id=None):
        self.genome = {gene: False for gene in gene_probs}
        self.mutation_history = []
        self.driver_genes = DRIVER_GENES
        self.id = str(uuid.uuid4())[:8]
        self.parent_id = parent_id
        self.lineage = []

    #Mutate - Simulates mutating 1 cell.
    #Environment Factor is for things like smoking, or being exposed to a lot of UV
    def mutate(self, gene_probs, mutation_rate=0.001, env_factor=1.0):
        for gene, prob in gene_probs.items():
            if not self.genome[gene]: #only mutate unmutated genes
                mut_chance = mutation_rate * prob * env_factor
                if random.random() < mut_chance:
                    self.genome[gene] = True
                    self.mutation_history.append(gene)
        

    # Define cancer-like state: 5+ total mutations & ≥1 from "critical" list
    def is_cancerous(self):     
        mutated= {gene for gene, mutated in self.genome.items() if mutated}
        return len(mutated) >= 5 and bool(mutated & DRIVER_GENES)
    
    #Let certain mutation make the cell more likely to survive or mutate farther
    def get_fitness(self):
        fitness = 1.0
        for gene, mutated in self.genome.items():
            if mutated:
                fitness += FITNESS_GENES.get(gene, 0)
        return fitness

    #Divide the cell into 2
    def divide(self):
        child = VirtualCell(gene_probs, parent_id=self.id)
        child.genome = self.genome.copy()
        child.mutation_history = self.mutation_history.copy()
        child.lineage = self.lineage + [self.id]
        return child

    def get_final_genome(self):
        return sorted([g for g, v in self.genome.items() if v])
    

def simulate_population(gene_probs, num_initial_cells=10, max_generations=50, mutation_rate=0.01, env_factor=1.0):
    population = [VirtualCell(gene_probs) for _ in range(num_initial_cells)]
    cancerous_cells = []
    lineage_tree = {}

    for gen in range(1, max_generations + 1):
        new_population = []

        for cell in population:
            cell.mutate(gene_probs, mutation_rate, env_factor)

            if cell.is_cancerous() and cell.id not in cancerous_cells:
                cancerous_cells.append(cell.id)
                lineage_tree[cell.id] = cell.lineage

            fitness = cell.get_fitness()
            if random.random() < min(fitness * 0.05, 1.0):
                child = cell.divide()
                new_population.append(child)

        population.extend(new_population)

    print(f"🔬 Simulated {len(population)} total cells over {max_generations} generations")
    print(f"💥 {len(cancerous_cells)} became cancerous")
    print("🌳 Example lineage trees:")
    for cid in cancerous_cells[:5]:
        print(f"  {cid}: {' → '.join(lineage_tree[cid])} → {cid}" if lineage_tree[cid] else f"  {cid}: [original]")


# === 4. Run the Simulation ===
if __name__ == "__main__":
    simulate_population(gene_probs, num_initial_cells=10, max_generations=100, mutation_rate=0.01, env_factor=2)