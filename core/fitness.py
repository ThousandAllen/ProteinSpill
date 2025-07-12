import pandas as pd


def parse_gene_name(col_name):

    """

    Extracts the gene symbol from a column header like 'TP53 (7157)'.

    """

    return col_name.split()[0]


def build_fitness_genes(filepath, min_effect=-0.4, scale=0.5):

    """

    Creates a dictionary mapping gene names to fitness score boosts.


    Args:

        filepath (str): Path to CRISPRGeneEffect.csv

        min_effect (float): Threshold for average essentiality score

        scale (float): Scale factor to turn DepMap values into simulator fitness boosts


    Returns:

        dict: gene → fitness_boost

    """

    df = pd.read_csv(filepath, index_col=0)

    

    # Rename columns to just gene symbols

    df.columns = [parse_gene_name(col) for col in df.columns]

    

    # Average effect across all samples per gene

    gene_means = df.mean(axis=0)


    # Keep genes with strong negative effect (essential)

    fitness_genes = {

        gene: round(abs(score) * scale, 3)

        for gene, score in gene_means.items()

        if score < min_effect

    }


    return fitness_genes
