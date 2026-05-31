import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# CONFIGURATION GÉNÉRALE
# ----------------------------
st.set_page_config(
    page_title="DRC Coffee Data",
    layout="wide",
    page_icon="☕"
)

# --- INJECTION CSS POUR LE DESIGN PROFESSIONNEL & ATTRAYANT ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        html, body, [data-testid="stSidebarView"] *, .main * {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        .header-container {
            background: linear-gradient(135deg, #4A2E2B 0%, #2E1A18 100%);
            padding: 40px;
            border-radius: 16px;
            color: #FFFFFF;
            margin-bottom: 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }
        
        .main-title {
            font-size: 44px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }
        
        .section-subtitle {
            font-size: 18px;
            color: #D2C4C1;
            font-weight: 300;
            line-height: 1.4;
        }
        
        .kpi-box {
            background-color: #FDFBF7;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #EFEBE4;
            border-top: 4px solid #8B5A2B;
            box-shadow: 0 4px 12px rgba(74,46,43,0.03);
            text-align: center;
        }
        
        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #4A2E2B;
            margin-bottom: 5px;
        }
        
        .kpi-label {
            font-size: 12px;
            color: #8A7A78;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }
        
        .news-box {
            background-color: #F4EFEA;
            padding: 25px;
            border-radius: 14px;
            border-left: 5px solid #4A2E2B;
            margin-bottom: 25px;
        }
        
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
        "Accueil & Actualités",
        "Production et Prix",
        "Données macroéconomiques (ARDL)"
    ]
)

# ----------------------------
# EN-TÊTE FIXE DU SITE
# ----------------------------
st.markdown("""
    <div class='header-container'>
        <div class='main-title'>Congo Coffee Data</div>
        <div class='section-subtitle'>Observatoire analytique et macroéconomique de la filière café en République Démocratique du Congo</div>
    </div>
""", unsafe_allowed_html=True)

# ----------------------------
# SECTION 1 : ACCUEIL & ACTUALITÉS
# ----------------------------
if section == "Accueil & Actualités":
    
    st.image(
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=2078&auto=format&fit=crop", 
        caption="Séchage traditionnel et contrôle qualité des cerises de café",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allowed_html=True)
    
    # --- AJOUT N°1 : POINT CONJONCTURE & ACTUALITÉ 2025 ---
    st.markdown("### 📰 Actualités et Conjoncture Récente")
    
    st.markdown("""
    <div class='news-box'>
        <h4 style='color: #4A2E2B; margin-top:0;'>Point de situation - Campagne 2025</h4>
        <p>La campagne caféière de l'année <b>2025</b> est marquée par une consolidation progressive des cours mondiaux combinée à des efforts structurels de relance agricole en RDC. Malgré les défis logistiques persistants à l'Est du pays, la production affiche une dynamique intéressante sous l'impulsion des coopératives locales.</p>
    </div>
    """, unsafe_allowed_html=True)
    
    # Indicateurs 2025
    col_news1, col_news2, col_news3, col_news4 = st.columns(4)
    with col_news1:
        st.markdown("<div class='kpi-box'><div class='kpi-value'>11 450 t</div><div class='kpi-label'>Prod. Robusta 2025 (Est.)</div></div>", unsafe_allowed_html=True)
    with col_news2:
        st.markdown("<div class='kpi-box'><div class='kpi-value'>4 120 t</div><div class='kpi-label'>Prod. Arabica 2025 (Est.)</div></div>", unsafe_allowed_html=True)
    with col_news3:
        st.markdown("<div class='kpi-box'><div class='kpi-value'>2.85 $/kg</div><div class='kpi-label'>Prix Moyen Robusta 2025</div></div>", unsafe_allowed_html=True)
    with col_news4:
        st.markdown("<div class='kpi-box'><div class='kpi-value'>5.10 $/kg</div><div class='kpi-label'>Prix Moyen Arabica 2025</div></div>", unsafe_allowed_html=True)
        
    st.markdown("<br><hr>", unsafe_allowed_html=True)
    
    col_intro, col_img_side = st.columns([3, 2])
    with col_intro:
        st.markdown("### Objectifs de la Plateforme")
        st.write(
            """
            **Congo Coffee Data** est un outil d'appui à la recherche économique dédié à la filière café en RDC. 
            Il vise à réduire l’asymétrie d’information sur le marché en mettant à disposition des séries temporelles épurées.
            
            L'architecture de l'application s'articule autour de trois dimensions :
            - **L'offre sectorielle** via le suivi des volumes de production.
            - **La viabilité financière** à travers les structures de prix sur le marché mondial et local.
            - **La stabilité macroéconomique** par l'intégration des variables de cointégration.
            """
        )
        st.info("Cette plateforme sert d'outil d'aide à la décision pour les producteurs, acheteurs, institutions publiques et chercheurs.")

    with col_img_side:
        st.image(
            "https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=1961&auto=format&fit=crop",
            use_container_width=True
        )

# ----------------------------
# SECTION 2 : PRODUCTION ET PRIX
# ----------------------------
elif section == "Production et Prix":

    st.markdown("### Évolution de la Production et des Prix du Café")
    tab1, tab2 = st.tabs(["📊 Données Annuelles", "📈 Données Mensuelles"])

    with tab1:
        st.markdown("#### Analyse des tendances de long terme")
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

            df_graph_ann = df_ann_prod.copy()
            df_graph_ann[df_graph_ann.columns[0]] = pd.to_numeric(df_graph_ann[df_graph_ann.columns[0]], errors='coerce')
            df_graph_ann = df_graph_ann.dropna(subset=[df_graph_ann.columns[0]])
            
            x = df_graph_ann.columns[0]
            y = 'Total' if 'Total' in df_graph_ann.columns else df_graph_ann.columns[1]

            fig = px.line(df_graph_ann, x=x, y=y, title=f"Trajectoire temporelle de la production annuelle globale (en tonnes)")
            fig.update_traces(line_color='#8B5A2B', line_width=3)
            fig.update_layout(template="plotly_white", font_family="Plus Jakarta Sans")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du chargement des données annuelles : {e}")

    with tab2:
        st.markdown("#### Fluctuations mensuelles des marchés")
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
# SECTION 3 : DONNÉES MACROÉCONOMIQUES
# ----------------------------
elif section == "Données macroéconomiques":

    st.markdown("### Analyse Macroéconomique de la Filière Café")

    try:
        df_ardl = load_excel(URL_DATA_SITE, "Data for ARDL")

        st.markdown("#### Base de données macroéconomiques brute")
        st.dataframe(df_ardl, use_container_width=True)

        # --- NETTOYAGE SÉCURISÉ POUR L'ANALYSE ---
        df_clean = df_ardl.copy()
        col_temps = df_clean.columns[0]
        
        df_clean[col_temps] = pd.to_numeric(df_clean[col_temps], errors="coerce")
        df_clean = df_clean.dropna(subset=[col_temps])

        for col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        
        df_clean = df_clean.dropna()

        # --- AJOUT N°2 : ANALYSE DES PICS HISTORIQUES ---
        st.markdown("#### 🏔️ Analyse des Points de Retournement (Pics Historiques)")
        st.write("Ce module calcule de manière dynamique le niveau maximum historique atteint par chaque variable de votre modèle économétrique :")
        
        # Calcul automatique des maximums
        variables_macro = [c for c in df_clean.columns if c != col_temps]
        
        kpi_cols = st.columns(len(variables_macro) if len(variables_macro) <= 4 else 3)
        
        for i, var in enumerate(variables_macro):
            idx_max = df_clean[var].idxmax()
            val_max = df_clean[var].max()
            annee_max = int(df_clean.loc[idx_max, col_temps])
            
            # Formatage d'unité basique
            unite = "t" if "Production" in var else ("$/kg" if "Prix" in var else ("%" if "Inflation" in var else "CDF/USD"))
            
            with kpi_cols[i % len(kpi_cols)]:
                st.markdown(f"""
                <div class='kpi-box' style='border-top: 4px solid #4A2E2B; margin-bottom:15px;'>
                    <div class='kpi-label'>{var}</div>
                    <div class='kpi-value'>{val_max:,.2f} {unite}</div>
                    <div class='kpi-label' style='color:#8B5A2B;'>Année Pic : {annee_max}</div>
                </div>
                """, unsafe_allowed_html=True)

        st.markdown("<br>", unsafe_allowed_html=True)

        # --- GRAPHIQUE TEMPOREL ---
        st.markdown("#### Analyse graphique temporelle")
        variables = list(df_clean.columns)
        x_axis = variables[0]
        y_var = st.selectbox("Sélectionner la variable macroéconomique à tracer :", variables[1:])

        fig = px.line(df_clean, x=x_axis, y=y_var, title=f"Trajectoire de la variable : {y_var}")
        fig.update_traces(line_color='#4A2E2B', line_width=3)
        fig.update_layout(template="plotly_white", font_family="Plus Jakarta Sans")
        st.plotly_chart(fig, use_container_width=True)

        # --- MATRICE DE CORRÉLATION ---
        st.markdown("#### Matrice de corrélation de Pearson")
        colonnes_calcul = [c for c in df_clean.columns if c != col_temps]
        corr = df_clean[colonnes_calcul].corr()

        fig_corr = px.imshow(
            corr, 
            text_auto=".2f", 
            color_continuous_scale="Brwnyl",
            title="Coefficients de corrélation linéaire"
        )
        fig_corr.update_layout(font_family="Plus Jakarta Sans")
        st.plotly_chart(fig_corr, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur lors du traitement des données ARDL : {e}")
    

