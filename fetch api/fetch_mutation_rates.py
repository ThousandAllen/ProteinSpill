import pybioportal
import json

import pybioportal.mutations
import pybioportal.sample_lists
import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

# Inputs
study_id = "brca_tcga_gdc"
profile_id = "brca_tcga_gdc_mutations"
sample_list_id = "brca_tcga_gdc_all"
genes = ["TP53", "BRCA1", "PTEN", "KRAS", "PIK3CA", "CDH1", "GATA3"]
# Step 1: Get all sample IDs
sample_list = pybioportal.sample_lists.get_sample_list(sample_list_id)
sample_ids = sample_list.get("sampleIds", [])

#Split pandas series of sample_ids into a list
if isinstance(sample_ids, pd.Series):
    sample_ids = sample_ids.iloc[0]
if isinstance(sample_ids, str):
    sample_ids = [s.strip() for s in sample_ids.split(",")]
total_samples=len(sample_ids)

print(f" Total samples: {total_samples}")
# Step 2: Fetch all mutations from the sample list
mutations = pybioportal.mutations.fetch_muts_in_mol_prof(molecular_profile_id=profile_id, sample_list_id=sample_list_id)
# Step 3: Calculate mutation frequencies
with open('troubleshooting.txt', 'w') as f:
    print(mutations, file=f) 

def extract_gene(val):
    try:
        return str(val).split()[0]
    except Exception:
        return None
    
mutations["gene"] = mutations["keyword"].apply(extract_gene)


# Drop rows with missing genes or sample IDs

mutations = mutations.dropna(subset=["gene", "sampleId"])


# Count how many *unique* samples each gene appears in

gene_sample_counts = mutations.groupby("gene")["sampleId"].nunique()


# Calculate frequency

mutation_frequencies = (gene_sample_counts / total_samples).round(4)


# Save as JSON

mutation_frequencies.to_json("mutation_frequencies.json", orient="index", indent=2)


print(f"✅ Saved frequencies for {len(mutation_frequencies)} genes.")
