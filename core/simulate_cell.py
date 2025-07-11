import json, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
GENE_PATH = os.path.join(BASE_DIR, "data", "gene_rules.json")
DRUG_PATH = os.path.join(BASE_DIR, "data", "drug_targets.json")

with open(GENE_PATH) as f:
    GENE_RULES = json.load(f)
with open(DRUG_PATH) as f:
    DRUG_TARGETS = json.load(f)

def simulate_cell(cell, applied_drugs=None):
    pathways = {"apoptosis": 0.5, "proliferation":0.5, "dna_repair":0.5}

    for gene, state in cell["genes"].items():
        if state== "mutated" and gene in GENE_RULES:
            for path, delta in GENE_RULES[gene]["mutation"].items():
                pathways[path] += delta

    if applied_drugs:
        for drug in applied_drugs:
            dt = DRUG_TARGETS.get(drug, [])
            for target in dt.get("targets", []):
                if cell["genes"].get("targets", []):
                    for path, delta in dt.get("effect", {}).items():
                        pathways[path] += delta
    
    #Make it min of 0 and max of 1
    for p in pathways:
        pathways[p] = max(0.0, min(1.0, pathways[p]))

    fitness = (
        0.6 * pathways["proliferation"]
        + 0.3 * (1 - pathways["apoptosis"])
        + 0.1 * pathways["dna_repair"]
    )
    return pathways, round(fitness, 3)

