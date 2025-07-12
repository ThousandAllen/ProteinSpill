# This is the main simulation file.
# Brings in gene probabilities from a json and predicts, of x many cells, how many genes will turn into cancer


import json
import random
import uuid
from fitness import build_fitness_genes

# === 1. Load Mutation Frequencies ===
with open('mutation_frequencies.json', 'r') as f:
    gene_freqs = json.load(f)

# Normalize into probabilities
total = sum(gene_freqs.values())
gene_probs = {gene: freq / total for gene, freq in gene_freqs.items()}

# ======== NEEDS UPDATED TO INCLUDE ALL DRIVER GENES ==================
DRIVER_GENES = {
        "TP53", "PIK3CA", "BRCA1", "BRCA2", "PTEN", "KRAS", "BRAF", "CDKN2A", "RB1",
        "AKT1", "ERBB2", "EGFR", "ATM", "ARID1A", "SMAD4", "NF1", "NOTCH1", "IDH1",
        "CDH1", "FGFR3", "CCND1", "NFE2L2", "CREBBP", "CTNNB1", "GATA3", "MLH1",
        "MED12", "KMT2D", "KMT2C", "FOXA1", "SETD2", "TET2", "MPL", "MYC", "ASXL1",
        "RUNX1", "FLT3", "DNMT3A", "TERT", "APC", "VHL", "POLE", "SMARCA4", "SUZ12"
        } 


MUTATION_TYPES = ["missense", "truncating", "frameshift", "inframe"]

TYPE_MULTIPLIER = {
    "missense": 0.5,
    "truncating":1.0,
    "frameshift": 0.8,
    "inframe": 0.6
}

# === 2. Virtual Cell Class ===+
class VirtualCell:
    def __init__(self, gene_probs, fitness_genes):
        self.genome = {gene: [] for gene in gene_probs}
        self.mutation_history = []
        self.driver_genes = DRIVER_GENES
        self.id = str(uuid.uuid4())[:8]
        self.lineage = []
        self.fitness=1.0
        self.gene_probs = gene_probs
        self.fitness_genes = fitness_genes

    #Mutate - Simulates mutating 1 cell.
    #Environment Factor is for things like smoking, or being exposed to a lot of UV
    def mutate(self, gene_probs, mutation_rate=0.001, env_factor=1.0):
        for gene, prob in gene_probs.items():
            mut_chance = mutation_rate * prob * env_factor
            if random.random() < mut_chance:
                mutation_type = random.choice(MUTATION_TYPES)
                self.genome[gene].append(mutation_type)
                self.mutation_history.append((gene, mutation_type))

        self.fitness = self.get_fitness()
    

    # Define cancer-like state: 5+ total mutations & ≥1 from "critical" list
    def is_cancerous(self):     
        mutated= {gene for gene, mutated in self.genome.items() if mutated}
        return len(mutated) >= 5 and bool(mutated & DRIVER_GENES)
    
    #Let certain mutation make the cell more likely to survive or mutate farther
    def get_fitness(self):
        base_fitness = 1.0
        for gene, mutations in self.genome.items():
            if gene in self.fitness_genes:
                for mutation_type in mutations:
                    multiplier = TYPE_MULTIPLIER.get(mutation_type, 0.5)
                    base_fitness += (self.fitness_genes[gene]*multiplier)
        return base_fitness

    #Divide the cell into 2
    def divide(self):
        child = VirtualCell(self.gene_probs, self.fitness_genes)
        child.genome = {gene: muts.copy() for gene, muts in self.genome.items()}
        child.mutation_history = self.mutation_history.copy()
        child.fitness = self.fitness
        child.lineage = self.lineage + [self.id]
        for gene, muts in self.genome.items():
            if muts: 
                print(f"{gene}: {', '.join(muts)}")
        return child

    def get_final_genome(self):
        return sorted([g for g, v in self.genome.items() if v])
    

def simulate_population(gene_probs, num_initial_cells=10, max_generations=50, mutation_rate=0.01, env_factor=1.0, fitness_genes=None):
    population = [VirtualCell(gene_probs, fitness_genes) for _ in range(num_initial_cells)]
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
    fitness_genes=build_fitness_genes("data/CRISPRGeneEffect.csv")
    simulate_population(gene_probs, num_initial_cells=2, max_generations=100, mutation_rate=0.01, env_factor=2, fitness_genes=fitness_genes)