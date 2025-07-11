from core.evolution import create_initial_population, evolve_population

if __name__ == "__main__":
    pop = create_initial_population(100)
    hist = evolve_population(pop, drugs=["MEK_inhibitor", "PARP_inhibitor"], generations=10, threshold=0.7)
    print("Generation | Avg Fitness | Survivors")
    for record in hist:
        print(f"{record['gen']:>9} | {record['avg_fitness']:>11} | {record['survivors']:>9}")
