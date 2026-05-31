import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# CONFIGURATION GÉNÉRALE
# ----------------------------
st.set_page_config(
    page_title="Congo Coffee Data",
    layout="wide"
)

# ----------------------------
# SOURCES DE DONNÉES
# ----------------------------
URL_PRODUCTION_PRIX = "https://raw.githubusercontent.com/emersonmbungu2-gif/DRC-COFFEE-DATA/main/Production%20et%20prix%20du%20caf%C3%A9.xlsx"
URL_DATA_SITE = "https://raw.githubusercontent.com/emersonmbungu2-gif/DRC-COFFEE-DATA/main/Data%20for%20site.xlsx"


# ----------------------------
# TITRE
# ----------------------------
st.title("Congo Coffee Data")
st.markdown("---")


# ----------------------------
# NAVIGATION
# ----------------------------
st.sidebar.header("Navigation")

section = st.sidebar.radio(
    "Choisir une section",
    [
        "Accueil",
        "Production et Prix",
        "Données macroéconomiques (ARDL)"
    ]
)


# ----------------------------
# FONCTIONS DE CHARGEMENT
# ----------------------------
@st.cache_data
def load_excel(url, sheet):
    return pd.read_excel(url, sheet_name=sheet)


# ----------------------------
# SECTION 1 : ACCUEIL
# ----------------------------
if section == "Accueil":

    st.write(
        """
        Congo Coffee Data est une plateforme de données économiques dédiée à la filière café en RDC.
        
        Elle vise à réduire l’asymétrie d’information en mettant à disposition des données fiables sur :
        - la production ;
        - les prix ;
        - les variables macroéconomiques liées au secteur.

        La plateforme s’adresse aux producteurs, acheteurs, investisseurs, institutions publiques et chercheurs.
        """
    )

    st.info(
        "Cette plateforme est conçue comme un outil d’aide à la décision et de transparence du marché."
    )


# ----------------------------
# SECTION 2 : PRODUCTION ET PRIX
# ----------------------------
elif section == "Production et Prix":

    st.subheader("Analyse de la production et des prix du café")

    tab1, tab2 = st.tabs(["Données annuelles", "Données mensuelles"])

    # -------- ANNUEL --------
    with tab1:
        st.markdown("### Analyse des tendances annuelles")

        try:
            df_ann_prod = load_excel(URL_PRODUCTION_PRIX, "Annual Production")
            df_ann_price = load_excel(URL_PRODUCTION_PRIX, "Annual Price")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Production annuelle (en tonnes)**")
                st.dataframe(df_ann_prod, use_container_width=True)

            with col2:
                st.write("**Prix annuels ($/kg)**")
                st.dataframe(df_ann_price, use_container_width=True)

            # --- NETTOYAGE ET GRAPH_ANNUEL ---
            # On ignore la ligne des unités pour le graphique
            df_graph_ann = df_ann_prod.copy()
            df_graph_ann[df_graph_ann.columns[0]] = pd.to_numeric(df_graph_ann[df_graph_ann.columns[0]], errors='coerce')
            df_graph_ann = df_graph_ann.dropna(subset=[df_graph_ann.columns[0]])
            
            x = df_graph_ann.columns[0]
            # On utilise le 'Total' si disponible, sinon la 2ème colonne
            y = 'Total' if 'Total' in df_graph_ann.columns else df_graph_ann.columns[1]

            fig = px.line(df_graph_ann, x=x, y=y, title=f"Évolution de la production annuelle globale ({y})")
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du chargement des données annuelles : {e}")


    # -------- MENSUEL --------
    with tab2:
        st.markdown("### Analyse des tendances mensuelles")

        try:
            df_mth_prod = load_excel(URL_PRODUCTION_PRIX, "Monthly Production")
            df_mth_price = load_excel(URL_PRODUCTION_PRIX, "Monthly Price")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Production mensuelle (en tonnes)**")
                st.dataframe(df_mth_prod, use_container_width=True)

            with col2:
                st.write("**Prix mensuels ($/kg)**")
                st.dataframe(df_mth_price, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du chargement des données mensuelles : {e}")


# ----------------------------
# SECTION 3 : ARDL
# ----------------------------
elif section == "Données macroéconomiques (ARDL)":

    st.subheader("Analyse macroéconomique de la filière café")

    try:
        df_ardl = load_excel(URL_DATA_SITE, "Data for ARDL")

        st.write("### Base de données macroéconomiques brute")
        st.dataframe(df_ardl, use_container_width=True)

        # --- NETTOYAGE SÉCURISÉ POUR L'ANALYSE ---
        df_clean = df_ardl.copy()
        
        # 1. Sauvegarder le nom de la première colonne (Période / Année)
        col_temps = df_clean.columns[0]
        
        # 2. Convertir la colonne temporelle en numérique et supprimer la ligne d'unités textuelles
        df_clean[col_temps] = pd.to_numeric(df_clean[col_temps], errors="coerce")
        df_clean = df_clean.dropna(subset=[col_temps])

        # 3. Convertir toutes les autres colonnes de variables en numérique
        for col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        
        df_clean = df_clean.dropna()

        # --- GRAPHIQUE TEMPOREL ---
        st.markdown("### Analyse temporelle")
        variables = list(df_clean.columns)

        x_axis = variables[0]
        y_var = st.selectbox("Sélectionner la variable à analyser", variables[1:])

        fig = px.line(df_clean, x=x_axis, y=y_var, title=f"Trajectoire de la variable : {y_var}")
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
        st.error(f"Erreur lors du traitement des données ARDL : {e}")
