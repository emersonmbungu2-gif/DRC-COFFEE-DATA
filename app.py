import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuration de la page (Inspiration Banque Mondiale / Our World in Data)
st.set_page_config(
    page_title="Congo Coffee Data | Base de Données du Café Congolais",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pour appliquer la charte graphique demandée (épuré, blanc, vert foncé, gris)
st.markdown("""
<style>
    :root {
        --primary-color: #1b4332;
        --secondary-color: #40916c;
        --bg-light: #f8f9fa;
    }
    .main .block-container { padding-top: 2rem; }
    h1 { color: #1b4332; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 700; }
    h2, h3 { color: #2d6a4f; font-family: 'Helvetica Neue', Arial, sans-serif; }
    .stButton>button { background-color: #1b4332; color: white; border-radius: 4px; }
    .stButton>button:hover { background-color: #40916c; color: white; }
    .metric-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 6px;
        border-left: 5px solid #1b4332;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-val { font-size: 2rem; font-weight: bold; color: #1b4332; }
    .metric-lbl { font-size: 0.9rem; color: #6c757d; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# --- CHARGEMENT ET NETTOYAGE DES DONNÉES ---
@st.cache_data
def load_data():
    # 1. Chargement données annuelles globales (ARDL)
    df_ardl = pd.read_excel("Data for site.xlsx", sheet_name="Data for ARDL")
    df_ardl_clean = df_ardl.dropna(subset=["Période"]).iloc[1:].copy()
    df_ardl_clean["Période"] = pd.to_numeric(df_ardl_clean["Période"]).astype(int)
    for col in df_ardl_clean.columns:
        if col != "Période":
            df_ardl_clean[col] = pd.to_numeric(df_ardl_clean[col], errors='coerce')
    
    # Ajout automatique de la production totale manquante dans ARDL pour conformité
    if "Production Totale" not in df_ardl_clean.columns:
        df_ardl_clean["Production Totale"] = df_ardl_clean["Production Robusta"] + df_ardl_clean["Production Arabica"]
        
    # 2. Chargement des séries mensuelles pour granularité fine
    df_m_prod = pd.read_excel("Production et prix du café.xlsx", sheet_name="Monthly Production").iloc[1:].dropna(subset=["Période"])
    df_m_price = pd.read_excel("Production et prix du café.xlsx", sheet_name="Monthly Price").iloc[1:].dropna(subset=["Période"])
    
    return df_ardl_clean, df_m_prod, df_m_price

try:
    df_annual, df_m_prod, df_m_price = load_data()
except Exception as e:
    st.error(f"Erreur de lecture des fichiers Excel sources ('Data for site.xlsx' et 'Production et prix du café.xlsx') : {e}")
    st.stop()

# Dictionnaire de métadonnées des indicateurs (Définitions académiques et sources)
indicators = {
    "Production Robusta": {
        "def": "Volume total annuel de café Robusta (Coffea canephora) produit et enregistré en République Démocratique du Congo, exprimé en tonnes métriques (t).",
        "col": "Production Robusta", "unit": "tonnes (t)", "source": "Ministère de l'Agriculture / ONAPAC / Guichet Unique"
    },
    "Production Arabica": {
        "def": "Volume total annuel de café Arabica (Coffea arabica) produit sur les hauts plateaux (notamment Kivu, Ituri), exprimé en tonnes métriques (t).",
        "col": "Production Arabica", "unit": "tonnes (t)", "source": "Ministère de l'Agriculture / ONAPAC"
    },
    "Production Totale": {
        "def": "Somme agrégée des productions nationales de café Robusta et Arabica en tonnes métriques (t).",
        "col": "Production Totale", "unit": "tonnes (t)", "source": "Calculs statistiques internes basés sur les données sectorielles"
    },
    "Prix Robusta": {
        "def": "Prix moyen pondéré perçu par les producteurs ou enregistré à l'exportation pour le café Robusta, exprimé en dollars américains par kilogramme ($/kg).",
        "col": "Prix Robusta", "unit": "$/kg", "source": "International Coffee Organization (ICO) / Notes de conjoncture BCC"
    },
    "Prix Arabica": {
        "def": "Prix moyen du marché ou à l'exportation pour le café Arabica de la RDC, exprimé en dollars américains par kilogramme ($/kg).",
        "col": "Prix Arabica", "unit": "$/kg", "source": "International Coffee Organization (ICO)"
    },
    "Inflation": {
        "def": "Taux d'inflation annuel moyen calculé sur l'indice des prix à la consommation (IPC) en République Démocratique du Congo, exprimé en pourcentage (%).",
        "col": "Inflation", "unit": "%", "source": "Banque Centrale du Congo (BCC) / FMI"
    },
    "Taux de change": {
        "def": "Valeur externe de la monnaie nationale exprimée en taux de change nominal moyen annuel (Franc Congolais pour un Dollar Américain - USD/CDF).",
        "col": "Taux de change", "unit": "USD/CDF", "source": "Banque Centrale du Congo (BCC)"
    }
}

# --- BARRE LATÉRALE DE NAVIGATION ---
st.sidebar.image("https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=150", width=100, caption="Filière Café RDC")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Page d'accueil", "Catalogue des indicateurs", "Comparaison d'indicateurs", "Recherche avancée"])

st.sidebar.markdown("---")
st.sidebar.info("**Note académique :** Ce portail fournit un accès libre aux indicateurs structurels de l'économie caféière en RDC pour appuyer la recherche et les politiques publiques économiques.")

# ==================== PAGE D'ACCUEIL ====================
if page == "Page d'accueil":
    st.title("☕ Congo Coffee Data")
    st.subheader("Base de Données du Café Congolais")
    
    st.markdown("""
    > **Plateforme ouverte de données statistiques sur la filière café en République Démocratique du Congo.**
    
    Inspirée des standards de diffusion de la *Banque Mondiale*, de l'*ICO* et de *Our World in Data*, cette interface centralise les données historiques de production, de prix et les variables macroéconomiques structurantes pour la filière en RDC.
    """)
    
    st.markdown("### 📊 Statistiques rapides de la base")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>32 ans</div><div class='metric-lbl'>Années couvertes<br>(1994 - 2025)</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{len(indicators)}</div><div class='metric-lbl'>Indicateurs macro & sectoriels</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>2 114</div><div class='metric-lbl'>Points d'observations</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>Mai 2026</div><div class='metric-lbl'>Dernière mise à jour</div></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 📌 Aperçu thématique")
    st.write("Sélectionnez un onglet dans le menu latéral pour explorer les données de production nationale, suivre l'évolution des prix de vente spot en $/kg ou croiser les dynamiques de marché face au taux de change du Franc Congolais (CDF).")


# ==================== CATALOGUE DES INDICATEURS ====================
elif page == "Catalogue des indicateurs":
    st.title("📂 Catalogue des indicateurs")
    st.write("Cliquez sur l'indicateur de votre choix pour voir sa série temporelle complète, sa définition, son graphique dynamique et exporter ses données.")
    
    # Génération d'une structure de grille (Cartes)
    cols = st.columns(3)
    idx = 0
    for key, info in indicators.items():
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="background-color:#ffffff; padding:15px; border-radius:6px; border:1px solid #e0e0e0; margin-bottom:15px;">
                <h4 style="margin:0; color:#1b4332;">{key}</h4>
                <p style="font-size:0.85rem; color:#6c757d; height:45px; overflow:hidden; text-overflow:ellipsis;">{info['def']}</p>
                <p style="font-weight:bold; font-size:0.8rem; color:#40916c; margin-bottom:5px;">Unité : {info['unit']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Consulter l'indicateur : {key}", key=f"btn_{key}"):
                st.session_state['selected_indicator'] = key
                st.session_state['trigger_view'] = True
        idx += 1

    # Section dynamique d'affichage suite au clic
    target = st.session_state.get('selected_indicator', "Production Robusta")
    
    st.markdown("---")
    st.header(f"📈 Analyse détaillée : {target}")
    
    info_target = indicators[target]
    st.markdown(f"**Définition technique :** {info_target['def']}")
    st.markdown(f"**Source institutionnelle :** `{info_target['source']}`")
    
    # Création du graphique temporel Plotly épuré
    fig = px.line(
        df_annual, x="Période", y=info_target['col'],
        title=f"Évolution temporelle : {target} (1994 - 2025)",
        labels={"Période": "Année", info_target['col']: f"{target} ({info_target['unit']})"},
        markers=True
    )
    fig.update_traces(line_color='#1b4332', marker=dict(size=6))
    fig.update_layout(plot_bgcolor='white', hovermode='x unified')
    fig.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig, use_container_width=True)
    
    # Table de données & Téléchargements
    st.subheader("📋 Données brutes de la série")
    sub_df = df_annual[["Période", info_target['col']]].rename(columns={"Période": "Année"}).dropna()
    
    col_data, col_dl = st.columns([2, 1])
    with col_data:
        st.dataframe(sub_df.style.format({"Année": "{:.0f}", info_target['col']: "{:,.2f}"}), height=250, use_container_width=True)
        
    with col_dl:
        st.write("📥 Exporter cette série :")
        # Téléchargement CSV
        csv_data = sub_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Télécharger au format CSV", data=csv_data, file_name=f"{target.lower().replace(' ', '_')}_rdc.csv", mime='text/csv')
        
        # Téléchargement Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            sub_df.to_excel(writer, index=False, sheet_name='Données')
        excel_data = output.getvalue()
        st.download_button(label="Télécharger au format Excel (XLSX)", data=excel_data, file_name=f"{target.lower().replace(' ', '_')}_rdc.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# ==================== COMPARAISON D'INDICATEURS ====================
elif page == "Comparaison d'indicateurs":
    st.title("🔀 Analyse comparative croisée")
    st.write("Sélectionnez jusqu'à deux variables pour analyser les corrélations historiques ou l'impact des chocs macroéconomiques sur les prix et volumes de café.")
    
    col_sel1, col_sel2 = st.columns(2)
    options_list = list(indicators.keys())
    
    with col_sel1:
        var1 = st.selectbox("Première variable (Axe Y Gauche)", options_list, index=0)
    with col_sel2:
        var2 = st.selectbox("Deuxième variable (Axe Y Droit)", options_list, index=3)
        
    if var1 and var2:
        fig_comp = go.Figure()
        
        # Ajout variable 1
        fig_comp.add_trace(go.Scatter(
            x=df_annual["Période"], y=df_annual[indicators[var1]['col']],
            name=f"{var1} ({indicators[var1]['unit']})",
            line=dict(color='#1b4332', width=2.5), mode='lines+markers'
        ))
        
        # Ajout variable 2 avec axe secondaire
        fig_comp.add_trace(go.Scatter(
            x=df_annual["Période"], y=df_annual[indicators[var2]['col']],
            name=f"{var2} ({indicators[var2]['unit']})",
            line=dict(color='#d90429', width=2.5, dash='dash'), yaxis="y2", mode='lines+markers'
        ))
        
        # Mise en page double axe
        fig_comp.update_layout(
            title=f"Comparatif : {var1} vs {var2}",
            xaxis=dict(title="Année"),
            yaxis=dict(title=f"{var1} ({indicators[var1]['unit']})", titlefont=dict(color="#1b4332"), tickfont=dict(color="#1b4332")),
            yaxis2=dict(title=f"{var2} ({indicators[var2]['unit']})", titlefont=dict(color="#d90429"), tickfont=dict(color="#d90429"), overlaying="y", side="right"),
            plot_bgcolor='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        fig_comp.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
        st.plotly_chart(fig_comp, use_container_width=True)
        
        st.info(f"💡 **Observation analytique :** Ce graphique permet de visualiser de manière synchrone les cycles des prix internationaux et leurs répercussions immédiates sur le niveau de production physique sur le territoire national.")


# ==================== RECHERCHE AVANCÉE ====================
elif page == "Recherche avancée":
    st.title("🔍 Moteur de recherche d'indicateurs")
    query = st.text_input("Saisissez des mots-clés (ex: Robusta, Inflation, Taux, Prix...)", "")
    
    if query:
        results = {k: v for k, v in indicators.items() if query.lower() in k.lower() or query.lower() in v['def'].lower()}
        if results:
            st.success(f"🎯 {len(results)} indicateur(s) correspondant(s) trouvé(s) :")
            for k, v in results.items():
                with st.expander(f"📊 {k} ({v['unit']})"):
                    st.write(f"**Définition :** {v['def']}")
                    st.write(f"**Source officielle :** {v['source']}")
        else:
            st.warning("Aucun indicateur ne correspond à votre recherche. Essayez des termes génériques comme 'Production' ou 'Prix'.")
