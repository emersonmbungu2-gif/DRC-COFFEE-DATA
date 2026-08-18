import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Congo Coffee Data",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# IDENTITÉ VISUELLE
# ============================================================

st.markdown("""
<style>

    /* ------------------------------
       GLOBAL
    ------------------------------ */

    .stApp {
        background-color: #ffffff;
        color: #1f2933;
    }

    .main .block-container {
        max-width: 1280px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /* ------------------------------
       TYPOGRAPHY
    ------------------------------ */

    h1 {
        color: #172b4d;
        font-weight: 650;
        letter-spacing: -0.025em;
    }

    h2 {
        color: #172b4d;
        font-weight: 600;
        margin-top: 2rem;
    }

    h3 {
        color: #334e68;
        font-weight: 600;
    }

    p, label {
        color: #52606d;
    }

    /* ------------------------------
       SIDEBAR
    ------------------------------ */

    section[data-testid="stSidebar"] {
        background-color: #f7f9fb;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #172b4d;
    }

    /* ------------------------------
       LINKS / BUTTONS
    ------------------------------ */

    .stButton > button {
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
        color: #172b4d;
        border-radius: 4px;
        font-weight: 500;
    }

    .stButton > button:hover {
        border-color: #486581;
        color: #102a43;
        background-color: #f8fafc;
    }

    /* ------------------------------
       METRICS
    ------------------------------ */

    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 4px;
        padding: 18px 20px;
        min-height: 120px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 650;
        color: #172b4d;
    }

    .metric-label {
        margin-top: 5px;
        color: #627d98;
        font-size: 0.85rem;
    }

    /* ------------------------------
       DATASET HEADER
    ------------------------------ */

    .dataset-header {
        border-left: 4px solid #486581;
        padding-left: 18px;
        margin: 15px 0 30px 0;
    }

    .dataset-title {
        font-size: 1.75rem;
        font-weight: 650;
        color: #172b4d;
    }

    .dataset-description {
        color: #627d98;
        font-size: 1rem;
        margin-top: 5px;
    }

    /* ------------------------------
       INFORMATION BOX
    ------------------------------ */

    .info-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 18px 20px;
        border-radius: 4px;
        margin: 15px 0;
    }

    /* ------------------------------
       FOOTER
    ------------------------------ */

    .footer {
        border-top: 1px solid #e5e7eb;
        margin-top: 60px;
        padding-top: 20px;
        color: #829ab1;
        font-size: 0.8rem;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CHEMINS DES FICHIERS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FILE_DATA = BASE_DIR / "Data for site.xlsx"
FILE_COFFEE = BASE_DIR / "Production et prix du café.xlsx"


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def clean_numeric_columns(df):
    """
    Convertit toutes les colonnes numériques lorsque possible.
    """
    result = df.copy()

    for col in result.columns:
        result[col] = pd.to_numeric(
            result[col],
            errors="ignore"
        )

    return result


def clean_annual_dataframe(df):
    """
    Nettoyage robuste des données annuelles.
    """
    df = df.copy()

    # Suppression des lignes entièrement vides
    df = df.dropna(how="all")

    # Renommage selon la structure réelle du fichier
    rename_map = {
        "Unnamed: 0": "Période",
        "(t)": "Production Robusta",
        "(t).1": "Production Arabica",
        "(t).2": "Production Totale",
        "($/kg)": "Prix Robusta",
        "($/kg).1": "Prix Arabica",
        "(USD/CDF)": "Taux de change",
        "(%)": "Inflation"
    }

    df = df.rename(columns=rename_map)

    # Retirer les lignes non statistiques
    if "Période" in df.columns:
        df["Période"] = pd.to_numeric(
            df["Période"],
            errors="coerce"
        )

        df = df[df["Période"].notna()]
        df["Période"] = df["Période"].astype(int)

    # Conversion numérique
    for col in df.columns:
        if col != "Période":
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Production totale
    if (
        "Production Totale" not in df.columns
        and "Production Robusta" in df.columns
        and "Production Arabica" in df.columns
    ):
        df["Production Totale"] = (
            df["Production Robusta"]
            + df["Production Arabica"]
        )

    return df.reset_index(drop=True)


def clean_monthly_dataframe(df):
    """
    Nettoyage des séries mensuelles.
    """
    df = df.copy()

    df = df.dropna(how="all")

    rename_map = {
        "Unnamed: 0": "Période",
        "(t)": "Production Robusta",
        "(t).1": "Production Arabica",
        "(t).2": "Production Totale",
        "($/kg)": "Prix Robusta",
        "($/kg).1": "Prix Arabica"
    }

    df = df.rename(columns=rename_map)

    if "Période" in df.columns:

        df["Période"] = (
            df["Période"]
            .astype(str)
            .str.strip()
        )

        # Exclure les lignes non statistiques
        df = df[
            ~df["Période"].str.contains(
                "Nombre total",
                case=False,
                na=False
            )
        ]

        # Vérifier les observations
        df = df[
            df["Période"].str.match(
                r"^\d{4}\s*-\s*"
            )
        ]

    for col in df.columns:

        if col != "Période":
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df.reset_index(drop=True)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

@st.cache_data
def load_data():

    # ------------------------------
    # Data for site.xlsx
    # ------------------------------

    df_ardl_raw = pd.read_excel(
        FILE_DATA,
        sheet_name="Data for ARDL",
        header=0
    )

    df_annual_ardl = clean_annual_dataframe(
        df_ardl_raw
    )

    # ------------------------------
    # Production et prix du café
    # ------------------------------

    df_annual_prod_raw = pd.read_excel(
        FILE_COFFEE,
        sheet_name="Annual Production",
        header=0
    )

    df_annual_price_raw = pd.read_excel(
        FILE_COFFEE,
        sheet_name="Annual Price",
        header=0
    )

    df_month_prod_raw = pd.read_excel(
        FILE_COFFEE,
        sheet_name="Monthly Production",
        header=0
    )

    df_month_price_raw = pd.read_excel(
        FILE_COFFEE,
        sheet_name="Monthly Price",
        header=0
    )

    df_annual_prod = clean_annual_dataframe(
        df_annual_prod_raw
    )

    df_annual_price = clean_annual_dataframe(
        df_annual_price_raw
    )

    df_month_prod = clean_monthly_dataframe(
        df_month_prod_raw
    )

    df_month_price = clean_monthly_dataframe(
        df_month_price_raw
    )

    # ------------------------------
    # Fusion annuelle
    # ------------------------------

    df_annual = df_annual_prod.merge(
        df_annual_price,
        on="Période",
        how="outer",
        suffixes=("", "_price")
    )

    # Ajouter les variables macroéconomiques
    macro_cols = [
        "Période",
        "Taux de change",
        "Inflation"
    ]

    available_macro = [
        col for col in macro_cols
        if col in df_annual_ardl.columns
    ]

    if len(available_macro) > 1:

        df_annual = df_annual.merge(
            df_annual_ardl[available_macro],
            on="Période",
            how="left"
        )

    # Trier
    df_annual = df_annual.sort_values(
        "Période"
    ).reset_index(drop=True)

    return (
        df_annual,
        df_month_prod,
        df_month_price,
        df_annual_ardl
    )


# ============================================================
# CHARGEMENT SÉCURISÉ
# ============================================================

try:

    if not FILE_DATA.exists():
        st.error(
            "Le fichier 'Data for site.xlsx' est introuvable."
        )
        st.stop()

    if not FILE_COFFEE.exists():
        st.error(
            "Le fichier 'Production et prix du café.xlsx' "
            "est introuvable."
        )
        st.stop()

    (
        df_annual,
        df_month_prod,
        df_month_price,
        df_ardl
    ) = load_data()

except Exception as e:

    st.error(
        "Impossible de charger les données."
    )

    st.exception(e)
    st.stop()


# ============================================================
# MÉTADONNÉES
# ============================================================

INDICATORS = {

    "Production Robusta": {
        "column": "Production Robusta",
        "unit": "tonnes",
        "frequency": "Annuelle",
        "description":
            "Production annuelle de café Robusta "
            "en République démocratique du Congo."
    },

    "Production Arabica": {
        "column": "Production Arabica",
        "unit": "tonnes",
        "frequency": "Annuelle",
        "description":
            "Production annuelle de café Arabica "
            "en République démocratique du Congo."
    },

    "Production Totale": {
        "column": "Production Totale",
        "unit": "tonnes",
        "frequency": "Annuelle",
        "description":
            "Production annuelle totale correspondant "
            "à la somme du Robusta et de l'Arabica."
    },

    "Prix Robusta": {
        "column": "Prix Robusta",
        "unit": "USD/kg",
        "frequency": "Annuelle",
        "description":
            "Prix du café Robusta exprimé en dollars "
            "américains par kilogramme."
    },

    "Prix Arabica": {
        "column": "Prix Arabica",
        "unit": "USD/kg",
        "frequency": "Annuelle",
        "description":
            "Prix du café Arabica exprimé en dollars "
            "américains par kilogramme."
    },

    "Taux de change": {
        "column": "Taux de change",
        "unit": "CDF/USD",
        "frequency": "Annuelle",
        "description":
            "Taux de change nominal annuel du franc congolais "
            "par rapport au dollar américain."
    },

    "Inflation": {
        "column": "Inflation",
        "unit": "%",
        "frequency": "Annuelle",
        "description":
            "Taux d'inflation annuel."
    }
}


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    # CONGO COFFEE DATA

    **Statistical Data Portal**

    République démocratique du Congo
    """
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Accueil",
        "Indicateurs",
        "Explorer les données",
        "Comparer",
        "Téléchargements",
        "Méthodologie"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Portail indépendant de diffusion "
    "de données statistiques sur la filière café."
)


# ============================================================
# ACCUEIL
# ============================================================

if page == "Accueil":

    st.markdown(
        """
        <div class="dataset-header">
            <div class="dataset-title">
                Congo Coffee Data
            </div>
            <div class="dataset-description">
                Données statistiques sur la production,
                les prix du café et certains indicateurs
                macroéconomiques de la République démocratique du Congo.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    min_year = int(df_annual["Période"].min())
    max_year = int(df_annual["Période"].max())

    annual_obs = len(df_annual)
    monthly_prod_obs = len(df_month_prod)
    monthly_price_obs = len(df_month_price)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">
                    {min_year}–{max_year}
                </div>
                <div class="metric-label">
                    Période couverte
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">
                    {annual_obs:,}
                </div>
                <div class="metric-label">
                    Observations annuelles
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">
                    {monthly_prod_obs:,}
                </div>
                <div class="metric-label">
                    Observations mensuelles de production
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">
                    {monthly_price_obs:,}
                </div>
                <div class="metric-label">
                    Observations mensuelles de prix
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.header("À propos des données")

    st.write(
        """
        Congo Coffee Data est un portail de diffusion de données
        consacré à la filière café en République démocratique du Congo.

        Le portail rassemble des séries annuelles et mensuelles portant
        notamment sur la production de Robusta et d'Arabica, les prix,
        le taux de change et l'inflation.

        Les données peuvent être explorées en ligne ou téléchargées
        pour une utilisation dans des travaux universitaires,
        statistiques et économétriques.
        """
    )

    st.header("Principales séries")

    overview = pd.DataFrame([
        {
            "Indicateur": name,
            "Unité": meta["unit"],
            "Fréquence": meta["frequency"]
        }
        for name, meta in INDICATORS.items()
    ])

    st.dataframe(
        overview,
        hide_index=True,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="footer">
            Congo Coffee Data · République démocratique du Congo
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# INDICATEURS
# ============================================================

elif page == "Indicateurs":

    st.title("Indicateurs")

    st.write(
        "Catalogue des séries statistiques disponibles."
    )

    selected = st.selectbox(
        "Sélectionner un indicateur",
        list(INDICATORS.keys())
    )

    meta = INDICATORS[selected]
    column = meta["column"]

    st.markdown("---")

    st.header(selected)

    st.write(meta["description"])

    c1, c2, c3 = st.columns(3)

    series = df_annual[["Période", column]].dropna()

    with c1:
        st.metric(
            "Unité",
            meta["unit"]
        )

    with c2:
        st.metric(
            "Fréquence",
            meta["frequency"]
        )

    with c3:
        st.metric(
            "Observations",
            len(series)
        )

    # ---------------------------------------
    # Graphique
    # ---------------------------------------

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=series["Période"],
            y=series[column],
            mode="lines",
            name=selected,
            line=dict(
                color="#243b53",
                width=2.5
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                + selected
                + ": %{y:,.3f}"
                + "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        height=500,
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),
        xaxis_title="Année",
        yaxis_title=meta["unit"],
        hovermode="x unified"
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#e5e7eb"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e5e7eb"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------------------
    # Données
    # ---------------------------------------

    st.header("Données")

    display_df = series.rename(
        columns={
            "Période": "Année",
            column: selected
        }
    )

    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True
    )

    # ---------------------------------------
    # Téléchargement
    # ---------------------------------------

    csv = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Télécharger la série CSV",
        data=csv,
        file_name=(
            selected.lower()
            .replace(" ", "_")
            .replace("/", "_")
            + ".csv"
        ),
        mime="text/csv"
    )


# ============================================================
# EXPLORER LES DONNÉES
# ============================================================

elif page == "Explorer les données":

    st.title("Explorer les données")

    st.write(
        """
        Explorez directement les observations disponibles,
        sélectionnez la fréquence et filtrez la période.
        """
    )

    frequency = st.radio(
        "Fréquence",
        [
            "Annuelle",
            "Mensuelle – Production",
            "Mensuelle – Prix"
        ],
        horizontal=True
    )

    if frequency == "Annuelle":

        df = df_annual.copy()

        min_year = int(df["Période"].min())
        max_year = int(df["Période"].max())

        years = st.slider(
            "Période",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )

        df = df[
            df["Période"].between(
                years[0],
                years[1]
            )
        ]

    elif frequency == "Mensuelle – Production":

        df = df_month_prod.copy()

        df["Année"] = pd.to_numeric(
            df["Période"]
            .str.extract(r"(\d{4})")[0],
            errors="coerce"
        )

        df = df.dropna(
            subset=["Année"]
        )

        df["Année"] = df["Année"].astype(int)

 
