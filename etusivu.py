import streamlit as st
import sqlite3
from urllib.parse import parse_qs

st.set_page_config(
    page_title="Etusivu",
    layout="centered",
)

# UUSI TAPA: Tarkista URL-parametrit
query_params = st.query_params
if query_params.get("page") == "secret":
    st.title("🔒 Varaston päivitys")

    salasana = st.text_input("Syötä salasana:", type="password")
    if salasana != "CcdablYgUIcMfZ30gLMB":
        if salasana:
            st.error("Väärä salasana.")
        st.stop()

    st.success("Tervetuloa varastonhallintaan!")

    db_path = "varasto.db"

    with st.form("paivitys_lomake"):
        tuotenimi = st.text_input("Tuotteen nimi:")
        maara = st.number_input("Lisättävä määrä:", min_value=1, step=1)
        submitted = st.form_submit_button("Lisää varastoon")

        if submitted:
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("UPDATE varasto SET saldo = saldo + ? WHERE tuote = ?", (maara, tuotenimi))
                if c.rowcount == 0:
                    st.warning("Tuotetta ei löytynyt.")
                else:
                    conn.commit()
                    st.success(f"{maara} lisätty tuotteen '{tuotenimi}' saldoon.")
                conn.close()
            except Exception as e:
                st.error(f"Virhe: {e}")
    st.stop()

# Oletusnäkymä (etusivu)
st.title("Vector infrashop kauppa")

st.markdown(
    """
    Tältä sivustolta löydät kaikki tilattavat tuotteet, kuten esim. pöydät, 
    tuolit, TV:t, yms.

    Kun lisäätte useita kappaleita samasta tuotteesta valikkoon, niin tarkastakaa
    että valikkoon on tullut oikea määrä kyseisiä tuotteita. Tällä hetkellä sivusto
    päivittää jokaisen valinnan pienellä viiveellä, joten nopeasti klikkaamalla 
    sivu saattaa valita vain ensimmäisen lisäyksen, jättäen loput huomioimatta.
    """
)
