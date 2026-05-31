# ----------------------------
# SECTION 1 : ACCUEIL
# ----------------------------
if section == "Accueil":

    st.subheader("Plateforme d'information")

    st.write(
        """
        Congo Coffee Data est une plateforme dédiée aux données économiques de la filière café en RDC.
        """
    )

    try:
        df_prod = load_excel(URL_PRODUCTION_PRIX, "Annual Production")
        df_price = load_excel(URL_PRODUCTION_PRIX, "Annual Price")

        st.markdown("## Actualité — Filière Café (2025)")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Production 2025",
                f"{df_prod.iloc[-1]['Total']:,.0f} tonnes"
            )

        with col2:
            st.metric(
                "Prix 2025",
                f"{df_price.iloc[-1]['Total']:,.2f} $/kg"
            )

    except Exception:
        st.warning("Impossible de charger les données d’actualité 2025.")

    st.info(
        "Objectif : réduire l’asymétrie d’information et faciliter les décisions économiques."  
    )


st.dataframe(df_ardl, use_container_width=True)

# ----------------------------
# VALEURS MAX / MIN
# ----------------------------

st.markdown("### Pics macroéconomiques")

col1, col2 = st.columns(2)

with col1:
    st.write("Valeurs maximales")
    st.dataframe(
        df_clean.describe().loc[["max"]],
        use_container_width=True
    )

with col2:
    st.write("Valeurs minimales")
    st.dataframe(
        df_clean.describe().loc[["min"]],
        use_container_width=True
)

st.markdown("### Observations extrêmes")

variable_pic = st.selectbox(
    "Variable",
    variables[1:]
)

annee_max = df_clean.loc[
    df_clean[variable_pic].idxmax(),
    x_axis
]

annee_min = df_clean.loc[
    df_clean[variable_pic].idxmin(),
    x_axis
]

st.write(f"📈 Pic observé en : **{annee_max}**")
st.write(f"📉 Creux observé en : **{annee_min}**")
