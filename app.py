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

# --- INJECTION CSS POUR LA POLICE ET LE DESIGN ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif !important;
        }
        
        .main-title {
            font-size: 42px;
            font-weight: 700;
            color: #4A2E2B;
            margin-bottom: 5px;
        }
        
        .section-subtitle {
            font-size: 18px;
            color: #7A6361;
            margin-bottom: 25px;
            font-weight: 300;
        }
        
        .kpi-box {
            background-color: #FDFBF7;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #8B5A2B;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            text-align: center;
        }
        
        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #8B5A2B;
        }
        
        .kpi-label {
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
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
st.sidebar.markdown("<h2 style='color: #4A2E2B; font-weight:600;'>Congo Coffee</h2>", unsafe_allowed_html=True)
section = st.sidebar.radio(
    "Navigation principale",
    [
        "Accueil & Objectifs",
        "Analyse de la Production & Prix",
        "Modélisation Macroéconomique (ARDL)"
    ]
)

# ----------------------------
# EN-TÊTE FIXE POUR LE SITE
# ----------------------------
st.markdown("<div class='main-title'>Congo Coffee Data</div>", unsafe_allowed_html=True)
st.markdown("<div class='section-subtitle'>Observatoire de la dynamique de la filière café en République Démocratique du Congo</div>", unsafe_allowed_html=True)
st.markdown("---")

# ----------------------------
# SECTION 1 : ACCUEIL
# ----------------------------
if section == "Accueil & Objectifs":
    
    # Image de couverture de haute qualité (Plantation de café)
    st.image(
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=2078&auto=format&fit=crop", 
        caption="Plantation et traitement des cerises de café",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allowed_html=True)
    
    col_intro, col_img_side = st.columns([3, 2])
    
    with col_intro:
        st.markdown("<h3 style='color: #4A2E2B;'>Présentation du projet</h3>", unsafe_allowed_html=True)
        st.write(
            """
            **Congo Coffee Data** est une plateforme de recherche et d'analyse économique dédiée à la filière café en RDC. 
            Dans un contexte de reconstruction des chaînes de valeur agricoles, elle vise à réduire l’asymétrie d'information 
            en mettant à la disposition des chercheurs, décideurs publics et investisseurs des séries temporelles fiables.
            
            Le portail structure l'analyse autour de trois piliers fondamentaux :
            - **La dynamique de production** (Robusta et Arabica)
            - **La transmission des prix** des marchés internationaux vers la sphère locale
            - **L'environnement macroéconomique** global à travers les modèles de cointégration.
            """
        )
        st.info("Cette plateforme a été construite pour servir d'outil d'aide à la décision et de transparence pour le secteur agricole.")

    with col_img_side:
        # Deuxième image contextuelle (Grains de café récoltés)
        st.image(
            "https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=1961&auto=format&fit=crop",
            use_container_width=True
        )

# ----------------------------
# SECTION 2 : PRODUCTION ET PRIX
# ----------------------------
elif section == "Analyse de la Production & Prix":

    st.markdown("<h3 style='color: #4A2E2B;'>Analyse Sectorielle : Production et Prix</h3>", unsafe_allowed_html=True)
    
    tab1, tab2 = st.tabs(["📊 Séries Annuelles", "📈 Évolutions Mensuelles"])

    # -------- ANNUEL --------
    with tab1:
        try:
            df_ann_prod = load_excel(URL_PRODUCTION_PRIX, "Annual Production")
            df_ann_price = load_excel(URL_PRODUCTION_PRIX, "Annual Price")

            # Cartes d'indicateurs (KPI) stylisées avec notre CSS
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.markdown("<div class='kpi-box'><div class='kpi-value'>1994 - 2023</div><div class='kpi-label'>Période couverte</div></div>", unsafe_allowed_html=True)
            with kpi2:
                st.markdown("<div class='kpi-box'><div class='kpi-value'>62 552 t</div><div class='kpi-label'>Production Max (1994)</div></div>", unsafe_allowed_html=True)
            with kpi3:
                st.markdown("<div class='kpi-box'><div class='kpi-value'>5,91 $/kg</div><div class='kpi-label'>Prix Max Arabica (2022)</div></div>", unsafe_allowed_html=True)

            st.markdown("<br>", unsafe_allowed_html=True)

            # Graphique interactif épuré (Thème blanc)
            df_graph_ann = df_ann_prod.copy()
            df_graph_ann[df_graph_ann.columns[0]] = pd.to_numeric(df_graph_ann[df_graph_ann.columns[0]], errors='coerce')
            df_graph_ann = df_graph_ann.dropna(subset=[df_graph_ann.columns[0]])
            
            x = df_graph_ann.columns[0]
            y = 'Total' if 'Total' in df_graph_ann.columns else df_graph_ann.columns[1]

            fig = px.line(df_graph_ann, x=x, y=y, title=f"Évolution temporelle de la production globale (en tonnes)")
            fig.update_traces(line_color='#8B5A2B', line_width=3)
            fig.update_layout(template="plotly_white", font_family="Inter")
            st.plotly_chart(fig, use_container_width=True)

            # Tableaux de données
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### Base de production annuelle")
                st.dataframe(df_ann_prod, use_container_width=True)
            with col2:
                st.markdown("##### Structure des prix annuels")
                st.dataframe(df_ann_price, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du chargement des données annuelles : {e}")

    # -------- MENSUEL --------
    with tab2:
        try:
            df_mth_prod = load_excel(URL_PRODUCTION_PRIX, "Monthly Production")
            df_mth_price = load_excel(URL_PRODUCTION_PRIX, "Monthly Price")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### Suivi mensuel de la production")
                st.dataframe(df_mth_prod, use_container_width=True)
            with col2:
                st.markdown("##### Fluctuations mensuelles des prix")
                st.dataframe(df_mth_price, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du chargement des données mensuelles : {e}")

# ----------------------------
# SECTION 3 : ARDL
# ----------------------------
elif section == "Modélisation Macroéconomique (ARDL)":

    st.markdown("<h3 style='color: #4A2E2B;'>Exploration Économétrique : Modèle de Co-intégration</h3>", unsafe_allowed_html=True)

    try:
        df_ardl = load_excel(URL_DATA_SITE, "Data for ARDL")

        # Nettoyage
        df_clean = df_ardl.copy()
        col_temps = df_clean.columns[0]
        df_clean[col_temps] = pd.to_numeric(df_clean[col_temps], errors="coerce")
        df_clean = df_clean.dropna(subset=[col_temps])

        for col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        df_clean = df_clean.dropna()

        # Sélection interactive de la variable avec un style épuré
        variables = list(df_clean.columns)
        x_axis = variables[0]
        
        st.markdown("##### Trajectoire historique des variables du modèle")
        y_var = st.selectbox("Sélectionner l'indicateur macroéconomique à tracer :", variables[1:])

        fig = px.line(df_clean, x=x_axis, y=y_var)
        fig.update_traces(line_color='#4A2E2B', line_width=2.5)
        fig.update_layout(template="plotly_white", font_family="Inter")
        st.plotly_chart(fig, use_container_width=True)

        # Grille basse : Matrice de corrélation + Tableau de données
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.markdown("##### Matrice de corrélation linéaire de Pearson")
            colonnes_calcul = [c for c in df_clean.columns if c != col_temps]
            corr = df_clean[colonnes_calcul].corr()

            fig_corr = px.imshow(
                corr, 
                text_auto=".2f", 
                color_continuous_scale="Blugrn",
            )
            fig_corr.update_layout(template="plotly_white", font_family="Inter")
            st.plotly_chart(fig_corr, use_container_width=True)
            
        with c_right:
            st.markdown("##### Échantillon de données (Data for ARDL)")
            st.dataframe(df_clean, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur lors du traitement des données ARDL : {e}")
            
