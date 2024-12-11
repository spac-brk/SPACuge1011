import numpy as np
import pandas as pd
import pprint as pp


pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)

path = 'data/'

vgsales = pd.read_csv(path + 'vgsales.csv', dtype={'Rank': int,
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

# Clean up missing data
vgsales['Year'] = vgsales['Year'].replace({np.nan: None})
vgsales['Publisher'] = vgsales['Publisher'].replace({np.nan: 'Unknown'})

# Delete duplicates
vgsales = vgsales[~vgsales['Rank'].isin([15002,16130])]

# Sort by Rank and make first column index column with proper sequential numbering
vgsales = vgsales.sort_values(by=['Rank']).reset_index(drop=True)
vgsales.index += 1  # Make index start at 1
vgsales.insert(0, 'Index', vgsales.index)
# vgsales.drop('Rank', axis = 1)

# Write to CSV
vgsales.to_csv(path + 'vgsales_out.csv', index=False)