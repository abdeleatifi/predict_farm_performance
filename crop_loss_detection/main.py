# Importing necessary libraries
import pandas as pd
import numpy as np
import random

# Generating dummy dataset
np.random.seed(42)

crop_types = ['Wheat', 'Corn', 'Soybeans', 'Rice', 'Cotton']
num_samples = 1000

# Generating NDVI values for each crop and each time-step (52 weeks)
ndvi = []
for i in range(num_samples):
    crop_ndvi = []
    for j in range(52):
        crop_ndvi.append(random.uniform(0.1, 0.8))
    ndvi.append(crop_ndvi)

df = pd.DataFrame({
    'Crop Type': np.random.choice(crop_types, num_samples),
    'NDVI Values': ndvi,
    'Crop Loss': np.random.randint(0, 2, num_samples)
})


# Importing necessary libraries
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Separating features and labels
X = np.array(df['NDVI Values'].values.tolist())
y = df['Crop Loss'].values

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating and training Random Forest Classifier
rfc = RandomForestClassifier(n_estimators=100, random_state=42)
rfc.fit(X_train, y_train)

# Evaluating performance on test set
y_pred = rfc.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))