import streamlit as st
import sqlite3

# --- Tietokantayhteys ---
def get_connection():
    return sqlite3.connect("varasto.db", check_same_thread=False)

# --- Hae kaikki tilaukset ---
def get_tilaukset():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, tuote, määrä, tila FROM tilaukset")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Hae yksittäinen tilaus ID:llä ---
def get_tilaus(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, tuote, määrä, tila FROM tilaukset WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    return row

# --- Päivitä tilaus ---
def update_tilaus(id, tuote, määrä, tila):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tilaukset SET tuote = ?, määrä = ?, tila = ? WHERE id = ?", (tuote, määrä, tila, id))
    conn.commit()
    conn.close()

# --- Streamlit UI ---
st.title("📝 Muokkaa tilausta")

tilaukset = get_tilaukset()
tilaus_idt = [str(r[0]) + " | " + r[1] for r in tilaukset]
valinta = st.selectbox("Valitse tilaus muokattavaksi:", tilaus_idt)

if valinta:
    valittu_id = int(valinta.split(" | ")[0])
    tilaus = get_tilaus(valittu_id)

    if tilaus:
        st.subheader("Muokkaa tietoja")
        uusi_tuote = st.text_input("Tuote", value=tilaus[1])
        uusi_maara = st.number_input("Määrä", value=tilaus[2], min_value=1)
        uusi_tila = st.selectbox("Tila", ["Uusi", "Käsittelyssä", "Lähetetty", "Peruttu"], index=["Uusi", "Käsittelyssä", "Lähetetty", "Peruttu"].index(tilaus[3]))

        if st.button("💾 Tallenna muutokset"):
            update_tilaus(valittu_id, uusi_tuote, uusi_maara, uusi_tila)
            st.success("Tilaus päivitetty onnistuneesti!")
            st.rerun()
    else:
        st.error("Tilausta ei löytynyt.")
