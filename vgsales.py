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
sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']

# Clean up missing data
vgsales['Year'] = vgsales['Year'].replace({np.nan: None})
vgsales['Publisher'] = vgsales['Publisher'].replace({np.nan: 'Unknown'})

# Delete duplicates
vgsales = vgsales.drop_duplicates(subset=['Name', 'Platform', 'Year', 'Genre', 'Publisher'])

# Add `Game_Id` for unique (Name, Year, Genre, Publisher) combinations
vgsales['Game_Id'] = (
    vgsales.groupby(['Name', 'Year', 'Genre', 'Publisher'], dropna=False).ngroup() + 1
)

# Add `Platform_Id` for each `Game_Id` and platform combination
vgsales['Platform_Id'] = (
    vgsales.groupby(['Game_Id', 'Platform'], dropna=False).cumcount() + 1
)

# Add unique `Index_Reg` for each row in `vgsales_reg`
vgsales['Index_Info'] = range(1, len(vgsales) + 1)

# Save vgsales with added identifiers
vgsales_info = vgsales[['Index_Info', 'Game_Id', 'Platform_Id', 'Name',
                        'Platform', 'Year', 'Genre', 'Publisher', 'Global_Sales']]
vgsales_info = vgsales_info.rename(columns={'Platform': 'Platform_Short'})
vgsales_info.to_csv(path + 'vgsales_info.csv', index=False)

# Expand regional sales into a separate dataset `vgsales_reg`
vgsales_reg = vgsales.melt(
    id_vars='Index_Info',
    value_vars=sales_columns[:-1],
    var_name='Region',
    value_name='Sales'
).reset_index(drop=True)

# Map `Region_Id` to regions
region_mapping = {
    'NA_Sales': 2,  # North America
    'EU_Sales': 1,  # Europe
    'JP_Sales': 3,  # Japan
    'Other_Sales': 4  # Other Countries
}
vgsales_reg['Region_Id'] = vgsales_reg['Region'].map(region_mapping)

# Add unique `Index_Reg` for each row in `vgsales_reg`
vgsales_reg['Index_Reg'] = range(1, len(vgsales_reg) + 1)

# Save `vgsales_reg` dataset
vgsales_reg = vgsales_reg[['Index_Reg', 'Index_Info', 'Region_Id', 'Sales']]
vgsales_reg.to_csv(path + 'vgsales_reg.csv', index=False)

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
]), columns=['Platform_Short', 'Platform_Long'])

# Region names
region_names = pd.DataFrame(np.array([
    [1, 'Europe'],
    [2, 'North America'],
    [3, 'Japan'],
    [4, 'Other Countries']
]), columns=['Region_Id', 'Region_Name'])

# Save additional datasets
platform_names.to_csv(path + 'platform_names.csv', index=False)
region_names.to_csv(path + 'region_names.csv', index=False)

# Print sample rows for verification
print("vgsales:")
print(vgsales_info.head())
print("\nvgsales_reg:")
print(vgsales_reg.head())
