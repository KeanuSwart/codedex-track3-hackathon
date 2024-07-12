import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

file_path = 'olympic_rank_counts.csv'
df = pd.read_csv(file_path)

# Normalize the data by assigning weights based on the year of the Olympic event
# Assuming the format of 'olympic_event' is consistent like 'london-2012', 'rio-2016', etc.
event_years = {'london-2012': 2012, 'rio-2016': 2016, 'tokyo-2020': 2020}
current_year = 2024

# Create a weight column based on the event year
df['weight'] = df['olympic_event'].apply(lambda x: 1 / (current_year - event_years[x]))

# Create features based on the historical performance
# Sum the weighted occurrences for each country and discipline
features = df.groupby(['discipline', 'country_name', 'country_code', 'country_3_letter_code']).apply(
    lambda x: pd.Series({
        'weighted_first': np.sum(x['first'] * x['weight']),
        'weighted_second': np.sum(x['second'] * x['weight']),
        'weighted_third': np.sum(x['third'] * x['weight']),
        'weighted_fourth': np.sum(x['fourth'] * x['weight']),
        'weighted_fifth': np.sum(x['fifth'] * x['weight']),
    })
).reset_index()

# Define the target variables
targets = df.groupby(['discipline', 'country_name', 'country_code', 'country_3_letter_code']).sum().reset_index()
targets = targets[['discipline', 'country_name', 'country_code', 'country_3_letter_code', 'first', 'second', 'third', 'fourth', 'fifth']]

# Merge features and targets
data = pd.merge(features, targets, on=['discipline', 'country_name', 'country_code', 'country_3_letter_code'])

# Split the data into training and testing sets
X = data[['weighted_first', 'weighted_second', 'weighted_third', 'weighted_fourth', 'weighted_fifth']]
y_first = data['first']
y_second = data['second']
y_third = data['third']
y_fourth = data['fourth']
y_fifth = data['fifth']

X_train, X_test, y_first_train, y_first_test = train_test_split(X, y_first, test_size=0.2, random_state=42)
_, _, y_second_train, y_second_test = train_test_split(X, y_second, test_size=0.2, random_state=42)
_, _, y_third_train, y_third_test = train_test_split(X, y_third, test_size=0.2, random_state=42)
_, _, y_fourth_train, y_fourth_test = train_test_split(X, y_fourth, test_size=0.2, random_state=42)
_, _, y_fifth_train, y_fifth_test = train_test_split(X, y_fifth, test_size=0.2, random_state=42)

# Train the model
model_first = LinearRegression().fit(X_train, y_first_train)
model_second = LinearRegression().fit(X_train, y_second_train)
model_third = LinearRegression().fit(X_train, y_third_train)
model_fourth = LinearRegression().fit(X_train, y_fourth_train)
model_fifth = LinearRegression().fit(X_train, y_fifth_train)

# Make predictions
y_first_pred = model_first.predict(X_test)
y_second_pred = model_second.predict(X_test)
y_third_pred = model_third.predict(X_test)
y_fourth_pred = model_fourth.predict(X_test)
y_fifth_pred = model_fifth.predict(X_test)

# Evaluate the model
mse_first = mean_squared_error(y_first_test, y_first_pred)
mse_second = mean_squared_error(y_second_test, y_second_pred)
mse_third = mean_squared_error(y_third_test, y_third_pred)
mse_fourth = mean_squared_error(y_fourth_test, y_fourth_pred)
mse_fifth = mean_squared_error(y_fifth_test, y_fifth_pred)

print(f'MSE for first place predictions: {mse_first}')
print(f'MSE for second place predictions: {mse_second}')
print(f'MSE for third place predictions: {mse_third}')
print(f'MSE for fourth place predictions: {mse_fourth}')
print(f'MSE for fifth place predictions: {mse_fifth}')

# Make predictions for 2024
predictions_2024 = features.copy()
predictions_2024['pred_first'] = model_first.predict(features[['weighted_first', 'weighted_second', 'weighted_third', 'weighted_fourth', 'weighted_fifth']])
predictions_2024['pred_second'] = model_second.predict(features[['weighted_first', 'weighted_second', 'weighted_third', 'weighted_fourth', 'weighted_fifth']])
predictions_2024['pred_third'] = model_third.predict(features[['weighted_first', 'weighted_second', 'weighted_third', 'weighted_fourth', 'weighted_fifth']])
predictions_2024['pred_fourth'] = model_fourth.predict(features[['weighted_first', 'weighted_second', 'weighted_third', 'weighted_fourth', 'weighted_fifth']])
predictions_2024['pred_fifth'] = model_fifth.predict(features[['weighted_first', 'weighted_second', 'weighted_third', 'weighted_fourth', 'weighted_fifth']])

predictions_file_path = 'olympic_predictions_2024.csv'
predictions_2024.to_csv(predictions_file_path, index=False)

print(f"Predictions for 2024 saved to {predictions_file_path}")