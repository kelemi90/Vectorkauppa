import streamlit as st
import sqlite3
from datetime import datetime
import os


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
        "Sähköt Muu", "verkko-1G Base-T", "verkko-10G SR", "verkko-10G LR",
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
# Tietokannan polku
# DB_PATH = "/workspaces/Vectorkauppa/gitrepo/tilaukset.db"

# Funktio tietokantojen alustamiseen
def init_db():
    conn = sqlite3.connect('tilaukset.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tilaukset 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nimi TEXT, tuote TEXT, maara INTEGER, lisatiedot TEXT,
                  toimituspiste TEXT, toimituspaiva TEXT, pvm TEXT)''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('varasto.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS varasto 
                 (tuote TEXT PRIMARY KEY, maara INTEGER)''')
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

# Git-komennot suoraan
    os.chdir("/Vectorkauppa_app/gitrepo")
    os.system("git add tilaukset.db")
    os.system(f'git commit -m "Uusi tilaus: {nimi} - {tuote} x{maara}"')
    os.system("git push origin main")

# Streamlit-sovellus
def main():
    init_db()
    varasto = hae_varasto()

    if 'valitut_tuotteet' not in st.session_state:
        st.session_state.valitut_tuotteet = {tuote: 0 for tuote in alkuperaiset_maarat.keys()}
    if 'lisatiedot' not in st.session_state:
        st.session_state.lisatiedot = {}
    if 'nimi' not in st.session_state:
        st.session_state.nimi = ""
    if 'toimituspiste' not in st.session_state:
        st.session_state.toimituspiste = ""
    if 'toimituspaiva' not in st.session_state:
        st.session_state.toimituspaiva = datetime(2025, 6, 1)

    st.title("Tilauslomake")

    # Syöttökentät ilman st.formia
    st.session_state.nimi = st.text_input("Nimi", value=st.session_state.nimi)
    st.session_state.toimituspiste = st.text_input("Toimituspiste", value=st.session_state.toimituspiste)
    st.session_state.toimituspaiva = st.date_input("Toimituspäivä", value=st.session_state.toimituspaiva, min_value=datetime(2025, 6, 1))

    st.subheader("Valitse tuotteet ja määrät")
    
    # Verkko-, Sähköt- ja Lisätuote-tunnistus
    verkko_tuotteet = ["verkko-1G Base-T", "verkko-10G SR", "verkko-10G LR"]
    sahko_tuotteet = ["Sähköt 1x16A 230V 3000W", "Sähköt 3x16A 400V 9000W", "Sähköt 3x32A 400V 15000W", "Sähköt Muu"]
    lisatuote = "Lisätuote"

    # Tuotekokonaisuudet expanderilla
    for kokonaisuus, tuotteet in tuotekokonaisuudet.items():
            with st.expander(kokonaisuus, expanded=False):
                for tuote in tuotteet:
                    if tuote not in alkuperaiset_maarat:
                        st.warning(f"Tuotetta '{tuote}' ei löydy varastosta. Tarkista nimi!")
                        continue
                    
                    saatavilla = varasto.get(tuote, 0)
                    unique_key = f"{kokonaisuus}_{tuote}_maara"
                    
                    # Käytä st.number_input callback-funktiolla viiveen poistamiseksi
                    def update_maara(tuote=tuote, unique_key=unique_key):
                        st.session_state.valitut_tuotteet[tuote] = st.session_state[unique_key]

                    maara = st.number_input(
                        f"{tuote} (Saatavilla: {saatavilla})",
                        min_value=0, max_value=saatavilla,
                        value=st.session_state.valitut_tuotteet.get(tuote, 0),
                        key=unique_key,
                        on_change=update_maara
                    )

                    # Näytä lisätietokenttä vain, jos määrä > 0
                    if st.session_state.valitut_tuotteet[tuote] > 0 and (tuote in verkko_tuotteet or tuote in sahko_tuotteet or tuote == lisatuote):
                        lisatieto_key = f"{kokonaisuus}_{tuote}_lisatieto"
                        
                        def update_lisatieto(tuote=tuote, lisatieto_key=lisatieto_key):
                            st.session_state.lisatiedot[tuote] = st.session_state[lisatieto_key]

                        st.text_input(
                            f"Lisätiedot: {tuote}",
                            value=st.session_state.lisatiedot.get(tuote, ""),
                            key=lisatieto_key,
                            on_change=update_lisatieto
                        )

    # Erillinen lähetysnappi
    if st.button("Lähetä tilaus"):
        if not st.session_state.nimi.strip():
            st.error("Syötä nimi!")
        elif not st.session_state.toimituspiste.strip():
            st.error("Syötä toimituspiste!")
        elif sum(st.session_state.valitut_tuotteet.values()) == 0:
            st.error("Valitse ainakin yksi tuote!")
        else:
            tallenna_tilaus(
                st.session_state.nimi,
                st.session_state.valitut_tuotteet,
                st.session_state.lisatiedot,
                st.session_state.toimituspiste,
                st.session_state.toimituspaiva
            )
            st.success(f"Kiitos, {st.session_state.nimi}! Tilauksesi on vastaanotettu.")
            # Nollaa lomake
            st.session_state.valitut_tuotteet = {tuote: 0 for tuote in alkuperaiset_maarat.keys()}
            st.session_state.lisatiedot = {}
            st.session_state.nimi = ""
            st.session_state.toimituspiste = ""
            st.session_state.toimituspaiva = datetime(2025, 6, 1)

    # Varaston palautusmahdollisuus
    if st.checkbox("Palauta varasto"):
        salasana = st.text_input("Syötä salasana varaston nollaamiseksi", type="password")
        if st.button("Nollaa varasto"):
            if salasana == "CcdablYgUIcMfZ30gLMB":  # Vaihda halutessasi turvallisempi salasana
                nollaa_varasto()
                st.success("Varasto on nollattu alkuperäisiin määriin!")
                st.rerun()  # Päivittää sivun automaattisesti
            else:
                st.error("Väärä salasana!")

if __name__ == "__main__":
    main()
