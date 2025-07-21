import json
import random

def load_drug_database(json_file="drug_database.json"):
    with open(json_file, "r") as f:
        return json.load(f)

def apply_drugs(cell):
    """
    Apply drugs to this cell. Reduces fitness if targets are mutated.
    For wild-type targets, small optional penalty.
    """
    for drug in cell.drug_database:
        targets = drug["targets"]
        for gene in targets:
            is_mutated = cell.genome.get(gene, False)

            # Apply effect if mutated
            if is_mutated:
                reduction = drug["fitness_reduction"]
                if random.random() < drug["success_rate"]:
                    cell.fitness -= reduction
                    cell.fitness = max(cell.fitness, 0.1)

            # Optional wild-type effect (some drugs have mild toxicity on wild-type)
            elif "wildtype_penalty" in drug:
                if random.random() < drug.get("wildtype_chance", 0.1):
                    cell.fitness -= drug["wildtype_penalty"]
                    cell.fitness = max(cell.fitness, 0.1)
