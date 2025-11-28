import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
st.set_page_config(page_title="Enquête Climat 4ème", page_icon="🕵️", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    .stApp { background-color: #FAFAFA; }
    .success { color: green; font-weight: bold; }
    .danger { color: red; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.title("🕵️ Mission : Qui réchauffe la planète ?")
st.markdown("""
Bienvenue au laboratoire. **4 suspects** ont été identifiés dans l'atmosphère. 
Ta mission : Manipuler les concentrations de ces gaz et observer la courbe de température pour identifier les coupables.
""")

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📚 Le Dossier (Intro)", "🧪 L'Expérience (Simulateur)", "📝 Le Rapport (Conclusion)"])

# --- ONGLET 1 : COMPRENDRE ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("Le Mécanisme")
        st.write("""
        La Terre reçoit de l'énergie du Soleil. Elle essaie de renvoyer cette chaleur vers l'espace, 
        mais certains gaz bloquent cette chaleur comme une vitre de serre.
        
        C'est l'**Effet de Serre**. Sans lui, il ferait -18°C. Mais s'il est trop fort, la Terre surchauffe.
        """)
        st.info("Rends-toi dans l'onglet **'L'Expérience'** pour tester les gaz !")
    with col2:
        st.write("### Schéma de l'effet de serre")
        # Placeholder visuel pour l'explication
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Schema_effet_ de_serre.svg/1200px-Schema_effet_de_serre.svg.png", caption="Les gaz piègent les infrarouges")

# --- ONGLET 2 : SIMULATEUR ---
with tab2:
    st.header("🧪 Laboratoire de test")
    st.write("Modifie la quantité de chaque gaz et regarde si la ligne rouge bouge.")

    col_control, col_graph = st.columns([1, 2])

    with col_control:
        st.subheader("Les Suspects")
        
        # Suspect 1 : CO2
        st.markdown("### 1. Dioxyde de Carbone ($CO_2$)")
        co2 = st.slider("Concentration (ppm)", 280, 1000, 420, key="co2")
        
        # Suspect 2 : Oxygène (Innocent)
        st.markdown("### 2. Oxygène ($O_2$)")
        o2 = st.slider("Concentration (%)", 15, 30, 21, key="o2")
        
        # Suspect 3 : Méthane (Coupable puissant)
        st.markdown("### 3. Méthane ($CH_4$)")
        methane = st.slider("Unités ajoutées", 0, 100, 10, key="ch4")
        
        # Suspect 4 : Azote (Innocent)
        st.markdown("### 4. Azote ($N_2$)")
        azote = st.slider("Concentration (%)", 70, 90, 78, key="n2")

        if st.button("Réinitialiser les niveaux"):
            st.rerun()

    # --- CALCULS SCIENTIFIQUES (Simplifiés pour 4ème) ---
    with col_graph:
        # Base temperature
        temp_base = 13.7
        
        # Impact du CO2 (Logarithmique : la physique réelle)
        effet_co2 = 3 * np.log2(co2 / 280)
        
        # Impact du Méthane (Linéaire simplifié pour l'app : 1 unité = +0.05°C)
        # Le méthane réchauffe beaucoup plus que le CO2 à quantité égale
        effet_methane = methane * 0.05 
        
        # Impact Oxygène et Azote (NUL : ce ne sont pas des GES)
        effet_o2 = 0 * (o2 - 21) # On multiplie par 0 pour annuler l'effet
        effet_azote = 0 * (azote - 78)

        # Température totale
        temp_finale = temp_base + effet_co2 + effet_methane + effet_o2 + effet_azote
        
        # --- VISUALISATION ---
        st.subheader("📈 Résultat sur la température globale")
        
        # Données pour le graphique
        annees = [2024, 2050, 2100]
        # Interpolation simple vers le futur
        temps = [15.0, 15.0 + (temp_finale - 15.0)*0.5, temp_finale]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Tracer la courbe
        ax.plot(annees, temps, marker='o', color='red', linewidth=3, label='Température simulée')
        
        # Tracer la ligne de base (pré-industriel)
        ax.axhline(y=13.7, color='green', linestyle='--', label='Niveau naturel (1850)')
        
        # FIXER L'ECHELLE (Crucial pour voir l'absence d'effet de l\'O2)
        ax.set_ylim(12, 25) 
        ax.set_ylabel("Température (°C)")
        ax.set_title("Projection en 2100")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # Feedback immédiat textuel
        st.metric("Température atteinte en 2100", f"{temp_finale:.1f} °C")
        
        if temp_finale > 16:
            st.error("🔥 La température monte dangereusement !")
        elif temp_finale == 13.7:
            st.success("✅ Température naturelle stable.")

# --- ONGLET 3 : RAPPORT / QUIZ ---
with tab3:
    st.header("📝 Rapport d'enquête")
    st.write("D'après tes tests dans l'onglet précédent, coche les gaz qui font monter la température.")
    
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        check_co2 = st.checkbox("Le Dioxyde de Carbone ($CO_2$)")
        check_o2 = st.checkbox("L'Oxygène ($O_2$)")
        check_ch4 = st.checkbox("Le Méthane ($CH_4$)")
        check_n2 = st.checkbox("L'Azote ($N_2$)")
        
        if st.button("Soumettre mon rapport"):
            # Vérification
            if check_co2 and check_ch4 and not check_o2 and not check_n2:
                st.balloons()
                st.success("🏆 BRAVO ! Tu as identifié les coupables.")
                st.markdown("""
                **Explication :**
                * 🔴 **CO2 et Méthane** sont des Gaz à Effet de Serre (GES). Ils vibrent quand ils reçoivent de la chaleur et la renvoient vers le sol.
                * 🟢 **Oxygène et Azote** sont transparents pour la chaleur infrarouge. Ils ne réchauffent pas la Terre.
                """)
            elif check_o2 or check_n2:
                st.error("❌ Erreur : Tu as accusé un innocent ! Retourne tester l'Oxygène ou l'Azote, la courbe bouge-t-elle ?")
            else:
                st.warning("⚠️ Tu as oublié un coupable (il y en a 2) ou tu n'as rien coché.")

    with col_q2:
        st.info("💡 Le savais-tu ?")
        st.write("Le **Méthane** est émis par la digestion des ruminants (vaches) et les décharges. Il est 25 fois plus puissant que le CO2, mais reste moins longtemps dans l'air.")
