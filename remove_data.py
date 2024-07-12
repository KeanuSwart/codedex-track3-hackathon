import pandas as pd

file_path = 'updated_filtered_results.csv'
df = pd.read_csv(file_path)

# Convert rank_position to integer
df['rank_position'] = pd.to_numeric(df['rank_position'], errors='coerce')

# Filter the DataFrame to keep only rows where rank_position is 1, 2, 3, 4, or 5
filtered_df = df[df['rank_position'].isin([1, 2, 3, 4, 5])]

pivot_df = filtered_df.pivot_table(
    index=['discipline_title', 'slug_game', 'country_name', 'country_code', 'country_3_letter_code'],
    columns='rank_position',
    aggfunc='size',
    fill_value=0
).reset_index()

pivot_df.columns = ['discipline', 'olympic_event', 'country_name', 'country_code', 'country_3_letter_code', 'first', 'second', 'third', 'fourth', 'fifth']

output_file_path = 'olympic_rank_counts.csv' 
pivot_df.to_csv(output_file_path, index=False)

print(f"Filtered file saved to {output_file_path}")