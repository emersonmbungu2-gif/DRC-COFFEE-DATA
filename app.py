import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page (Style épuré et académique)
st.set_page_config(page_title="Congo Coffee Data", layout="wide")

# 2. Définition des URLs brutes (Raw) GitHub
url_production_prix = "https://raw.githubusercontent.com/emersonmbungu2-gif/DRC-COFFEE-DATA/main/Production%20et%20prix%20du%20caf%C3%A9.xlsx"
url_data_site = "https://raw.githubusercontent.com/emersonmbungu2-gif/DRC-COFFEE-DATA/main/Data%20for%20site.xlsx"

# 3. Titre de la plateforme
st.title("Congo Coffee Data")
st.markdown("##### Plateforme d'analyse macroéconomique et sectorielle de la filière café en RDC")
st.markdown("---")

# 4. Barre latérale de navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Sélectionner un module :",
    ["Présentation du Projet", "Analyse de la Production et des Prix", "Modélisation et Corrélations (ARDL)"]
)

# --- SECTION 1 : PRÉSENTATION ---
if section == "Présentation du Projet":
    st.header("Objectifs de la plateforme")
    st.write(
        "Ce tableau de bord interactif centralise les données relatives à la production, "
        "aux prix, à l'inflation et au taux de change en République Démocratique du Congo. "
        "Conçu comme un outil d'appui à la recherche économique, il permet d'explorer les dynamiques "
        "sectorielles et d'analyser les tendances structurelles de la filière."
    )
    st.info("Utilisez le menu latéral pour naviguer entre les analyses statistiques et les données de modélisation.")

# --- SECTION 2 : PRODUCTION & PRIX ---
elif section == "Analyse de la Production et des Prix":
    st.header("Analyse Sectorielle : Évolution de la Production et des Prix")
    
    tab1, tab2 = st.tabs(["Données Annuelles", "Données Mensuelles"])
    
    with tab1:
        try:
            df_ann_prod = pd.read_excel(url_production_prix, sheet_name="Annual Production")
            df_ann_price = pd.read_excel(url_production_prix, sheet_name="Annual Price")
            
            # Nettoyage rapide des lignes de sous-titres vides si elles existent
            df_ann_prod = df_ann_prod.dropna(subset=[df_ann_prod.columns[0]])
            
            # Graphique interactif de la production annuelle (Total)
            col_x_prod = df_ann_prod.columns[0]  # Période / Année
            col_y_prod = 'Total' if 'Total' in df_ann_prod.columns else df_ann_prod.columns[1]
            
            fig_prod = px.line(df_ann_prod, x=col_x_prod, y=col_y_prod, 
                               title="Évolution de la production annuelle globale de café (en tonnes)", markers=True)
            fig_prod.update_layout(template="plotly_white")
            st.plotly_chart(fig_prod, use_container_width=True)
            
            # Affichage des données en deux colonnes sous le graphique
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Volume de la Production Annuelle")
                st.dataframe(df_ann_prod, use_container_width=True)
            with c2:
                st.subheader("Historique des Prix Annuels ($/kg)")
                st.dataframe(df_ann_price, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erreur lors de l'analyse des données annuelles : {e}")
            
    with tab2:
        try:
            df_mth_prod = pd.read_excel(url_production_prix, sheet_name="Monthly Production")
            df_mth_price = pd.read_excel(url_production_prix, sheet_name="Monthly Price")
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Suivi Mensuel de la Production (en tonnes)")
                st.dataframe(df_mth_prod, use_container_width=True)
            with c2:
                st.subheader("Suivi Mensuel des Prix ($/kg)")
                st.dataframe(df_mth_price, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erreur lors de l'analyse des données mensuelles : {e}")

# --- SECTION 3 : DONNÉES ARDL & STATISTIQUES ---
elif section == "Modélisation et Corrélations (ARDL)":
    st.header("Variables Macroéconomiques et Exploration Économétrique")
    
    try:
        df_ardl = pd.read_excel(url_data_site, sheet_name="Data for ARDL")
        
        # Nettoyage des lignes d'unités pour le calcul statistique (ex: la ligne contenant (t) ou ($/kg))
        # On ne garde que les lignes où la première colonne est une année numérique valide
        df_ardl[df_ardl.columns[0]] = pd.to_numeric(df_ardl[df_ardl.columns[0]], errors='coerce')
        df_ardl = df_ardl.dropna(subset=[df_ardl.columns[0]])
        
        # Convertir les autres colonnes en numérique pour éviter les conflits de calcul
        for col in df_ardl.columns:
            df_ardl[col] = pd.to_numeric(df_ardl[col], errors='coerce')
            
        # 1. Résumé statistique automatique
        st.subheader("Analyse Descriptive : Résumé statistique des variables")
        st.write("Ce tableau présente les moments clés (Moyenne, Écart-type, Minimum, Maximum) de votre série temporelle :")
        st.dataframe(df_ardl.describe(), use_container_width=True)
        
        # 2. Graphique temporel interactif
        st.subheader("Analyse Graphique Temporelle")
        colonnes_numeriques = [col for col in df_ardl.columns if col not in ['Période', 'Year', 'Annee', 'Date']]
        
        if colonnes_numeriques:
            variable_selectionnee = st.selectbox("Sélectionner la variable à tracer sur l'axe des ordonnées :", colonnes_numeriques)
            axe_temporel = df_ardl.columns[0]
            
            fig_temporal = px.line(df_ardl, x=axe_temporel, y=variable_selectionnee, 
                                   title=f"Trajectoire temporelle de la variable : {variable_selectionnee}",
                                   markers=True)
            fig_temporal.update_layout(template="plotly_white")
            st.plotly_chart(fig_temporal, use_container_width=True)
            
            # 3. Matrice de corrélation linéaire
            st.subheader("Matrice de Corrélation de Pearson")
            st.write("Analyse pré-estimatoire de l'intensité des liaisons linéaires entre vos variables macroéconomiques.")
            
            # Calcul de la matrice sur les colonnes numériques valides
            df_corr_input = df_ardl[colonnes_numeriques].dropna()
            corr_matrix = df_corr_input.corr()
            
            fig_corr = px.imshow(corr_matrix, text_auto=".2f", 
                                 title="Coefficients de corrélation linéaire",
                                 color_continuous_scale="RdBu_r", aspect="auto")
            fig_corr.update_layout(template="plotly_white")
            st.plotly_chart(fig_corr, use_container_width=True)
            
        st.subheader("Base de données complète (Data for ARDL)")
        st.dataframe(df_ardl, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier ARDL : {e}")
  
