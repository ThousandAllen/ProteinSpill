import requests
import json
import os
import time

CACHE_FILE = "vep_cache.json"
ENSEMBL_URL = "https://rest.ensembl.org/vep/human/region"
HEADERS = {"Content-Type": "application/json"}

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def query_vep_bulk_region(variant_tuples, existing_cache):
    to_query = []
    for chrom, pos, ref, alt in variant_tuples:
        key = f"{chrom}:{pos}:{ref}>{alt}"
        if key not in existing_cache:
            to_query.append((key, chrom, pos, ref, alt))

    print(f"Querying {len(to_query)} new variants...")

    chunk_size = 200
    for i in range(0, len(to_query), chunk_size):
        chunk = to_query[i:i + chunk_size]
        formatted = [f"{chrom} {pos} . {ref} {alt} . . ." for _, chrom, pos, ref, alt in chunk]

        response = requests.post(
            ENSEMBL_URL,
            headers=HEADERS,
            json={"variants": formatted}
        )

        if not response.ok:
            print(f"Failed chunk {i}-{i + chunk_size}: {response.status_code} {response.text}")
            time.sleep(1)
            continue

        results = response.json()
        for j, entry in enumerate(results):
            key = to_query[i + j][0]
            gene = (
                entry.get("transcript_consequences", [{}])[0].get("gene_symbol")
                or "unknown"
            )
            consequence = entry.get("most_severe_consequence", "unknown")
            existing_cache[key] = {
                "gene": gene,
                "consequence": consequence
            }

    time.sleep(1) # rate limiting

    return existing_cache

def main():
 # Example list of variants
    variant_tuples = [
    ("17", 7579472, "G", "A"), # TP53
    ("13", 32340345, "C", "T"), # BRCA2
    ("10", 89623195, "C", "T") # PTEN
    ]

    cache = load_cache()
    cache = query_vep_bulk_region(variant_tuples, cache)
    save_cache(cache)

    print(f"\n Cached {len(cache)} variants:")
    for k, v in cache.items():
        print(f"{k}: {v['gene']} - {v['consequence']}")

if __name__ == "__main__":
 main()