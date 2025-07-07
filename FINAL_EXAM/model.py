from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('dataset/tic-tac-toe.csv')

mapping = {'x': 1, 'o': -1, 'b': 0}
for col in df.columns[:-1]:  # toutes sauf 'class'
    df[col] = df[col].map(mapping)
df['class'] = df['class'].map({True: 1, False: 0})
# Cible binaire, encode True/False en 1/0
X = df.drop(columns=['class']).values
y = df['class']
print(df)
# Créer et entraîner le modèle
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)


# 💾 Sauvegarder le modèle entraîné
with open('model/tic_tac_toe_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# ✅ Pour le recharger plus tard
# with open('model/tic_tac_toe_model.pkl', 'rb') as f:
#     model = pickle.load(f)
