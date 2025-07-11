import pybioportal
import pybioportal.molecular_profiles
import pybioportal.sample_lists
import pandas as pd
import pybioportal.studies

df = pybioportal.sample_lists.get_all_sample_lists()
study = pybioportal.studies.get_all_studies()
prof = pybioportal.molecular_profiles.get_all_molecular_profiles()
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

with open('sample.txt', 'w') as f:
    print(df, file=f) 
with open('study.txt', 'w') as f:
    print(study, file=f) 
with open('profile.txt', 'w') as f:
    print(prof, file=f) 

