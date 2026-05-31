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

    st.subheader("Plateforme d'information sur la filière café en République Démocratique du Congo")

    st.write(
        """
        Congo Coffee Data est une plateforme de données économiques dédiée à la filière café en RDC.
        
        Elle vise à réduire l’asymétrie d’information en mettant à disposition des données fiables sur :
        - la production
        - les prix
        - les variables macroéconomiques liées au secteur

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
        st.markdown("Analyse des tendances annuelles")

        try:
            df_ann_prod = load_excel(URL_PRODUCTION_PRIX, "Annual Production")
            df_ann_price = load_excel(URL_PRODUCTION_PRIX, "Annual Price")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Production annuelle")
                st.dataframe(df_ann_prod, use_container_width=True)

            with col2:
                st.write("Prix annuels")
                st.dataframe(df_ann_price, use_container_width=True)

            # Graphique simple production
            x = df_ann_prod.columns[0]
            y = df_ann_prod.columns[1]

            fig = px.line(df_ann_prod, x=x, y=y)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error("Erreur lors du chargement des données annuelles")


    # -------- MENSUEL --------
    with tab2:
        st.markdown("Analyse des tendances mensuelles")

        try:
            df_mth_prod = load_excel(URL_PRODUCTION_PRIX, "Monthly Production")
            df_mth_price = load_excel(URL_PRODUCTION_PRIX, "Monthly Price")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Production mensuelle")
                st.dataframe(df_mth_prod, use_container_width=True)

            with col2:
                st.write("Prix mensuels")
                st.dataframe(df_mth_price, use_container_width=True)

        except Exception:
            st.error("Erreur lors du chargement des données mensuelles")


# ----------------------------
# SECTION 3 : ARDL
# ----------------------------
elif section == "Données macroéconomiques (ARDL)":

    st.subheader("Analyse macroéconomique de la filière café")

    try:
        df_ardl = load_excel(URL_DATA_SITE, "Data for ARDL")

        st.write("Base de données macroéconomiques")
        st.dataframe(df_ardl, use_container_width=True)

        # Nettoyage minimal
        df_ardl = df_ardl.copy()

        for col in df_ardl.columns:
            df_ardl[col] = pd.to_numeric(df_ardl[col], errors="coerce")

        df_ardl = df_ardl.dropna()

        st.markdown("Analyse temporelle")

        variables = list(df_ardl.columns)

        x_axis = variables[0]
        y_var = st.selectbox("Variable à analyser", variables[1:])

        fig = px.line(df_ardl, x=x_axis, y=y_var)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("Corrélation entre variables")

        corr = df_ardl.corr()

        fig_corr = px.imshow(corr, text_auto=True)
        st.plotly_chart(fig_corr, use_container_width=True)

    except Exception:
        st.error("Erreur lors du chargement des données ARDL")
