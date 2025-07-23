import openpyxl
import pandas as pd

df = pd.read_excel("./data/GDSC2_fitted_dose_response_27Oct23.xlsx", engine="openpyxl")

import json
with open("./data/" \
"GDSC2.json", "w") as f:
    df.to_json(f, orient="records", lines=True)