import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# CONFIGURATION GÉNÉRALE
# ----------------------------
st.set_page_config(
    page_title="Congo Coffee Data",
    layout="wide",
    page_icon="☕"
)

# --- INJECTION CSS POUR RENDRE LE SITE TRÈS BEAU ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Application de la police globale */
        html, body, [data-testid="stSidebarView"] *, .main * {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Style du conteneur de titre principal */
        .header-container {
            background: linear-gradient(135deg, #4A2E2B 0%, #2E1A18 100%);
            padding: 40px;
            border-radius: 16px;
            color: #FFFFFF;
            margin-bottom: 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }
        
        .main-title {
            font-size: 46px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }
        
        .section-subtitle {
            font-size: 19px;
            color: #D2C4C1;
            font-weight: 300;
            line-height: 1.4;
        }
        
        /* Style des cartes d'indicateurs (KPI) */
        .kpi-box {
            background-color: #FDFBF7;
            padding: 25px 20px;
            border-radius: 14px;
            border: 1px solid #EFEBE4;
            border-top: 4px solid #8B5A2B;
            box-shadow: 0 4px 12px rgba(74,46,43,0.03);
            text-align: center;
            transition: transform 0.2s;
        }
        .kpi-box:hover {
            transform: translateY(-2px);
        }
        
        .kpi-value {
            font-size: 32px;
            font-weight: 700;
            color: #4A2E2B;
            margin-bottom: 5px;
        }
        
        .kpi-label {
            font-size: 13px;
            color: #8A7A78;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 500;
        }
        
        /* Titres de sections */
        h3, h2, h1 {
            color: #4A2E2B !important;
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allowed_html=True)

# ----------------------------
# SOURCES DE DONNÉES
# ----------------------------
URL_PRODUCTION_PRIX = "https://raw.githubusercontent.com/emersonmbungu2-gif/DRC-COFFEE-DATA/main/Production%20et%20prix%20du%20caf%C3%A9.xlsx"
URL_DATA_SITE = "https://raw.githubusercontent.com/emersonmbungu2-gif/DRC-COFFEE-DATA/main/Data%20for%20site.xlsx"

# ----------------------------
# FONCTIONS DE CHARGEMENT
# ----------------------------
@st.cache_data
def load_excel(url, sheet):
    return pd.read_excel(url, sheet_name=sheet)

# ----------------------------
# NAVIGATION (Barre latérale)
# ----------------------------
st.sidebar.markdown("<h3 style='color: #4A2E2B; margin-bottom:20px;'>Options d'analyse</h3>", unsafe_allowed_html=True)
section = st.sidebar.radio(
    "Navigation principale",
    [
        "Accueil & Objectifs",
        "Analyse de la Production & Prix",
        "Modélisation Macroéconomique (ARDL)"
    ]
)

# ----------------------------
# EN-TÊTE DESIGN FIXE
# ----------------------------
st.markdown("""
    <div class='header-container'>
        <div class='main-title'>Congo Coffee Data</div>
        <div class='section-subtitle'>Observatoire analytique et macroéconomique de la filière café en République Démocratique du Congo</div>
    </div>
""", unsafe_allowed_html=True)

# ----------------------------
# SECTION 1 : ACCUEIL
# ----------------------------
if section == "Accueil & Objectifs":
    
    # Image principale haute définition (Plantation)
    st.image(
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=2078&auto=format&fit=crop", 
        caption="Séchage traditionnel et traitement des cerises de café",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allowed_html=True)
    
    col_intro, col_img_side = st.columns([3, 2])
    
    with col_intro:
        st.markdown("### Introduction et contexte")
        st.write(
            """
            **Congo Coffee Data** est un outil d'analyse et de centralisation statistique dédié à l'étude de la filière café en RDC. 
            Dans un contexte de redynamisation des filières agricoles d'exportation, cette plateforme vise à briser l'asymétrie 
            d'information en fournissant des séries temporelles historiques épurées.
            
            L'architecture de l'application s'articule autour de trois dimensions :
            - **La dynamique de l'offre** via le suivi des volumes de production (Robusta et Arabica).
            - **La viabilité financière** à travers les structures de prix sur le marché mondial.
            - **La stabilité macroéconomique** par l'intégration des variables de change, d'inflation et de cointégration.
            """
        )
        st.info("Ce projet est conçu pour servir de support aux chercheurs, décideurs publics et analystes du secteur agricole.")

    with col_img_side:
        st.image(
            "https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=1961&auto=format&fit=crop",
            use_container_width=True
        )

# ----------------------------
# SECTION 2 : PRODUCTION ET PRIX
# ----------------------------
elif section == "Analyse de la Production & Prix":

    st.markdown("### Évolution sectorielle de la filière")
    
    tab1, tab2 = st.tabs(["📊 Séries Annuelles", "📈 Évolutions Mensuelles"])

    # -------- ANNUEL --------
    with tab1:
        try:
            df_ann_prod = load_excel(URL_PRODUCTION_PRIX, "Annual Production")
            df_ann_price = load_excel(URL_PRODUCTION_PRIX, "Annual Price")

            # Blocs d'indicateurs clés (KPI) stylisés
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.markdown("<div class='kpi-box'><div class='kpi-value'>1994 - 2023</div><div class='kpi-label'>Séries Temporelles</div></div>", unsafe_allowed_html=True)
            with kpi2:
                st.markdown("<div class='kpi-box'><div class='kpi-value'>62 552 t</div><div class='kpi-label'>Production Pic (1994)</div></div>", unsafe_allowed_html=True)
            with kpi3:
                st.markdown("<div class='kpi-box'><div class='kpi-value'>5.91 $/kg</div><div class='kpi-label'>Prix Max Arabica (2022)</div></div>", unsafe_allowed_html=True)

            st.markdown("<br>", unsafe_allowed_html=True)

            # Nettoyage et graphique
            df_graph_ann = df_ann_prod.copy()
            df_graph_ann[df_graph_ann.columns[0]] = pd.to_numeric(df_graph_ann[df_graph_ann.columns[0]], errors='coerce')
            df_graph_ann = df_graph_ann.dropna(subset=[df_graph_ann.columns[0]])
            
            x = df_graph_ann.columns[0]
            y = 'Total' if 'Total' in df_graph_ann.columns else df_graph_ann.columns[1]

            fig = px.line(df_graph_ann, x=x, y=y, title="Évolution à long terme de la production globale (en tonnes)")
            fig.update_traces(line_color='#8B5A2B', line_width=3)
            fig.update_layout(template="plotly_white", font_family="Plus Jakarta Sans")
            st.plotly_chart(fig, use_container_width=True)

            # Tableaux côte à côte
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Volumes de production annuelle")
                st.dataframe(df_ann_prod, use_container_width=True)
            with col2:
                st.markdown("#### Évolution des prix annuels")
                st.dataframe(df_ann_price, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du traitement des données annuelles : {e}")

    # -------- MENSUEL --------
    with tab2:
        try:
            df_mth_prod = load_excel(URL_PRODUCTION_PRIX, "Monthly Production")
            df_mth_price = load_excel(URL_PRODUCTION_PRIX, "Monthly Price")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Suivi mensuel des volumes")
                st.dataframe(df_mth_prod, use_container_width=True)
            with col2:
                st.markdown("#### Suivi mensuel des cours ($/kg)")
                st.dataframe(df_mth_price, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du traitement des données mensuelles : {e}")

# ----------------------------
# SECTION 3 : ARDL
# ----------------------------
elif section == "Modélisation Macroéconomique (ARDL)":

    st.markdown("### Analyse Économétrique des Variables du Modèle")

    try:
        df_ardl = load_excel(URL_DATA_SITE, "Data for ARDL")

        # Nettoyage strict
        df_clean = df_ardl.copy()
        col_temps = df_clean.columns[0]
        df_clean[col_temps] = pd.to_numeric(df_clean[col_temps], errors="coerce")
        df_clean = df_clean.dropna(subset=[col_temps])

        for col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        df_clean = df_clean.dropna()

        # Menu déroulant de sélection
        variables = list(df_clean.columns)
        x_axis = variables[0]
        
        st.markdown("#### Graphique dynamique des indicateurs")
        y_var = st.selectbox("Choisir la variable macroéconomique à projeter :", variables[1:])

        fig = px.line(df_clean, x=x_axis, y=y_var)
        fig.update_traces(line_color='#4A2E2B', line_width=3)
        fig.update_layout(template="plotly_white", font_family="Plus Jakarta Sans")
        st.plotly_chart(fig, use_container_width=True)

        # Structure du bas : Corrélation et Données nettoyées
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.markdown("#### Matrice de corrélation linéaire (Pearson)")
            colonnes_calcul = [c for c in df_clean.columns if c != col_temps]
            corr = df_clean[colonnes_calcul].corr()

            fig_corr = px.imshow(
                corr, 
                text_auto=".2f", 
                color_continuous_scale="Brwnyl"
            )
            fig_corr.update_layout(template="plotly_white", font_family="Plus Jakarta Sans")
            st.plotly_chart(fig_corr, use_container_width=True)
            
        with c_right:
            st.markdown("#### Échantillon des données épurées (ARDL)")
            st.dataframe(df_clean, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur lors du traitement analytique de la feuille ARDL : {e}")
