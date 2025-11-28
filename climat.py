import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
st.set_page_config(page_title="Mission Climat 4ème", page_icon="🌍", layout="centered")

# --- STYLE ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    .stApp { background-color: #FAFAFA; }
</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.title("🌍 Mission Climat : Comprendre l'Effet de Serre")
st.markdown("Bienvenue dans ton laboratoire virtuel.")

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["💡 Comprendre", "🎛️ Simulateur", "❓ Quiz"])

# --- ONGLET 1 : COMPRENDRE ---
with tab1:
    st.header("C'est quoi l'Effet de Serre ?")
    st.info("Imagine que la Terre porte un manteau invisible (l'atmosphère).")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        1. Le **Soleil** chauffe la Terre.
        2. La Terre renvoie cette chaleur vers l'espace.
        3. Les **Gaz à Effet de Serre (GES)** piègent une partie de cette chaleur.
        
        👉 **Sans eux** : -18°C (Glacial).
        👉 **Avec trop de CO2** : La Terre a de la fièvre.
        """)
    with col_b:
        # Affichage d'un diagramme simple si possible, sinon texte visuel
        st.markdown("### ☀️ ➡️ 🌍 ➡️ 🔥 (Piégé)")

# --- ONGLET 2 : SIMULATEUR ---
with tab2:
    st.header("🎛️ Le Laboratoire du Futur")
    st.write("Fais glisser le curseur pour changer la quantité de CO2 dans l'air.")
    
    # --- 1. LE REGLAGE ---
    # Slider pour le CO2
    co2 = st.slider("Concentration de CO2 (ppm)", 
                    min_value=280, max_value=1000, value=420, step=10)
    
    # --- 2. LE CALCUL (Modèle simplifié sensibilité climatique) ---
    # Référence pré-industrielle (280ppm = ~13.7°C)
    # Formule : Delta T = 3 * log2(CO2 / 280)
    temp_base_1850 = 13.7
    rechauffement = 3 * np.log2(co2 / 280)
    temp_finale = temp_base_1850 + rechauffement
    
    # Affichage des chiffres
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Température en 2100", f"{temp_finale:.1f} °C", delta=f"+{rechauffement:.1f} °C")
    with col2:
        if co2 <= 350:
            st.success("✅ Climat stable")
        elif co2 < 450:
            st.warning("⚠️ Attention")
        else:
            st.error("🔥 Urgence")

    # --- 3. LE GRAPHIQUE CORRIGÉ (Matplotlib) ---
    st.write("### 📈 Projection de la température")
    
    # Création des données pour la courbe
    annees = [2024, 2050, 2100]
    # On part de 15°C aujourd'hui vers la temp_finale en 2100
    temp_2024 = 15.0
    # On lisse la courbe
    temps = [temp_2024, temp_2024 + (temp_finale - temp_2024)*0.6, temp_finale]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Tracer la courbe
    ax.plot(annees, temps, marker='o', color='red', linewidth=3, label='Température')
    
    # --- CORRECTION IMPORTANTE : Fixer l'échelle verticale ---
    # On force l'axe Y à aller de 13°C à 22°C. 
    # Comme ça, si la courbe monte, on le voit vraiment !
    ax.set_ylim(13, 22)
    ax.set_ylabel("Température moyenne (°C)")
    ax.set_title("Evolution future si on garde ce taux de CO2")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Zone de confort (la normale historique)
    ax.axhspan(13.5, 14.5, color='green', alpha=0.1, label='Climat historique')
    ax.legend()
    
    st.pyplot(fig)
    st.caption("La zone verte représente le climat qu'ont connu nos grands-parents.")

# --- ONGLET 3 : QUIZ ---
with tab3:
    st.header("❓ Quiz rapide")
    rep = st.radio("Si on augmente le CO2, que fait la courbe de température ?", 
                   ["Elle descend", "Elle reste plate", "Elle monte"])
    
    if st.button("Valider"):
        if "monte" in rep:
            st.balloons()
            st.success("Exact ! Plus de CO2 = Plus de chaleur piégée.")
        else:
            st.error("Regarde bien le simulateur : quand tu augmentes le CO2, la courbe rouge grimpe !")
