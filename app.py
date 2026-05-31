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
# FONCTIONS DE CHARGEMENT
# ----------------------------
@st.cache_data
def load_excel(url, sheet):
    return pd.read_excel(url, sheet_name=sheet)


def clean_numeric_df(df, time_col_name=None):
    """
    Nettoie un DataFrame en supprimant la ligne d'unités et les lignes finales
    de type 'Nombre total d'observation'. Convertit toutes les colonnes numériques.
    """
    df_clean = df.copy()
    time_col = time_col_name if time_col_name else df_clean.columns[0]
    # Conversion de la colonne temporelle en numérique
    df_clean[time_col] = pd.to_numeric(df_clean[time_col], errors="coerce")
    df_clean = df_clean.dropna(subset=[time_col])
    # Conversion des autres colonnes
    for col in df_clean.columns:
        if col != time_col:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
    return df_clean


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
        "Données macroéconomiques"
    ]
)

# ----------------------------
# SECTION 1 : ACCUEIL
# ----------------------------
if section == "Accueil":

    st.subheader("Plateforme d'information")

    st.write(
        """
        Congo Coffee Data est une plateforme de données économiques dédiée à la filière café en RDC.

        Elle vise à réduire l'asymétrie d'information en mettant à disposition des données fiables sur :
        - la production ;
        - les prix ;
        - les variables macroéconomiques liées au secteur.

        La plateforme s'adresse aux producteurs, acheteurs, investisseurs, institutions publiques et chercheurs.
        """
    )

    st.info(
        "Cette plateforme est conçue comme un outil d'aide à la décision et de transparence du marché."
    )

    # ----------------------------
    # ACTUALITÉS 2025
    # ----------------------------
    st.markdown("---")
    st.subheader("Actualités 2025")
    st.caption("Chiffres clés de la filière café en RDC pour l'année 2025")

    try:
        df_prod_ann = clean_numeric_df(load_excel(URL_PRODUCTION_PRIX, "Annual Production"))
        df_price_ann = clean_numeric_df(load_excel(URL_PRODUCTION_PRIX, "Annual Price"))

        time_col_p = df_prod_ann.columns[0]
        time_col_pr = df_price_ann.columns[0]

        # Données 2025 et 2024 pour calculer la variation
        row_2025_prod = df_prod_ann[df_prod_ann[time_col_p] == 2025]
        row_2024_prod = df_prod_ann[df_prod_ann[time_col_p] == 2024]
        row_2025_price = df_price_ann[df_price_ann[time_col_pr] == 2025]
        row_2024_price = df_price_ann[df_price_ann[time_col_pr] == 2024]

        # --- Production 2025 ---
        st.markdown("#### Production 2025 (en tonnes)")
        c1, c2, c3 = st.columns(3)

        if not row_2025_prod.empty:
            total_2025 = float(row_2025_prod["Total"].values[0])
            robusta_2025 = float(row_2025_prod["Robusta"].values[0])
            arabica_2025 = float(row_2025_prod["Arabica"].values[0])

            delta_total = None
            delta_rob = None
            delta_ara = None
            if not row_2024_prod.empty:
                t24 = float(row_2024_prod["Total"].values[0])
                r24 = float(row_2024_prod["Robusta"].values[0])
                a24 = float(row_2024_prod["Arabica"].values[0])
                delta_total = f"{((total_2025 - t24) / t24 * 100):+.1f}% vs 2024"
                delta_rob = f"{((robusta_2025 - r24) / r24 * 100):+.1f}% vs 2024"
                delta_ara = f"{((arabica_2025 - a24) / a24 * 100):+.1f}% vs 2024"

            c1.metric("Production totale", f"{total_2025:,.0f} t", delta_total, delta_color="normal")
            c2.metric("Robusta", f"{robusta_2025:,.0f} t", delta_rob, delta_color="normal")
            c3.metric("Arabica", f"{arabica_2025:,.0f} t", delta_ara, delta_color="normal")
        else:
            st.warning("Aucune donnée de production disponible pour 2025.")

        # --- Prix 2025 ---
        st.markdown("#### Prix 2025 ($/kg)")
        c1, c2 = st.columns(2)

        if not row_2025_price.empty:
            rob_price_2025 = float(row_2025_price["Robusta"].values[0])
            ara_price_2025 = float(row_2025_price["Arabica"].values[0])

            delta_rob_p = None
            delta_ara_p = None
            if not row_2024_price.empty:
                r24 = float(row_2024_price["Robusta"].values[0])
                a24 = float(row_2024_price["Arabica"].values[0])
                delta_rob_p = f"{((rob_price_2025 - r24) / r24 * 100):+.1f}% vs 2024"
                delta_ara_p = f"{((ara_price_2025 - a24) / a24 * 100):+.1f}% vs 2024"

            c1.metric("Prix Robusta", f"{rob_price_2025:.2f} $/kg", delta_rob_p, delta_color="normal")
            c2.metric("Prix Arabica", f"{ara_price_2025:.2f} $/kg", delta_ara_p, delta_color="normal")
        else:
            st.warning("Aucune donnée de prix disponible pour 2025.")

        st.caption("Sources : Banque Centrale du Congo & Banque mondiale")

    except Exception as e:
        st.error(f"Erreur lors du chargement des actualités 2025 : {e}")


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
            df_graph_ann = df_ann_prod.copy()
            df_graph_ann[df_graph_ann.columns[0]] = pd.to_numeric(df_graph_ann[df_graph_ann.columns[0]], errors='coerce')
            df_graph_ann = df_graph_ann.dropna(subset=[df_graph_ann.columns[0]])

            x = df_graph_ann.columns[0]
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
# SECTION 3 : Données macroéconomiques
# ----------------------------
elif section == "Données macroéconomiques":

    st.subheader("Analyse macroéconomique de la filière café")

    try:
        df_ardl = load_excel(URL_DATA_SITE, "Data for ARDL")

        st.write("### Base de données macroéconomiques")
        st.dataframe(df_ardl, use_container_width=True)

        # --- NETTOYAGE SÉCURISÉ POUR L'ANALYSE ---
        df_clean = df_ardl.copy()
        col_temps = df_clean.columns[0]

        df_clean[col_temps] = pd.to_numeric(df_clean[col_temps], errors="coerce")
        df_clean = df_clean.dropna(subset=[col_temps])

        for col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

        df_clean = df_clean.dropna()

        # --- TABLEAU DES PICS ---
        st.markdown("### Tableau récapitulatif des pics")
        st.caption("Valeurs maximales et minimales observées pour chaque variable macroéconomique, avec les années correspondantes.")

        variables_pics = [c for c in df_clean.columns if c != col_temps]
        pics_data = []
        for var in variables_pics:
            serie = df_clean[[col_temps, var]].dropna()
            if serie.empty:
                continue
            idx_max = serie[var].idxmax()
            idx_min = serie[var].idxmin()
            pics_data.append({
                "Variable": var,
                "Pic maximum": round(float(serie.loc[idx_max, var]), 4),
                "Année du pic max": int(serie.loc[idx_max, col_temps]),
                "Pic minimum": round(float(serie.loc[idx_min, var]), 4),
                "Année du pic min": int(serie.loc[idx_min, col_temps]),
                "Amplitude (max - min)": round(float(serie[var].max() - serie[var].min()), 4),
                "Moyenne": round(float(serie[var].mean()), 4),
            })

        df_pics = pd.DataFrame(pics_data)
        st.dataframe(df_pics, use_container_width=True, hide_index=True)

        # --- GRAPHIQUE TEMPOREL ---
        st.markdown("### Analyse temporelle")
        variables = list(df_clean.columns)

        x_axis = variables[0]
        y_var = st.selectbox("Sélectionner la variable à analyser", variables[1:])

        fig = px.line(df_clean, x=x_axis, y=y_var, title=f"Trajectoire de la variable : {y_var}")
        fig.update_layout(template="plotly_white")

        # Annoter les pics max et min sur le graphique sélectionné
        serie_sel = df_clean[[x_axis, y_var]].dropna()
        if not serie_sel.empty:
            idx_max = serie_sel[y_var].idxmax()
            idx_min = serie_sel[y_var].idxmin()
            x_max = serie_sel.loc[idx_max, x_axis]
            y_max = serie_sel.loc[idx_max, y_var]
            x_min = serie_sel.loc[idx_min, x_axis]
            y_min = serie_sel.loc[idx_min, y_var]

            fig.add_scatter(
                x=[x_max], y=[y_max],
                mode="markers+text",
                marker=dict(color="green", size=12, symbol="triangle-up"),
                text=[f"Max : {y_max:.2f}"],
                textposition="top center",
                name="Pic max"
            )
            fig.add_scatter(
                x=[x_min], y=[y_min],
                mode="markers+text",
                marker=dict(color="red", size=12, symbol="triangle-down"),
                text=[f"Min : {y_min:.2f}"],
                textposition="bottom center",
                name="Pic min"
            )

        st.plotly_chart(fig, use_container_width=True)

        # --- MATRICE DE CORRÉLATION ---
        st.markdown("### Corrélation entre variables (Pearson)")

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
            
