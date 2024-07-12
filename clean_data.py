import pandas as pd
import numpy as np

file_path = 'olympic_predictions_2024.csv'
df = pd.read_csv(file_path)

# Round down the values and remove decimal places
df['pred_first'] = np.floor(df['pred_first']).astype(int)
df['pred_second'] = np.floor(df['pred_second']).astype(int)
df['pred_third'] = np.floor(df['pred_third']).astype(int)
df['pred_fourth'] = np.floor(df['pred_fourth']).astype(int)
df['pred_fifth'] = np.floor(df['pred_fifth']).astype(int)

# Convert negative values to 0
df['pred_first'] = df['pred_first'].apply(lambda x: max(x, 0))
df['pred_second'] = df['pred_second'].apply(lambda x: max(x, 0))
df['pred_third'] = df['pred_third'].apply(lambda x: max(x, 0))
df['pred_fourth'] = df['pred_fourth'].apply(lambda x: max(x, 0))
df['pred_fifth'] = df['pred_fifth'].apply(lambda x: max(x, 0))

df = df.drop(columns=['weighted_first', 'weighted_second', 'weighted_third', 'weighted_fourth', 'weighted_fifth'])

processed_file_path = 'processed_olympic_predictions_2024.csv'
df.to_csv(processed_file_path, index=False)

print(f"Processed file saved to {processed_file_path}")
