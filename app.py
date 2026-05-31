import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page de l'application
st.set_page_config(page_title="Congo Coffee Data", layout="wide", page_icon="☕")

# 2. Définition des URLs brutes (Raw) de vos fichiers sur GitHub
url_production_prix = "https://raw.githubusercontent.com/emersonmbungu2-gif/DRC-COFFEE-DATA/main/Production%20et%20prix%20du%20caf%C3%A9.xlsx"
url_data_site = "https://raw.githubusercontent.com/emersonmbungu2-gif/DRC-COFFEE-DATA/main/Data%20for%20site.xlsx"

# 3. Titre principal de la plateforme
st.title("☕ Congo Coffee Data")
st.markdown("---")

# 4. Menu latéral de navigation
st.sidebar.header("🧭 Navigation")
section = st.sidebar.radio(
    "Choisir une analyse :",
    ["Accueil & Objectifs", "Production & Prix du Café", "Modélisation (Données ARDL)"]
)

# --- SECTION 1 : ACCUEIL ---
if section == "Accueil & Objectifs":
    st.subheader("Visualisation et Analyse de la Filière Café en RDC")
    st.write(
        "Ce tableau de bord interactif centralise les données sur la production, "
        "les prix, l'inflation et le taux de change en République Démocratique du Congo. "
        "Il permet d'explorer les dynamiques du secteur et d'appuyer les analyses macroéconomiques."
    )
    st.info("💡 Utilisez le menu de gauche pour basculer entre les données de production et les variables du modèle économétrique.")

# --- SECTION 2 : PRODUCTION & PRIX ---
elif section == "Production & Prix du Café":
    st.subheader("📊 Analyse Sectorielle : Production et Évolution des Prix")
    
    # Création d'onglets pour séparer l'analyse annuelle et mensuelle
    tab1, tab2 = st.tabs(["📅 Données Annuelles", "📆 Données Mensuelles"])
    
    with tab1:
        st.markdown("### Évolution Annuelle")
        try:
            # Chargement des feuilles correspondantes
            df_ann_prod = pd.read_excel(url_production_prix, sheet_name="Annual Production")
            df_ann_price = pd.read_excel(url_production_prix, sheet_name="Annual Price")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Volume de Production Annuelle**")
                st.dataframe(df_ann_prod, use_container_width=True)
            with col2:
                st.write("**Prix Annuels**")
                st.dataframe(df_ann_price, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erreur lors du chargement des données annuelles : {e}")
            
    with tab2:
        st.markdown("### Évolution Mensuelle")
        try:
            df_mth_prod = pd.read_excel(url_production_prix, sheet_name="Monthly Production")
            df_mth_price = pd.read_excel(url_production_prix, sheet_name="Monthly Price")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Production Mensuelle**")
                st.dataframe(df_mth_prod, use_container_width=True)
            with col2:
                st.write("**Prix Mensuels**")
                st.dataframe(df_mth_price, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erreur lors du chargement des données mensuelles : {e}")

# --- SECTION 3 : DONNÉES ARDL ---
elif section == "Modélisation (Données ARDL)":
    st.subheader("📈 Variables Macroéconomiques & Modèle ARDL")
    st.write("Cette section présente les données nettoyées utilisées pour l'analyse économétrique.")
    
    try:
        # Chargement de la feuille "Data for ARDL" du fichier Data for site.xlsx
        df_ardl = pd.read_excel(url_data_site, sheet_name="Data for ARDL")
        
        st.success("Données ARDL chargées avec succès depuis GitHub !")
        st.dataframe(df_ardl, use_container_width=True)
        
        # --- AJOUT D'UN GRAPHIQUE DYNAMIQUE ---
        st.markdown("### 📊 Graphique Interactif des Variables")
        # Permet à l'étudiant ou au chercheur de choisir la variable à afficher sur l'axe Y
        colonnes_disponibles = [col for col in df_ardl.columns if col not in ['Year', 'Annee', 'Date']]
        
        if colonnes_disponibles:
            variable_choisie = st.selectbox("Sélectionnez une variable à analyser :", colonnes_disponibles)
            axe_x = 'Year' if 'Year' in df_ardl.columns else df_ardl.columns[0]
            
            fig = px.line(df_ardl, x=axe_x, y=variable_choisie, 
                          title=f"Évolution de la variable {variable_choisie} dans le temps",
                          markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erreur lors du chargement de la feuille ARDL : {e}")
  
