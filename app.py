import streamlit as st
import pandas as pd
import ast

# charger le fichier csv contenant les regles d'association
@st.cache_data
def load_rules():
    rules = pd.read_csv("association_rules.csv")


    ## Transformation des chaines en liste
    rules['antecedents']=rules['antecedents'].apply(ast.literal_eval)
    rules['consequents']=rules['consequents'].apply(ast.literal_eval)

    return rules


# Appel de la fonction de chargement des donnees 
rules = load_rules()

# Titre de la page
st.title(" RECOMMENDATION D'ARTICLES")

unique_items=sorted(set(item for ant in rules['antecedents'] for item in ant))
# Liste deroulante pour le choix d'articles
selected_item=st.selectbox("Selectionner un produits", unique_items)


# curseur pour definir confiance et le lift
min_conf=st.slider("Confiance minimum", 0.0, 1.0, 0.5, 0.05)
min_lift=st.slider("Lift minimum", 0.0, 1.0, 0.5, 0.05)

# Filter les regles en fonction de l'elelment selectionner
filtered_rules = rules [
    rules['antecedents'].apply(lambda x : selected_item in x) & 
    (rules['confidence'] >= min_conf) & 
    (rules['lift'] >= min_lift ) ]


# Retirer les recommandantions dupliquées basé sur les consequents
filtered_rules=filtered_rules.sort_values(by= 'confidence', ascending=False)
filtered_rules['consequents_set']=filtered_rules['consequents'].apply(lambda x : frozenset(x))
filtered_rules=filtered_rules.drop_duplicates(subset='consequents_set')

# Afichage des recommendation dans l'application
if not filtered_rules.empty : 
    st.subheader(f"Recpmmendations pour : {selected_item}")
    for _, row in filtered_rules.iterrows():
        recommended_items= ', '.join(row['consequents'])
        st.markdown(f"""
        - Produit recommendé : {recommended_items}
        - Confiance : {row['confidence']:.2f}
        - Lift : {row['lift']:.2f}
        """)
else :
    st.warning("Aucun recommandation")
        


                                     
                                     
                                     




