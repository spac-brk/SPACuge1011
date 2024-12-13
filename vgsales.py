import pandas as pd
import numpy as np

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)

# Load the dataset
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

# Delete exact duplicates
vgsales = vgsales.drop_duplicates(subset=['Name', 'Platform', 'Year', 'Genre', 'Publisher',
                                          'EU_Sales', 'NA_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'])

# Step 1: Create vgsales_info with unique entries of Name, Year, Genre, Publisher
vgsales_info = vgsales[['Name', 'Year', 'Genre', 'Publisher']].drop_duplicates().reset_index(drop=True)
vgsales_info['Index_Info'] = range(1, len(vgsales_info) + 1)

# Step 2: Create vgsales_plf with aggregated sales data
sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
vgsales_plf = vgsales[['Name', 'Year', 'Platform'] + sales_columns].merge(
    vgsales_info[['Name', 'Year', 'Index_Info']], on=['Name', 'Year'], how='left'
).groupby(['Index_Info', 'Platform'], as_index=False).agg({col: 'sum' for col in sales_columns})
vgsales_plf['Index_Plf'] = range(1, len(vgsales_plf) + 1)
vgsales_plf.rename(columns={'Platform': 'Platform_Id'}, inplace=True)

# Step 3: Create vgsales_reg directly from vgsales_plf
vgsales_reg = vgsales_plf.melt(
    id_vars=['Index_Plf', 'Platform_Id'],
    value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
    var_name='Region',
    value_name='Sales'
).reset_index(drop=True)
vgsales_reg['Region_Id'] = vgsales_reg['Region'].map({'EU_Sales': 1, 'NA_Sales': 2, 'JP_Sales': 3, 'Other_Sales': 4})
vgsales_reg['Index_Reg'] = range(1, len(vgsales_reg) + 1)
vgsales_reg = vgsales_reg[['Index_Reg', 'Index_Plf', 'Region_Id', 'Sales']]

# Choosing columns
vgsales_info = vgsales_info[['Index_Info', 'Name', 'Year', 'Genre', 'Publisher']]
vgsales_plf = vgsales_plf[['Index_Plf', 'Index_Info', 'Platform_Id', 'Global_Sales']]
vgsales_reg = vgsales_reg[['Index_Reg', 'Index_Plf', 'Region_Id', 'Sales']]

# Region names
region_names = pd.DataFrame(np.array([
    [1, 'Europe'],
    [2, 'North America'],
    [3, 'Japan'],
    [4, 'Other Countries']
]), columns=['Region_Id', 'Region_Name'])

# Platform names
platform_names = pd.DataFrame(np.array([
    ['PS2', 'PlayStation 2'],
    ['DS', 'Nintendo DS'],
    ['GB', 'Game Boy'],
    ['GBA', 'Game Boy Advance'],
    ['PS4', 'PlayStation 4'],
    ['PS', 'PlayStation'],
    ['Wii', 'Wii'],
    ['PS3', 'PlayStation 3'],
    ['X360', 'Xbox 360'],
    ['PSP', 'PlayStation Portable'],
    ['3DS', 'Nintendo 3DS'],
    ['NES', 'Nintendo'],
    ['XOne', 'Xbox One'],
    ['SNES', 'Super Nintendo'],
    ['N64', 'Nintendo 64'],
    ['GEN', 'Genesis'],
    ['2600', 'Atari 2600'],
    ['XB', 'Xbox'],
    ['GC', 'GameCube'],
    ['PSV', 'PlayStation Vita'],
    ['WiiU', 'Wii U'],
    ['SAT', 'Sega Saturn'],
    ['DC', 'Dreamcast'],
    ['TG16', 'TurboGrafx-16'],
    ['SCD', 'Sega CD'],
    ['3DO', '3DO'],
    ['NG', 'Neo Geo'],
    ['PCFX', 'NEC PC-FX'],
    ['WS', 'WonderSwan'],
    ['PC', 'PC'],
    ['GG', 'Game Gear']
]), columns=['Platform_Id', 'Platform_Name'])

# Save datasets to CSV files
vgsales_info.to_csv(path + 'vgsales_info.csv', index=False)
vgsales_plf.to_csv(path + 'vgsales_plf.csv', index=False)
vgsales_reg.to_csv(path + 'vgsales_reg.csv', index=False)
region_names.to_csv(path + 'region_names.csv', index=False)
platform_names.to_csv(path + 'platform_names.csv', index=False)

# Print sample rows for verification
print("vgsales_info:")
print(vgsales_info.head())
print("\nvgsales_plf:")
print(vgsales_plf.head())
print("\nvgsales_reg:")
print(vgsales_reg.head())
