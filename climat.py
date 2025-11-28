import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Mission Climat 4ème", page_icon="🌍", layout="centered")

# Titre principal
st.title("🌍 Mission Climat : Comprendre l'Effet de Serre")
st.markdown("Bienvenue dans ton laboratoire virtuel. Ton but : comprendre pourquoi la Terre se réchauffe.")

# Création des onglets
tab1, tab2, tab3, tab4 = st.tabs(["💡 Comprendre", "🔍 Les Suspects (Gaz)", "🎛️ Simulateur", "❓ Quiz"])

# --- ONGLET 1 : COMPRENDRE ---
with tab1:
    st.header("C'est quoi l'Effet de Serre ?")
    
    st.info("Imagine que la Terre porte un manteau invisible. Ce manteau, c'est l'atmosphère.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        1. Le **Soleil** envoie de l'énergie (lumière) vers la Terre.
        2. La Terre chauffe et renvoie cette chaleur vers l'espace (rayons infrarouges).
        3. **MAIS**, certains gaz dans l'atmosphère piègent une partie de cette chaleur.
        
        👉 **Sans effet de serre**, il ferait **-18°C** sur Terre ! La vie serait impossible.
        👉 **Le problème**, c'est qu'on a mis un manteau *trop chaud*.
        """)
    with col2:
        # Ici, l'image serait affichée dans la vraie app
        st.markdown("### ☀️ ➡️ 🌍 ➡️ 🌡️")
        st.warning("L'effet de serre est naturel, c'est son augmentation qui est dangereuse.")

# --- ONGLET 2 : LES GAZ ---
with tab2:
    st.header("Les Principaux Gaz à Effet de Serre (GES)")
    st.markdown("Voici les molécules responsables. On les appelle les **GES**.")
    
    col_gas1, col_gas2, col_gas3 = st.columns(3)
    
    with col_gas1:
        st.subheader("Dioxyde de Carbone")
        st.latex(r"CO_2")
        st.markdown("**Source :** Respiration, volcans, mais surtout **voitures, usines, chauffage**.")
        st.metric(label="Durée de vie", value="~100 ans")
        
    with col_gas2:
        st.subheader("Méthane")
        st.latex(r"CH_4")
        st.markdown("**Source :** Digestion des vaches (élevage), rizières, décharges.")
        st.metric(label="Pouvoir réchauffant", value="25x CO2")

    with col_gas3:
        st.subheader("Protoxyde d'Azote")
        st.latex(r"N_2O")
        st.markdown("**Source :** Engrais agricoles, industrie chimique.")
        st.metric(label="Pouvoir réchauffant", value="300x CO2")

# --- ONGLET 3 : SIMULATEUR ---
with tab3:
    st.header("🎛️ Le Laboratoire du Futur")
    st.markdown("Fais varier la concentration de $CO_2$ dans l'atmosphère et observe la température moyenne de la Terre.")
    
    # Slider pour simuler la concentration de CO2 (en ppm - parties par million)
    co2_ppm = st.slider("Concentration de CO2 (ppm)", min_value=280, max_value=1000, value=420, step=10)
    
    # Calcul simplifié pour la simulation (Formule pédagogique approximative)
    # Sensibilité climatique : doublement du CO2 = +3°C environ
    base_temp = 14.5 # Température moyenne de base vers 1960
    warming = 3 * np.log2(co2_ppm / 280)
    current_temp = base_temp + warming
    
    col_sim1, col_sim2 = st.columns([1, 2])
    
    with col_sim1:
        st.metric(label="Température Moyenne", value=f"{current_temp:.1f} °C", delta=f"+{warming:.1f} °C")
        if co2_ppm > 450:
            st.error("⚠️ Attention : Seuil critique dépassé !")
        elif co2_ppm > 350:
            st.warning("⚠️ Niveau élevé")
        else:
            st.success("✅ Niveau pré-industriel")
            
    with col_sim2:
        # Graphique simple
        years = np.arange(1850, 2100)
        # Création d'une courbe fictive basée sur le choix de l'élève
        temps = [13.5 + (3 * np.log2(280 + (co2_ppm-280)*(max(0, y-1850)/250) / 280)) for y in years]
        
        chart_data = pd.DataFrame({'Année': years, 'Température (°C)': temps})
        st.line_chart(chart_data, x='Année', y='Température (°C)')
        st.caption("Projection simplifiée basée sur ton réglage.")

# --- ONGLET 4 : QUIZ ---
with tab4:
    st.header("❓ As-tu bien suivi ?")
    
    q1 = st.radio("1. Quel est le principal gaz émis par les activités humaines ?", 
                  ("L'oxygène", "Le dioxyde de carbone (CO2)", "L'hélium"))
    
    if st.button("Valider la réponse 1"):
        if "CO2" in q1:
            st.success("Bravo ! C'est bien le CO2.")
        else:
            st.error("Raté ! L'oxygène nous aide à respirer, c'est le CO2 qui réchauffe.")

    st.markdown("---")
    
    q2 = st.radio("2. Sans effet de serre, quelle serait la température sur Terre ?", 
                  ("25°C", "0°C", "-18°C"))
    
    if st.button("Valider la réponse 2"):
        if "-18°C" in q2:
            st.success("Exact ! La Terre serait un glaçon géant.")
        else:
            st.error("Non, il ferait beaucoup plus froid !")

st.markdown("---")
st.caption("Application générée pour un cours de Sciences Physiques / SVT - Niveau 4ème")