import numpy as np
import pandas as pd

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
vgsales.rename(columns={'Platform': 'Platform_Id'}, inplace=True)

# Clean up missing data
vgsales['Year'] = vgsales['Year'].replace({np.nan: None})
vgsales['Publisher'] = vgsales['Publisher'].replace({np.nan: 'Unknown'})

# Delete exact duplicates
vgsales = vgsales.drop_duplicates(subset=['Name', 'Platform_Id', 'Year', 'Genre', 'Publisher',
                                          'EU_Sales', 'NA_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'])

# Sort data and make first column index column with proper sequential numbering
vgsales = (vgsales.sort_values(by=['Year', 'Genre', 'Publisher', 'Name', 'Platform_Id'])
           .reset_index(drop=True))
vgsales.index += 1  # Make index start at 1
vgsales.insert(0, 'Index_Info', vgsales.index)
vgsales_info = vgsales[['Index_Info', 'Name', 'Platform_Id', 'Year', 'Genre', 'Publisher', 'Global_Sales']]

# Normalize sales
vgsales = pd.melt(vgsales, ['Index_Info', 'Name', 'Platform_Id', 'Year', 'Genre', 'Publisher'],
                  ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'],
                  var_name='Region', value_name='Sales')
vgsales = vgsales[~(vgsales['Region'] == 'Global_Sales')]
vgsales['Region_Id'] = vgsales['Region'].map({'EU_Sales': 1, 'NA_Sales': 2, 'JP_Sales': 3, 'Other_Sales': 4})
vgsales = (vgsales.sort_values(by=['Index_Info', 'Region_Id'])
           .reset_index(drop=True))
vgsales.index += 1  # Make index start at 1
vgsales.insert(0, 'Index_Reg', vgsales.index)
vgsales_reg = vgsales[['Index_Reg', 'Index_Info', 'Region_Id', 'Sales']]

# Region names
region_names = pd.DataFrame(np.array([[1, 'Europe'],
                                      [2, 'North America'],
                                      [3, 'Japan'],
                                      [4, 'Other Countries']]),
                            columns=['Region_Id', 'Region_Name'])

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

# Write to CSV
vgsales_info.to_csv(path + 'vgsales_info.csv', index=False)
vgsales_reg.to_csv(path + 'vgsales_reg.csv', index=False)
region_names.to_csv(path + 'region_names.csv', index=False)
platform_names.to_csv(path + 'platform_names.csv', index=False)
