import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# CONFIGURATION GÉNÉRALE
# ============================================================

st.set_page_config(
    page_title="DRC Coffee Data",
    page_icon="☕",
    layout="wide"
)


# ============================================================
# SOURCES DE DONNÉES
# ============================================================

URL_PRODUCTION_PRIX = (
    "https://raw.githubusercontent.com/emersonmbungu2-gif/"
    "DRC-COFFEE-DATA/main/"
    "Production%20et%20prix%20du%20caf%C3%A9.xlsx"
)

URL_DATA_SITE = (
    "https://raw.githubusercontent.com/emersonmbungu2-gif/"
    "DRC-COFFEE-DATA/main/"
    "Data%20for%20site.xlsx"
)


# ============================================================
# FONCTIONS DE CHARGEMENT
# ============================================================

@st.cache_data
def load_excel(url, sheet):
    """
    Charge une feuille Excel depuis une URL.
    """
    try:
        return pd.read_excel(url, sheet_name=sheet)
    except Exception as e:
        raise RuntimeError(
            f"Impossible de charger la feuille '{sheet}'. "
            f"Erreur : {e}"
        )


def clean_numeric_df(df, time_col_name=None):
    """
    Nettoie un DataFrame destiné à une analyse numérique.

    - Supprime les lignes sans année/période valide.
    - Convertit les colonnes numériques.
    - Supprime les colonnes entièrement vides après conversion.
    - Trie les observations selon la variable temporelle.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    df_clean = df.copy()

    # Supprimer les colonnes complètement vides
    df_clean = df_clean.dropna(axis=1, how="all")

    if df_clean.empty:
        return pd.DataFrame()

    # Identifier la colonne temporelle
    if time_col_name and time_col_name in df_clean.columns:
        time_col = time_col_name
    else:
        time_col = df_clean.columns[0]

    # Conversion de la variable temporelle
    df_clean[time_col] = pd.to_numeric(
        df_clean[time_col],
        errors="coerce"
    )

    # Supprimer les lignes sans période valide
    df_clean = df_clean.dropna(subset=[time_col])

    if df_clean.empty:
        return pd.DataFrame()

    # Conversion des autres colonnes
    for col in df_clean.columns:
        if col != time_col:
            df_clean[col] = pd.to_numeric(
                df_clean[col],
                errors="coerce"
            )

    # Supprimer les colonnes qui ne contiennent aucune valeur numérique
    numeric_cols = [time_col]

    for col in df_clean.columns:
        if col != time_col and df_clean[col].notna().any():
            numeric_cols.append(col)

    df_clean = df_clean[numeric_cols]

    # Trier par année/période
    df_clean = df_clean.sort_values(
        by=time_col
    ).reset_index(drop=True)

    return df_clean


def get_row_by_year(df, time_col, year):
    """
    Retourne l'observation correspondant à une année donnée.
    """
    if df.empty or time_col not in df.columns:
        return None

    result = df[df[time_col] == year]

    if result.empty:
        return None

    return result.iloc[0]


def calculate_variation(current, previous):
    """
    Calcule une variation en pourcentage.
    Retourne None si le calcul est impossible.
    """
    if pd.isna(current) or pd.isna(previous):
        return None

    if previous == 0:
        return None

    return f"{((current - previous) / previous) * 100:+.1f}% vs 2024"


def safe_float(value):
    """
    Convertit une valeur en float sans provoquer d'erreur.
    """
    try:
        if pd.isna(value):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


# ============================================================
# TITRE
# ============================================================

st.title("☕ DRC Coffee Data")
st.markdown("---")


# ============================================================
# NAVIGATION
# ============================================================

st.sidebar.header("Navigation")

section = st.sidebar.radio(
    "Choisir une section",
    [
        "Accueil",
        "Production et Prix",
        "Données macroéconomiques"
    ]
)


# ============================================================
# SECTION 1 : ACCUEIL
# ============================================================

if section == "Accueil":

    st.subheader("Welcome!")

    st.write(
        """
        DRC Coffee Data est une plateforme de données économiques
        dédiée à la filière café en République démocratique du Congo.

        Elle vise à réduire l'asymétrie d'information en mettant
        à disposition des données sur :

        - la production ;
        - les prix ;
        - les variables macroéconomiques liées au secteur.

        La plateforme s'adresse aux producteurs, acheteurs,
        investisseurs, institutions publiques et chercheurs.
        """
    )

    st.info(
        "Cette plateforme est conçue comme un outil d'aide à la "
        "décision et de transparence du marché."
    )

    # --------------------------------------------------------
    # ACTUALITÉS
    # --------------------------------------------------------

    st.markdown("---")
    st.subheader("Actualités")

    st.caption(
        "Voici les chiffres clés de la filière café en RDC "
        "pour l'année 2025."
    )

    try:

        # Chargement des données
        raw_prod = load_excel(
            URL_PRODUCTION_PRIX,
            "Annual Production"
        )

        raw_price = load_excel(
            URL_PRODUCTION_PRIX,
            "Annual Price"
        )

        # Nettoyage
        df_prod_ann = clean_numeric_df(raw_prod)
        df_price_ann = clean_numeric_df(raw_price)

        # Vérification des données
        if df_prod_ann.empty:
            st.warning(
                "Les données de production annuelle sont indisponibles."
            )

        if df_price_ann.empty:
            st.warning(
                "Les données de prix annuels sont indisponibles."
            )

        # ====================================================
        # PRODUCTION
        # ====================================================

        st.markdown("#### Production 2025 (en tonnes)")

        c1, c2, c3 = st.columns(3)

        if not df_prod_ann.empty:

            time_col = df_prod_ann.columns[0]

            row_2025 = get_row_by_year(
                df_prod_ann,
                time_col,
                2025
            )

            row_2024 = get_row_by_year(
                df_prod_ann,
                time_col,
                2024
            )

            required_columns = [
                "Total",
                "Robusta",
                "Arabica"
            ]

            missing_columns = [
                col
                for col in required_columns
                if col not in df_prod_ann.columns
            ]

            if missing_columns:

                st.warning(
                    "Colonnes de production manquantes : "
                    + ", ".join(missing_columns)
                )

            elif row_2025 is None:

                st.warning(
                    "Aucune donnée de production disponible pour 2025."
                )

            else:

                total_2025 = safe_float(row_2025["Total"])
                robusta_2025 = safe_float(row_2025["Robusta"])
                arabica_2025 = safe_float(row_2025["Arabica"])

                delta_total = None
                delta_rob = None
                delta_ara = None

                if row_2024 is not None:

                    total_2024 = safe_float(row_2024["Total"])
                    robusta_2024 = safe_float(row_2024["Robusta"])
                    arabica_2024 = safe_float(row_2024["Arabica"])

                    if total_2025 is not None:
                        delta_total = calculate_variation(
                            total_2025,
                            total_2024
                        )

                    if robusta_2025 is not None:
                        delta_rob = calculate_variation(
                            robusta_2025,
                            robusta_2024
                        )

                    if arabica_2025 is not None:
                        delta_ara = calculate_variation(
                            arabica_2025,
                            arabica_2024
                        )

                # Production totale
                if total_2025 is not None:
                    c1.metric(
                        "Production totale",
                        f"{total_2025:,.0f} t",
                        delta_total
                    )
                else:
                    c1.metric(
                        "Production totale",
                        "N/D"
                    )

                # Robusta
                if robusta_2025 is not None:
                    c2.metric(
                        "Robusta",
                        f"{robusta_2025:,.0f} t",
                        delta_rob
                    )
                else:
                    c2.metric(
                        "Robusta",
                        "N/D"
                    )

                # Arabica
                if arabica_2025 is not None:
                    c3.metric(
                        "Arabica",
                        f"{arabica_2025:,.0f} t",
                        delta_ara
                    )
                else:
                    c3.metric(
                        "Arabica",
                        "N/D"
                    )

        # ====================================================
        # PRIX
        # ====================================================

        st.markdown("#### Prix 2025 ($/kg)")

        c1, c2 = st.columns(2)

        if not df_price_ann.empty:

            time_col = df_price_ann.columns[0]

            row_2025 = get_row_by_year(
                df_price_ann,
                time_col,
                2025
            )

            row_2024 = get_row_by_year(
                df_price_ann,
                time_col,
                2024
            )

            required_columns = [
                "Robusta",
                "Arabica"
            ]

            missing_columns = [
                col
                for col in required_columns
                if col not in df_price_ann.columns
            ]

            if missing_columns:

                st.warning(
                    "Colonnes de prix manquantes : "
                    + ", ".join(missing_columns)
                )

            elif row_2025 is None:

                st.warning(
                    "Aucune donnée de prix disponible pour 2025."
                )

            else:

                robusta_price_2025 = safe_float(
                    row_2025["Robusta"]
                )

                arabica_price_2025 = safe_float(
                    row_2025["Arabica"]
                )

                delta_rob_price = None
                delta_ara_price = None

                if row_2024 is not None:

                    robusta_price_2024 = safe_float(
                        row_2024["Robusta"]
                    )

                    arabica_price_2024 = safe_float(
                        row_2024["Arabica"]
                    )

                    if robusta_price_2025 is not None:
                        delta_rob_price = calculate_variation(
                            robusta_price_2025,
                            robusta_price_2024
                        )

                    if arabica_price_2025 is not None:
                        delta_ara_price = calculate_variation(
                            arabica_price_2025,
                            arabica_price_2024
                        )

                if robusta_price_2025 is not None:
                    c1.metric(
                        "Prix Robusta",
                        f"{robusta_price_2025:.2f} $/kg",
                        delta_rob_price
                    )
                else:
                    c1.metric(
                        "Prix Robusta",
                        "N/D"
                    )

                if arabica_price_2025 is not None:
                    c2.metric(
                        "Prix Arabica",
                        f"{arabica_price_2025:.2f} $/kg",
                        delta_ara_price
                    )
                else:
                    c2.metric(
                        "Prix Arabica",
                        "N/D"
                    )

        st.caption(
            "Sources : Banque Centrale du Congo et Banque mondiale."
        )

        st.caption(
            "Développé par Emerson Mbungu."
        )

    except Exception as e:

        st.error(
            "Erreur lors du chargement des données 2025."
        )

        st.exception(e)


# ============================================================
# SECTION 2 : PRODUCTION ET PRIX
# ============================================================

elif section == "Production et Prix":

    st.subheader("Production et Prix")

    tab1, tab2 = st.tabs(
        [
            "Données annuelles",
            "Données mensuelles"
        ]
    )

    # ========================================================
    # DONNÉES ANNUELLES
    # ========================================================

    with tab1:

        st.markdown(
            "### Analyse des tendances annuelles"
        )

        try:

            df_ann_prod = load_excel(
                URL_PRODUCTION_PRIX,
                "Annual Production"
            )

            df_ann_price = load_excel(
                URL_PRODUCTION_PRIX,
                "Annual Price"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Production annuelle (en tonnes)**"
                )

                st.dataframe(
                    df_ann_prod,
                    use_container_width=True,
                    hide_index=True
                )

            with col2:

                st.write(
                    "**Prix annuels ($/kg)**"
                )

                st.dataframe(
                    df_ann_price,
                    use_container_width=True,
                    hide_index=True
                )

            # ------------------------------------------------
            # PRÉPARATION DU GRAPHIQUE
            # ------------------------------------------------

            df_graph_ann = clean_numeric_df(
                df_ann_prod
            )

            if df_graph_ann.empty:

                st.warning(
                    "Impossible de générer le graphique annuel."
                )

            else:

                x = df_graph_ann.columns[0]

                if "Total" in df_graph_ann.columns:

                    y = "Total"

                elif len(df_graph_ann.columns) > 1:

                    y = df_graph_ann.columns[1]

                else:

                    st.warning(
                        "Aucune variable de production disponible."
                    )
                    y = None

                if y is not None:

                    df_graph_ann = df_graph_ann[
                        [x, y]
                    ].dropna()

                    if not df_graph_ann.empty:

                        fig = px.line(
                            df_graph_ann,
                            x=x,
                            y=y,
                            markers=True,
                            title=(
                                "Évolution de la production "
                                "annuelle globale"
                            ),
                            labels={
                                x: "Année",
                                y: "Production (tonnes)"
                            }
                        )

                        fig.update_layout(
                            template="plotly_white",
                            hovermode="x unified"
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    else:

                        st.warning(
                            "Aucune donnée exploitable pour le graphique."
                        )

        except Exception as e:

            st.error(
                "Erreur lors du chargement des données annuelles."
            )

            st.exception(e)

    # ========================================================
    # DONNÉES MENSUELLES
    # ========================================================

    with tab2:

        st.markdown(
            "### Analyse des tendances mensuelles"
        )

        try:

            df_mth_prod = load_excel(
                URL_PRODUCTION_PRIX,
                "Monthly Production"
            )

            df_mth_price = load_excel(
                URL_PRODUCTION_PRIX,
                "Monthly Price"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Production mensuelle (en tonnes)**"
                )

                st.dataframe(
                    df_mth_prod,
                    use_container_width=True,
                    hide_index=True
                )

            with col2:

                st.write(
                    "**Prix mensuels ($/kg)**"
                )

                st.dataframe(
                    df_mth_price,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:

            st.error(
                "Erreur lors du chargement des données mensuelles."
            )

            st.exception(e)


# ============================================================
# SECTION 3 : DONNÉES MACROÉCONOMIQUES
# ============================================================

elif section == "Données macroéconomiques":

    st.subheader(
        "Données, statistiques et graphiques"
    )

    try:

        # ----------------------------------------------------
        # CHARGEMENT
        # ----------------------------------------------------

        df_ardl = load_excel(
            URL_DATA_SITE,
            "Data for ARDL"
        )

        if df_ardl.empty:

            st.warning(
                "La base de données ARDL est vide."
            )

            st.stop()

        # ----------------------------------------------------
        # BASE DE DONNÉES BRUTE
        # ----------------------------------------------------

        st.write("### Base de données")

        st.dataframe(
            df_ardl,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # NETTOYAGE
        # ----------------------------------------------------

        df_clean = clean_numeric_df(
            df_ardl
        )

        if df_clean.empty:

            st.warning(
                "Aucune donnée numérique exploitable "
                "n'a été trouvée."
            )

            st.stop()

        col_temps = df_clean.columns[0]

        variables = [
            col
            for col in df_clean.columns
            if col != col_temps
            and df_clean[col].notna().any()
        ]

        if not variables:

            st.warning(
                "Aucune variable macroéconomique exploitable."
            )

            st.stop()

        # ----------------------------------------------------
        # STATISTIQUES ET PICS
        # ---------------------------------------
