import streamlit as st
import sqlite3
from datetime import datetime

# Alkuperäiset määrät (sisältää myös piilotetut tuotteet varastosaldoa varten)
alkuperaiset_maarat = {
    # Pöydät ja tuolit
    "Valkoiset muovipöydät": 250,
    "Ikeapöydät": 28,
    "Vaneripöydät B": 57,
    "Vaneripöydät C": 78,
    "Vaneripöydät D": 18,
    "Vaneripöydät E": 100,
    "Vaneripöydät G": 158,
    "Vaneripöydät H": 16,
    "Vaneripöydät F-info": 3,
    "Tuoli": 267,
    "Sohva": 4,
    # Koneet ja toimistotarvikkeet
    "Jimms tehokone": 20,
    "Jimms pelikone": 20,
    "jimms yleisnäyttö": 40,
    "Jimms pelinäyttö": 40,
    "Medialäppäri": 30,
    "PROVO Matto - Hiirimatto": 35,
    "PROVO KUMU PRO - 7.1 tilaäänipelikuuloke": 30,
    "PROVO NOSTE PRO - hiiri": 30,
    "PROVO KAJO OPTO - Näppäimistö": 30,
    "Esperanza EG102": 10,
    "Toimisto näppäimistö": 50,
    "Toimistohiiri": 50,
    "Toimistotuolit": 40,
    # TV
    "info-tv": 87,
    "Kuluttaja-tv": 17,
    "TV virtakaapeli ja hdmi kaapeli": 100,
    "Tv lattiajalat": 29,
    "TV Trussi-kiinnitys": 20,
    "Tv pöytäjalat": 28,
    # Sähkö ja verkko
    "Sähköt 1x16A 230V 3000W": 21,
    "Sähköt 3x16A 400V 9000W": 20,
    "Sähköt 3x32A 400V 15000W": 20,
    "Sähköt Muu": 10,
    "verkko-1G Base-T": 1000,
    "verkko-10G SR": 1000,
    "verkko-10G LR": 1000,
    "Verkkokaapeli": 1000,
    # Standipaketit ja loossit
    "Standi paketti Custom, ota yhteys yhteistyo@vectorama.fi": 4,
    "Ständialueen matotus per neliömetri": 10000,
    "Standipaketti 4x4m": 10,
    "Loossi": 10,
    "Standipaketti 6x4m": 10,
    "Standipaketti 6x8m": 10,
    "Custom standi paketti": 3,
    # Valot
    "Spottivalot": 10,
    "Valaistus": 1000,
    # Kodinkoneet
    "Lasiovinen jääkaappi": 2,
    "Lasi-ikkunallinen arkkupakastin": 1,
    "Pullonkeräys tynnyrit": 30,
    "Arkkupakastin": 2,
    "Jenkkikaappi": 1,
    "Jääkaappipakastin": 1,
    "Kiertoilmauuni": 1,
    "Kylmälaari": 1,
    "Metallinen jääkaappi/pakastin": 1,
    "Mikro": 2,
    "Induktioliesi": 5,
    # Muut
    "Lisätuote": 1000,
    "Taittojalka": 2,

    # Piilotetut tuotteet (vain varastosaldoissa)
    "RGB lediputki 201cm pyöreä": 188,
    "RGB lediputki 201cm litteä": 26,
    "360 led-360 led-yksipäinen-50": 0,
    "360 led-360 led-kaksipäinen-250": 26,
    "360 led-360 led-kaksipäinen-150": 0,
    "360 led-360 led-kaksipäinen-100": 43,
    "360 led-360 led-kaksipäinen-50": 39,
    "360 led-360 led-yksipäinen-250": 0,
    "360 led-360 led-yksipäinen-150": 23,
    "360 led-360 led-yksipäinen-100": 40,
    "RGB wash pixel ohjattu": 30,
    "trussi paketti": 0,
    "Päätylaatta-päätylaatta (eurotruss)": 2,
    "Päätylaatta-päätylaatta (alutruss)": 8,
    "Päätylaatta-päätylaatta (milos)": 3,
    "Päätylaatta-päätylaatta (globaltruss/omavalmiste)": 2,
    "Päätylaatta-päätylaatta 60x60cm rauta (musta) (globaltrus)": 4,
    "Päätylaatta-päätylaatta 60x60cm alumiini (bt-truss)": 4,
    "Päätylaatta": 0,
    "Trussit-Trussit-0,5m trussi": 4,
    "Trussit-Trussit-1m trussi": 8,
    "Trussit-Trussit-1,5m trussi": 0,
    "Trussit-Trussit-2m trussi": 16,
    "Trussit-Trussit-2,5m trussi": 7,
    "Trussit-Trussit-3m trussi": 24,
    "Trussit-Trussit-3,5m trussi": 2,
    "Trussit-Trussit-4m trussi": 12,
    "Trussit-Trussit-4,5m trussi": 4,
    "Trussit-Trussit-5m trussi": 2,
    "Trussit": 0,
    "2D kulma L": 23,
    "3D kulma": 1,
    "4D risteys": 4,
    "t-pala": 3,
}

# Tuotekokonaisuudet (ei sisällä piilotettuja tuotteita)
tuotekokonaisuudet = {
    "Pöydät ja tuolit": [
        "Valkoiset muovipöydät", "Ikeapöydät", "Vaneripöydät B",
        "Vaneripöydät C", "Vaneripöydät D",
        "Vaneripöydät E", "Vaneripöydät G",
        "Vaneripöydät H", "Vaneripöydät F-info",
        "Tuoli", "Sohva"
    ],
    "Koneet ja toimistotarvikkeet": [
        "Jimms tehokone", "Jimms pelikone", "jimms yleisnäyttö", "Jimms pelinäyttö",
        "Medialäppäri", "PROVO Matto - Hiirimatto", "PROVO KUMU PRO - 7.1 tilaäänipelikuuloke",
        "PROVO NOSTE PRO - hiiri", "PROVO KAJO OPTO - Näppäimistö", "Esperanza EG102",
        "Toimisto näppäimistö", "Toimistohiiri", "Taittojalka"
    ],
    "TV": [
        "info-tv", "Kuluttaja-tv", "TV virtakaapeli ja hdmi kaapeli", "Tv lattiajalat",
        "TV Trussi-kiinnitys", "Tv pöytäjalat"
    ],
    "Sähkö ja verkko": [
        "Sähköt 1x16A 230V 3000W", "Sähköt 3x16A 400V 9000W", "Sähköt 3x32A 400V 15000W",
        "Sähköt-vecto-Sähköt-Muu", "verkko-1G Base-T", "verkko-10G SR", "verkko-10G LR",
        "Verkkokaapeli"
    ],
    "Standipaketit ja loossit": [
        "Standi paketti Custom, ota yhteys yhteistyo@vectorama.fi", "Ständialueen matotus per neliömetri",
        "Standipaketti 4x4m", "Loossi", "Standipaketti 6x4m", "Standipaketti 6x8m",
        "Custom standi paketti"
    ],
    "Valot": [
        "Spottivalot", "Valaistus"
    ],
    "Kodinkoneet": [
        "Lasiovinen jääkaappi", "Lasi-ikkunallinen arkkupakastin", "Pullonkeräys tynnyrit",
        "Arkkupakastin", "Jenkkikaappi", "Jääkaappipakastin", "Kiertoilmauuni",
        "Kylmälaari", "Metallinen jääkaappi/pakastin", "Mikro", "Induktioliesi",
        "Lisätuote"
    ],
    "Muut": [
        "Lisätuote", "Taittojalka"
    ]
}

# Funktio tietokantojen alustamiseen
def init_db():
    conn = sqlite3.connect('tilaukset.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tilaukset 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nimi TEXT,
                  tuote TEXT,
                  maara INTEGER,
                  lisatiedot TEXT,
                  toimituspiste TEXT,
                  toimituspaiva TEXT,
                  pvm TEXT)''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('varasto.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS varasto 
                 (tuote TEXT PRIMARY KEY,
                  maara INTEGER)''')
    c.execute("SELECT COUNT(*) FROM varasto")
    if c.fetchone()[0] == 0:
        for tuote, maara in alkuperaiset_maarat.items():
            c.execute("INSERT INTO varasto (tuote, maara) VALUES (?, ?)", (tuote, maara))
    conn.commit()
    conn.close()

# Funktio varaston päivittämiseen
def paivita_varasto(valitut_tuotteet):
    conn = sqlite3.connect('varasto.db')
    c = conn.cursor()
    for tuote, maara in valitut_tuotteet.items():
        if maara > 0:
            c.execute("UPDATE varasto SET maara = maara - ? WHERE tuote = ?", (maara, tuote))
    conn.commit()
    conn.close()

# Funktio varaston nollaamiseen
def nollaa_varasto():
    conn = sqlite3.connect('varasto.db')
    c = conn.cursor()
    c.execute("DELETE FROM varasto")
    for tuote, maara in alkuperaiset_maarat.items():
        c.execute("INSERT INTO varasto (tuote, maara) VALUES (?, ?)", (tuote, maara))
    conn.commit()
    conn.close()

# Funktio varaston hakemiseen
def hae_varasto():
    conn = sqlite3.connect('varasto.db')
    c = conn.cursor()
    c.execute("SELECT tuote, maara FROM varasto")
    varasto = dict(c.fetchall())
    conn.close()
    return varasto

# Funktio tilauksen tallentamiseen
def tallenna_tilaus(nimi, valitut_tuotteet, lisatiedot, toimituspiste, toimituspaiva):
    conn = sqlite3.connect('tilaukset.db')
    c = conn.cursor()
    pvm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for tuote, maara in valitut_tuotteet.items():
        if maara > 0:
            lisatieto = lisatiedot.get(tuote, "")
            c.execute("INSERT INTO tilaukset (nimi, tuote, maara, lisatiedot, toimituspiste, toimituspaiva, pvm) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (nimi, tuote, maara, lisatieto, toimituspiste, toimituspaiva.strftime("%Y-%m-%d"), pvm))
    conn.commit()
    conn.close()
    paivita_varasto(valitut_tuotteet)

# Streamlit-sovellus
def main():
    init_db()
    varasto = hae_varasto()

    st.title("Tilauslomake")

    with st.form(key='tilauslomake'):
        nimi = st.text_input("Nimi")
        toimituspiste = st.text_input("Toimituspiste")
        toimituspaiva = st.date_input("Toimituspäivä", min_value=datetime(2025, 6, 1))

        st.subheader("Valitse tuotteet ja määrät")
        valitut_tuotteet = {}
        lisatiedot = {}

        # Verkko-, Sähköt- ja Lisätuote-tunnistus
        verkko_tuotteet = [t for t in alkuperaiset_maarat.keys() if "verkko" in t.lower()]
        sahko_tuotteet = [t for t in alkuperaiset_maarat.keys() if "sähköt" in t.lower()]
        lisatuote = "Lisätuote"

        # Tuotekokonaisuudet expanderilla
        for kokonaisuus, tuotteet in tuotekokonaisuudet.items():
            with st.expander(kokonaisuus, expanded=False):
                col1, col2 = st.columns(2)
                puolivali = len(tuotteet) // 2

                with col1:
                    for i, tuote in enumerate(tuotteet[:puolivali]):
                        saatavilla = varasto.get(tuote, 0)
                        maara = st.number_input(f"{tuote} (Saatavilla: {saatavilla})", 
                                                min_value=0, max_value=saatavilla, value=0, 
                                                key=f"{tuote}_{i}_col1")
                        valitut_tuotteet[tuote] = maara
                        if maara > 0 and (tuote in verkko_tuotteet or tuote in sahko_tuotteet or tuote == lisatuote):
                            lisatiedot[tuote] = st.text_input(f"Lisätiedot: {tuote}", 
                                                              key=f"lisatieto_{tuote}_{i}_col1")

                with col2:
                    for i, tuote in enumerate(tuotteet[puolivali:]):
                        saatavilla = varasto.get(tuote, 0)
                        maara = st.number_input(f"{tuote} (Saatavilla: {saatavilla})", 
                                                min_value=0, max_value=saatavilla, value=0, 
                                                key=f"{tuote}_{i}_col2")
                        valitut_tuotteet[tuote] = maara
                        if maara > 0 and (tuote in verkko_tuotteet or tuote in sahko_tuotteet or tuote == lisatuote):
                            lisatiedot[tuote] = st.text_input(f"Lisätiedot: {tuote}", 
                                                              key=f"lisatieto_{tuote}_{i}_col2")

        submit_button = st.form_submit_button(label="Lähetä tilaus")

    if submit_button:
        if nimi.strip() == "":
            st.error("Syötä nimi!")
        elif toimituspiste.strip() == "":
            st.error("Syötä toimituspiste!")
        elif sum(valitut_tuotteet.values()) == 0:
            st.error("Valitse ainakin yksi tuote!")
        else:
            tallenna_tilaus(nimi, valitut_tuotteet, lisatiedot, toimituspiste, toimituspaiva)
            st.success(f"Kiitos, {nimi}! Tilauksesi on vastaanotettu.")
            st.experimental_rerun()

    if st.checkbox("Näytä kaikki tilaukset"):
        conn = sqlite3.connect('tilaukset.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tilaukset")
        tilaukset = c.fetchall()
        conn.close()
        
        if tilaukset:
            st.write("### Kaikki tilaukset")
            for tilaus in tilaukset:
                lisatieto = f", Lisätiedot: {tilaus[4]}" if tilaus[4] else ""
                st.write(f"ID: {tilaus[0]}, Nimi: {tilaus[1]}, Tuote: {tilaus[2]}, Määrä: {tilaus[3]}{lisatieto}, "
                         f"Toimituspiste: {tilaus[5]}, Toimituspäivä: {tilaus[6]}, Päivämäärä: {tilaus[7]}")
        else:
            st.write("Ei tilauksia vielä.")

    if st.checkbox("Palauta varasto"):
        salasana = st.text_input("Syötä salasana varaston nollaamiseksi", type="password")
        if st.button("Nollaa varasto"):
            if salasana == "salasana":
                nollaa_varasto()
                st.success("Varasto on nollattu alkuperäisiin määriin!")
                st.experimental_rerun()
            else:
                st.error("Väärä salasana!")

if __name__ == "__main__":
    main()