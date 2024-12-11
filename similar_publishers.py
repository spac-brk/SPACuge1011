import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)

path = 'data/'

vgsales = pd.read_csv(path + 'vgsales_out.csv', dtype={'Rank': int,
                                                   'Name': str,
                                                   'Platform': str,
                                                   'Year': 'Int64',
                                                   'Genre': str,
                                                   'Publisher': str,
                                                   'NA_Sales': float,
                                                   'EU_Sales': float,
                                                   'JP_Sales': float,
                                                   'Other_Sales': float,
                                                   'Global_Sales': float})


# Find publishers with similar names
publishers = pd.DataFrame(np.sort(vgsales['Publisher'].unique()), columns=['Publisher'])
publishers_n = publishers
publishers_n['Next_Publisher'] = publishers_n['Publisher'].shift(-1)
publishers_n['Similarity'] = publishers_n.apply(
    lambda row: fuzz.partial_ratio(row['Publisher'], row['Next_Publisher']) if row['Next_Publisher'] else 0, axis=1)
similar_publishers_1 = (publishers_n[publishers['Similarity'] >= 75]
                        .sort_values(by='Similarity', ascending=False)
                        .reset_index(drop=True))

# Loop through publishers and extract similar ones
similar_publishers_2_data = []
for publ in publishers['Publisher']:
    matches = process.extract(publ, publishers['Publisher'].tolist(), limit=2)
    for match in matches:
        if match[0] != publ:
            sorted_pair = tuple(sorted([publ, match[0]]))
            similar_publishers_2_data.append({
                'Publisher': sorted_pair[0],
                'Similar_Publisher': sorted_pair[1],
                'Similarity': match[1]
            })
similar_publishers_2 = (pd.DataFrame(similar_publishers_2_data)
                        .drop_duplicates()
                        .reset_index(drop=True))
similar_publishers_2 = (similar_publishers_2[similar_publishers_2['Similarity'] >= 75]
                        .sort_values(by='Similarity', ascending=False)
                        .reset_index(drop=True))

# Write to CSV
similar_publishers_1.to_csv(path + 'similar_publishers_1.csv', index=False)
similar_publishers_2.to_csv(path + 'similar_publishers_2.csv', index=False)
