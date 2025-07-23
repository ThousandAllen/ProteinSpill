from core.virtual_cell import VirtualCell
import random
from core.drug_modeling import apply_drugs

def simulate_population(gene_probs, num_initial_cells=10, max_generations=50, mutation_rate=0.01, env_factor=1.0, fitness_genes=None, drug_db = None):
    population = [VirtualCell(gene_probs, fitness_genes, drug_db) for _ in range(num_initial_cells)]
    cancerous_cells = []
    lineage_tree = {}
    

    for gen in range(1, max_generations + 1):
        new_population = []
        fitness_change=[]

        for cell in population:
            cell.mutate(gene_probs, mutation_rate, env_factor)

            fitness = cell.get_fitness()
            fitness_pre = fitness #For keeping track of fitness scores
            
            apply_drugs(cell)

            if cell.is_cancerous() and cell.id not in cancerous_cells:
                cancerous_cells.append(cell.id)
                lineage_tree[cell.id] = cell.lineage

            if random.random() < min(fitness * 0.05, 1.0):
                child = cell.divide()
                new_population.append(child)

            fitness_change.append(fitness_pre-fitness)
            print(f"{fitness}")

        population.extend(new_population)
        print(f"Average fitness from drugs: {(sum(fitness_change)/len(fitness_change)):.2f}")

    print(f"🔬 Simulated {len(population)} total cells over {max_generations} generations")
    print(f"💥 {len(cancerous_cells)} became cancerous")
    print("🌳 Example lineage trees:")
    for cid in cancerous_cells[:5]:
        print(f"  {cid}: {' → '.join(lineage_tree[cid])} → {cid}" if lineage_tree[cid] else f"  {cid}: [original]")