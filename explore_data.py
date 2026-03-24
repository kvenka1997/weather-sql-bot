import pandas as pd
import sqlite3

# Load the CSV
df = pd.read_csv('/Users/krishnavenkatesan/Downloads/climate_data/global_climate_energy_2020_2024.csv')

# Explore the data
print('Columns:', df.columns.tolist())
print('Rows:', len(df))
print(df.head(3))

# Convert to SQLite
conn = sqlite3.connect('/Users/krishnavenkatesan/Documents/Projects/test sql agent/climate.db')
df.to_sql('climate_data', conn, if_exists='replace', index=False)
conn.close()
print("Successfully saved to climate.db!")

# Summary statistics
print("\n--- BASIC INFO ---")
print(f"Total Rows: {len(df)}")
print(f"Total Countries: {df['country'].nunique()}")
print(f"Countries: {df['country'].unique().tolist()}")
print(f"Date Range: {df['date'].min()} to {df['date'].max()}")

print("\n--- STATISTICS ---")
print(df.describe())

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())