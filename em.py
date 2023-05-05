import pandas as pd
import numpy as np

# Define the column names
columns = ['Farmer ID', 'Gender', 'Age', 'Education Level', 'Marital Status',
           'Farm Size (Acres)', 'Crop Yield (kg/acre)', 'Annual Income (USD)',
           'Debt (USD)', 'Credit Score']

# Define some example data
data = {'Farmer ID': np.arange(1, 21),
        'Gender': np.random.choice(['M', 'F'], size=20),
        'Age': np.random.randint(25, 60, size=20),
        'Education Level': np.random.choice(['Primary', 'Secondary', 'Tertiary'], size=20),
        'Marital Status': np.random.choice(['Married', 'Single'], size=20),
        'Farm Size (Acres)': np.random.randint(2, 20, size=20),
        'Crop Yield (kg/acre)': np.random.randint(1000, 5000, size=20),
        'Annual Income (USD)': np.random.randint(10000, 50000, size=20),
        'Debt (USD)': np.random.randint(0, 10000, size=20),
        'Credit Score': np.random.randint(300, 850, size=20)}

# Create the DataFrame
farmers_df = pd.DataFrame(data=data, columns=columns)

def get_feature_score(feature):

    # Define the safe range for the feature
    feature_safe_ranges = {
        'Gender': ['M'],
        'Age': [range(40, 67)],
        'Education Level': ['Secondary', 'Tertiary'],
        'Marital Status': ['Married'],
        'Farm Size (Acres)': [range(10)],
        'Crop Yield (kg/acre)': [range(2000, 5000)],
        'Annual Income (USD)': [range(22000, 50000)],
        'Debt (USD)': [0, 1000]}
    
    # Determine the position of the value relative to the safe range
    if feature in feature_safe_ranges:
        safe_range = feature_safe_ranges[feature]
        if feature < safe_range[0]:
            return -1
        elif feature > safe_range[1]:
            return 1
        else:
            return 0
    else:
        if feature == 0:
            return -1
        else:
            return 1

# Example usage

age_value = get_feature_score(farmers_df.Age)
print(age_value)  # Output: 0

temperature = 37.2
temperature_value = get_feature_value("temperature", temperature)
print(temperature_value)  # Output: 0

binary_feature = 1
binary_feature_value = get_feature_value("binary_feature", binary_feature)
print(binary_feature_value)  # Output: 1
