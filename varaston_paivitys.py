import streamlit as st
import sqlite3
import os

# Tuotekategoriat ja tuotteet
tuotekokonaisuudet = {
    "Pöydät ja tuolit": ["Valkoiset muovipöydät", "Ikeapöydät", "Vaneripöydät B", "Vaneripöydät C", "Vaneripöydät D", "Vaneripöydät E", "Vaneripöydät G", "Vaneripöydät H", "Vaneripöydät F-info", "Tuoli", "Sohva"],
    "Koneet ja toimistotarvikkeet": ["Tehokone", "Pelikone", "Yleisnäyttö", "Pelinäyttö", "Medialäppäri", "PROVO Matto - Hiirimatto", "PROVO KUMU PRO - 7.1 tilaäänipelikuuloke", "PROVO NOSTE PRO - hiiri", "PROVO KAJO OPTO - Näppäimistö", "Esperanza EG102", "Toimisto näppäimistö", "Toimistohiiri", "Taittojalka"],
    "TV": ["info-tv", "Kuluttaja-tv", "TV virtakaapeli ja hdmi kaapeli", "Tv lattiajalat", "TV Trussi-kiinnitys", "Tv pöytäjalat"],
    "Sähkö ja verkko": ["Sähköt 1x16A 230V 3000W", "Sähköt 3x16A 400V 9000W", "Sähköt 3x32A 400V 15000W", "Sähköt Muu", "verkko-1G Base-T", "verkko-10G SR", "verkko-10G LR", "Verkkokaapeli"],
    "Standipaketit ja loossit": ["Standi paketti Custom, ota yhteys yhteistyo@vectorama.fi", "Ständialueen matotus per neliömetri", "Standipaketti 4x4m", "Loossi", "Standipaketti 6x4m", "Standipaketti 6x8m"],
    "Valot": ["Spottivalot", "Valaistus"],
    "Kodinkoneet": ["Lasiovinen jääkaappi", "Lasi-ikkunallinen arkkupakastin", "Pullonkeräys tynnyrit", "Arkkupakastin", "Jenkkikaappi", "Jääkaappipakastin", "Kiertoilmauuni", "Kylmälaari", "Metallinen jääkaappi/pakastin", "Mikro", "Induktioliesi", "Lisätuote"],
    "Muut": ["Lisätuote", "Taittojalka"]
}

# Tietokantapolku
def get_db_connection():
    db_polku = os.path.join("pages", "varasto.db")
    return sqlite3.connect(db_polku)

# Luo varastotaulu
def luo_varastotaulu():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS varasto (
            tuote TEXT PRIMARY KEY,
            saldo INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Päivitä saldo
def paivita_saldo(tuote, maara_muutos):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT saldo FROM varasto WHERE tuote = ?", (tuote,))
    tulos = c.fetchone()

    if tulos:
        uusi_saldo = tulos[0] + maara_muutos
        c.execute("UPDATE varasto SET saldo = ? WHERE tuote = ?", (uusi_saldo, tuote))
    else:
        c.execute("INSERT INTO varasto (tuote, saldo) VALUES (?, ?)", (tuote, maara_muutos))

    conn.commit()
    conn.close()

# Hae varasto
def hae_varasto():
    conn = get_db_connection()
    df = conn.execute("SELECT tuote, saldo FROM varasto ORDER BY tuote").fetchall()
    conn.close()
    return df

# Streamlit-pääsivu
def main():
    st.set_page_config(page_title="Varasto", layout="centered", initial_sidebar_state="collapsed")
    st.title("Varaston saldon päivitys")

    luo_varastotaulu()

    st.subheader("Päivitä saldo")

    # Valitse kategoria ja tuote alasvetovalikosta
    valittu_kategoria = st.selectbox("Valitse tuotekategoria", list(tuotekokonaisuudet.keys()))
    valittu_tuote = st.selectbox("Valitse tuote", tuotekokonaisuudet[valittu_kategoria])

    maara = st.number_input("Määrän muutos (voi olla negatiivinen)", value=0, step=1)

    if st.button("Päivitä saldo"):
        if maara == 0:
            st.info("Määrän muutos on 0 — mitään ei päivitetty.")
        else:
            paivita_saldo(valittu_tuote, int(maara))
            st.success(f"Tuotteen **{valittu_tuote}** saldo päivitetty {maara:+}.")

    st.divider()

    st.subheader("Varaston sisältö")
    data = hae_varasto()
    if data:
        st.table(data)
    else:
        st.write("Varasto on tyhjä.")

if __name__ == "__main__":
    main()
