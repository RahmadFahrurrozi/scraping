# Load data with semicolon separator
df = pd.read_csv('all_months_clean.csv', sep=';')

# Clean headers again just to be sure (same logic as before)
df.columns = [clean_col_name(col) for col in df.columns]

# Save as STANDARD CSV (Comma separated)
# quoting=1 ensures that if there are commas inside the data (e.g. addresses), 
# they are wrapped in quotes so BigQuery doesn't break.
output_filename = 'all_months_clean_final_comma.csv'
df.to_csv(output_filename, index=False, sep=',')

print("File converted to standard Comma Separated Values.")