# This is the main simulation file.
# Brings in gene probabilities from a json and predicts, of x many cells, how many genes will turn into cancer


import json
import random
import uuid


# ======== NEEDS UPDATED TO INCLUDE ALL DRIVER GENES ==================
DRIVER_GENES = {
        "TP53", "PIK3CA", "BRCA1", "BRCA2", "PTEN", "KRAS", "BRAF", "CDKN2A", "RB1",
        "AKT1", "ERBB2", "EGFR", "ATM", "ARID1A", "SMAD4", "NF1", "NOTCH1", "IDH1",
        "CDH1", "FGFR3", "CCND1", "NFE2L2", "CREBBP", "CTNNB1", "GATA3", "MLH1",
        "MED12", "KMT2D", "KMT2C", "FOXA1", "SETD2", "TET2", "MPL", "MYC", "ASXL1",
        "RUNX1", "FLT3", "DNMT3A", "TERT", "APC", "VHL", "POLE", "SMARCA4", "SUZ12"
        } 


MUTATION_TYPES = ["missense", "truncating", "frameshift", "inframe", "nonsense"]

TYPE_MULTIPLIER = {
    "missense": 0.5,
    "truncating":1.0,
    "frameshift": 0.8,
    "inframe": 0.6,
    "nonsense": 0.1
}

# === 2. Virtual Cell Class ===+
class VirtualCell:
    def __init__(self, gene_probs, fitness_genes, drug_database):
        self.genome = {gene: [] for gene in gene_probs} 
        self.mutation_history = []
        self.driver_genes = DRIVER_GENES
        self.id = str(uuid.uuid4())[:8]
        self.lineage = []
        self.fitness=1.0
        self.gene_probs = gene_probs
        self.fitness_genes = fitness_genes
        self.drug_database = drug_database

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
        child = VirtualCell(self.gene_probs, self.fitness_genes, self.drug_database)
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
    
