import streamlit as st
import sqlite3
from datetime import datetime

# Funktio tietokannan alustamiseen
def init_db():
    conn = sqlite3.connect('tilaukset.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tilaukset 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nimi TEXT,
                  tuote TEXT,
                  maara INTEGER,
                  pvm TEXT)''')
    conn.commit()
    conn.close()

# Funktio tilauksen tallentamiseen
def tallenna_tilaus(nimi, tuote, maara):
    conn = sqlite3.connect('tilaukset.db')
    c = conn.cursor()
    pvm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO tilaukset (nimi, tuote, maara, pvm) VALUES (?, ?, ?, ?)",
              (nimi, tuote, maara, pvm))
    conn.commit()
    conn.close()

# Streamlit-sovellus
def main():
    # Alusta tietokanta
    init_db()

    # Sovelluksen otsikko
    st.title("Tilauslomake")

    # Esivalitut tuotteet
    tuotteet = [
        "Kahvi (5€)",
        "Tee (3€)",
        "Pullapartti (8€)",
        "Keksi (2€)"
    ]

    # Lomake
    with st.form(key='tilauslomake'):
        nimi = st.text_input("Nimi")
        tuote = st.selectbox("Valitse tuote", tuotteet)
        maara = st.number_input("Määrä", min_value=0, max_value=20, value=0)
        submit_button = st.form_submit_button(label="Lähetä tilaus")

    # Kun lomake lähetetään
    if submit_button:
        if nimi.strip() == "":
            st.error("Syötä nimi!")
        else:
            tallenna_tilaus(nimi, tuote, maara)
            st.success(f"Kiitos, {nimi}! Tilauksesi ({maara} x {tuote}) on vastaanotettu.")

    # Näytä kaikki tilaukset (valinnainen)
    if st.checkbox("Näytä kaikki tilaukset"):
        conn = sqlite3.connect('tilaukset.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tilaukset")
        tilaukset = c.fetchall()
        conn.close()
        
        if tilaukset:
            st.write("### Kaikki tilaukset")
            for tilaus in tilaukset:
                st.write(f"ID: {tilaus[0]}, Nimi: {tilaus[1]}, Tuote: {tilaus[2]}, Määrä: {tilaus[3]}, Päivämäärä: {tilaus[4]}")
        else:
            st.write("Ei tilauksia vielä.")

if __name__ == "__main__":
    main()