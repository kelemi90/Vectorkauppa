# varastopaivitys.py

import streamlit as st
import sqlite3

st.set_page_config(page_title="Varaston päivitys", layout="centered", initial_sidebar_state="collapsed")

# Salauskenttä
st.title("🔒 Varaston päivitys")

salasana = st.text_input("Syötä salasana:", type="password")

if salasana != "CcdablYgUIcMfZ30gLMB":
    if salasana:  # Jos syötti jotain mutta väärin
        st.error("Väärä salasana.")
    st.stop()

st.success("Tervetuloa!")

# Yhteys tietokantaan
db_path = "varasto.db"

# Lomake varaston päivitykseen
with st.form("päivityslomake"):
    tuotenimi = st.text_input("Tuotteen nimi (täsmälleen kuten tietokannassa):")
    maara = st.number_input("Lisättävä määrä:", min_value=1, step=1)
    submitted = st.form_submit_button("Lisää varastoon")

    if submitted:
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            # Päivitä olemassa olevan tuotteen saldo
            c.execute("UPDATE varasto SET maara = maara + ? WHERE tuote = ?", (maara, tuotenimi))
            if c.rowcount == 0:
                st.warning("Tuotetta ei löytynyt. Varmista nimi.")
            else:
                conn.commit()
                st.success(f"Lisättiin {maara} kpl tuotetta '{tuotenimi}' varastoon.")

            conn.close()
        except Exception as e:
            st.error(f"Virhe päivityksessä: {e}")
