import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv('transactions.csv')
X = df[['amount', 'time_of_day', 'location']].values
y = df['is_fraud'].values

model = RandomForestClassifier()
model.fit(X, y)

with open('fraud_transaction_model.pkl', 'wb') as f:
    pickle.dump(model, f)