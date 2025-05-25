import streamlit as st
import sqlite3

st.set_page_config(page_title="Varaston päivitys", layout="centered", initial_sidebar_state="collapsed")

# Salauskenttä
st.title("🔒 Varaston päivitys")

salasana = st.text_input("Syötä salasana:", type="password")

if salasana != "CcdablYgUIcMfZ30gLMB":
    if salasana:
        st.error("Väärä salasana.")
    st.stop()

st.success("Tervetuloa!")

db_path = "varasto.db"

with st.form("päivityslomake"):
    tuotenimi = st.text_input("Tuotteen nimi (täsmälleen kuten tietokannassa):")
    maara = st.number_input("Lisättävä määrä:", min_value=1, step=1)
    submitted = st.form_submit_button("Lisää varastoon")

    if submitted:
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            c.execute("UPDATE varasto SET maara = maara + ? WHERE tuote = ?", (maara, tuotenimi))
            if c.rowcount == 0:
                c.execute("INSERT INTO varasto (tuote, maara) VALUES (?, ?)", (tuotenimi, maara))
                st.success(f"Tuote '{tuotenimi}' lisätty uutena varastoon määrällä {maara} kpl.")
            else:
                st.success(f"Lisättiin {maara} kpl tuotetta '{tuotenimi}' varastoon.")

            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Virhe päivityksessä: {e}")
