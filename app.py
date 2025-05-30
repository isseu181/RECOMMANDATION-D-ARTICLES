import streamlit as st
import pandas as pd
import ast

# Config de la page
st.set_page_config(page_title="Recommandation d'Articles", layout="centered")

st.title("🛒 Recommandation d'Articles Basée sur les Règles d'Association")

# Fonction de chargement des règles
@st.cache_data
def load_rules():
    rules = pd.read_csv("association_rules.csv")

    # Convertir les colonnes de chaînes vers des listes
    rules['antecedents'] = rules['antecedents'].apply(ast.literal_eval)
    rules['consequents'] = rules['consequents'].apply(ast.literal_eval)

    return rules

# Charger les règles
rules = load_rules()

# Extraire les articles uniques
unique_items = sorted(set(item for ant in rules['antecedents'] for item in ant))

# Interface utilisateur : sélection d'un produit
selected_item = st.selectbox("🧾 Sélectionnez un produit :", unique_items)

# Interface utilisateur : sliders pour les filtres
min_conf = st.slider("🔒 Confiance minimale", 0.0, 1.0, 0.5, 0.05)
min_lift = st.slider("📈 Lift minimal", 0.0, 5.0, 1.0, 0.1)

# Filtrer les règles selon les critères
filtered_rules = rules[
    rules['antecedents'].apply(lambda x: selected_item in x) &
    (rules['confidence'] >= min_conf) &
    (rules['lift'] >= min_lift)
]

# Supprimer les doublons basés sur les "consequents"
filtered_rules = filtered_rules.sort_values(by='confidence', ascending=False)
filtered_rules['consequents_set'] = filtered_rules['consequents'].apply(lambda x: frozenset(x))
filtered_rules = filtered_rules.drop_duplicates(subset='consequents_set')

# Affichage des recommandations
if not filtered_rules.empty:
    st.subheader(f"✅ Recommandations pour : `{selected_item}`")
    for _, row in filtered_rules.iterrows():
        recommended_items = ', '.join(row['consequents'])
        st.markdown(f"""
        - **Produit recommandé :** {recommended_items}  
        - **Confiance :** {row['confidence']:.2f}  
        - **Lift :** {row['lift']:.2f}
        """)
else:
    st.warning("⚠️ Aucune recommandation ne correspond à vos critères.")
