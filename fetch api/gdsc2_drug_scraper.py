import pandas as pd

#This us used to create a JSON from the GDSC 2 file.
#I am using this GDSC 2 file

def parse_gdsc_to_drug_db(ic50_file, annotations_file):
    # Load IC50 data
    ic50_df = pd.read_excel(ic50_file)

    # Load drug annotations (targets etc.)
    annotations_df = pd.read_csv(annotations_file)

    drug_db = []

    for _, row in annotations_df.iterrows():
        drug_name = row["DRUG_NAME"]
        targets = [t.strip() for t in str(row["TARGET"]).split(",") if pd.notna(t)]

        if not targets or targets == ["nan"]:
            continue

        # Estimate effectiveness from IC50
        ic50_rows = ic50_df[ic50_df["DRUG_NAME"] == drug_name]
        if ic50_rows.empty:
            continue

        avg_ic50 = ic50_rows["LN_IC50"].mean()
        # Convert IC50 to fitness reduction (inverse scale, adjust as needed)
        fitness_reduction = min(max((5 - avg_ic50) / 5, 0), 0.5)

        # Make mock success rate (optional tweak later)
        success_rate = max(0.5, 1 - avg_ic50 / 10)

        drug_entry = {
            "name": drug_name,
            "targets": targets,
            "mutation_types": ["missense", "truncating"],  # Placeholder; refine later
            "fitness_reduction": round(fitness_reduction, 2),
            "success_rate": round(success_rate, 2)
        }

        drug_db.append(drug_entry)

    return drug_db


if __name__ == "__main__":
    ic50_file = "./data/GDSC2_fitted_dose_response_27Oct23.xlsx"
    annotations_file = "./data/screened_compounds_rel_8.5.csv"

    drug_database = parse_gdsc_to_drug_db(ic50_file, annotations_file)

    # Output to JSON for easy import
    import json
    with open("./data/" \
    "drug_database.json", "w") as f:
        json.dump(drug_database, f, indent=4)

    print(f"Extracted {len(drug_database)} drugs with targets.")
