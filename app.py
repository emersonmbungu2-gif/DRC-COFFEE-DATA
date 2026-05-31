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
st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Choisir une section :",
    [
        "Accueil",
        "Production et Prix",
        "Données macroéconomiques"
    ]
)

# ----------------------------
# TITRE PRINCIPAL ÉPURÉ
# ----------------------------
st.title("☕ Congo Coffee Data")
st.caption("Observatoire analytique et macroéconomique de la filière café en République Démocratique du Congo")
st.markdown("---")

# ----------------------------
# SECTION 1 : ACCUEIL & ACTUALITÉS
# ----------------------------
if section == "Accueil & Actualités":
    
    # Image principale de la plantation
    st.image(
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=2078&auto=format&fit=crop", 
        caption="Séchage traditionnel et contrôle qualité des cerises de café",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allowed_html=True)
    
    # --- ACTUALITÉS & CONJONCTURE 2025 ---
    st.subheader("📰 Actualités et Conjoncture Récente (Campagne 2025)")
    
    st.markdown(
        """
        La campagne caféière de l'année **2025** est marquée par une consolidation progressive des cours mondiaux 
        combinée à des efforts structurels de relance agricole en RDC. Malgré les défis logistiques persistants 
        à l'Est du pays, la production affiche une dynamique intéressante sous l'impulsion des coopératives locales.
        """
    )
    
    # Cartes d'indicateurs natifs Streamlit pour 2025 (Évite les bugs CSS)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Prod. Robusta 2025 (Est.)", value="11 450 t")
    with c2:
        st.metric(label="Prod. Arabica 2025 (Est.)", value="4 120 t")
    with c3:
        st.metric(label="Prix Moyen Robusta 2025", value="2.85 $/kg")
    with c4:
        st.metric(label="Prix Moyen Arabica 2025", value="5.10 $/kg")
        
    st.markdown("---")
    
    # Présentation générale
    col_intro, col_img_side = st.columns([3, 2])
    with col_intro:
        st.markdown("### Objectifs de la Plateforme")
        st.write(
            """
            **DRC Coffee Data** est un outil d'appui à la recherche économique dédié à la filière café en RDC. 
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

    st.subheader("Analyse de la production et des prix du café")
    tab1, tab2 = st.tabs(["📊 Données Annuelles", "📈 Données Mensuelles"])

    with tab1:
        st.markdown("### Analyse des tendances de long terme")
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

            fig = px.line(df_graph_ann, x=x, y=y, title=f"Trajectoire de la production annuelle globale (en tonnes)")
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du chargement des données annuelles : {e}")

    with tab2:
        st.markdown("### Fluctuations mensuelles des marchés")
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

    st.subheader("Analyse macroéconomique de la filière café")

    try:
        df_ardl = load_excel(URL_DATA_SITE, "Data for ARDL")

        st.write("### Base de données macroéconomiques brute")
        st.dataframe(df_ardl, use_container_width=True)

        # --- NETTOYAGE SÉCURISÉ POUR L'ANALYSE ---
        df_clean = df_ardl.copy()
        col_temps = df_clean.columns[0]
        
        df_clean[col_temps] = pd.to_numeric(df_clean[col_temps], errors="coerce")
        df_clean = df_clean.dropna(subset=[col_temps])

        for col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        
        df_clean = df_clean.dropna()

        # --- MODULE DES PICS HISTORIQUES ---
        st.markdown("### 🏔️ Analyse des Points de Retournement (Pics Historiques)")
        st.write("Calcul dynamique des niveaux maximums atteints par les variables clés de votre modèle :")
        
        variables_macro = [c for c in df_clean.columns if c != col_temps]
        
        # Affichage sous forme de colonnes
        kpi_cols = st.columns(len(variables_macro) if len(variables_macro) <= 4 else 3)
        
        for i, var in enumerate(variables_macro):
            idx_max = df_clean[var].idxmax()
            val_max = df_clean[var].max()
            annee_max = int(df_clean.loc[idx_max, col_temps])
            
            # Détermination automatique des unités
            unite = "t" if "Production" in var else ("$/kg" if "Prix" in var else ("%" if "Inflation" in var else "USD/CDF"))
            
            with kpi_cols[i % len(kpi_cols)]:
                st.metric(
                    label=f"Pic : {var}",
                    value=f"{val_max:,.2f} {unite}",
                    delta=f"Année : {annee_max}",
                    delta_color="off"
                )

        st.markdown("---")

        # --- GRAPHIQUE TEMPOREL ---
        st.markdown("### Analyse graphique temporelle")
        variables = list(df_clean.columns)
        x_axis = variables[0]
        y_var = st.selectbox("Sélectionner la variable macroéconomique à tracer :", variables[1:])

        fig = px.line(df_clean, x=x_axis, y=y_var, title=f"Trajectoire de la variable : {y_var}")
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # --- MATRICE DE CORRÉLATION ---
        st.markdown("### Matrice de corrélation de Pearson")
        colonnes_calcul = [c for c in df_clean.columns if c != col_temps]
        corr = df_clean[colonnes_calcul].corr()

        fig_corr = px.imshow(
            corr, 
            text_auto=".2f", 
            color_continuous_scale="RdBu_r",
            title="Coefficients de corrélation linéaire"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur lors du traitement des données ARDL : {e}")
        
