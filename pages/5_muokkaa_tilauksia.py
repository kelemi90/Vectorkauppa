import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Tilausten hallinta", layout="wide")
st.title("📦 Tilausten muokkaus ja poisto")

if "ohje_luettu" not in st.session_state:
    st.session_state.ohje_luettu = False

if not st.session_state.ohje_luettu:
    st.warning("Ole hyvä ja lue ohjeet ennen tilausten muokkausta!")
    st.write("""
        Ohjeet:
        - Voit muokata tai poistaa tilauksia. Valitse toimituspiste, jonka tilauksia haluat hallita.
        - Tee ensin kaikki haluamasi muutokset ja tallenna ne ennen kuin poistat tilauksia.
        - Poistaminen on pysyvää, joten ole varovainen.
    """)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kyllä, olen lukenut ohjeet"):
            st.session_state.ohje_luettu = True
            st.rerun()
    with col2:
        if st.button("Ei, näytä ohjeet uudelleen"):
            st.info("Ole hyvä ja lue ohjeet huolellisesti ennen jatkamista.")
    st.stop()

# --- Ladataan tilaukset ---
conn = sqlite3.connect('tilaukset.db')
tilaukset_df = pd.read_sql_query("SELECT * FROM tilaukset", conn)
conn.close()

if tilaukset_df.empty:
    st.info("Ei tilauksia.")
    st.stop()

# Ohjeistus
st.markdown("""
		## Tilausten hallinta

		Voit muokata tai poistaa tilauksia. Valitse toimituspiste, jonka tilauksia haluat hallita. Kun olet valinnut toimituspisteen, näet siihen liittyvät tilaukset ja voit alkaa muokkaamaan niitä suoraan taulukosta tai valita poistettavat tilaukset "Poista"-valintaruudusta.

		Muista, että muutokset tallennetaan tietokantaan, joten varmista, että teet muutokset huolellisesti. Kun olet tehnyt muutokset, klikkaa "Päivitä valitut tilaukset" tallentaaksesi ne tai "Poista valitut tilaukset" poistaaksesi ne tietokannasta.

		Et voi tehdä muutoksia tilauksiin ja samalla poistaa toista kohtaa, joten tee ensin kaikki haluamasi muutokset ja tallenna ne ennen kuin poistat tilauksia.

		#### **Huom:** Poistaminen on pysyvää, joten varmista, että haluat todella poistaa tilaukset ennen kuin teet sen.
		""")

# --- Valitse toimituspiste ---
toimituspisteet = tilaukset_df["toimituspiste"].dropna().unique()
valittu_piste = st.selectbox("Valitse toimituspiste", toimituspisteet)
suodatettu_df = tilaukset_df[tilaukset_df["toimituspiste"] == valittu_piste].reset_index(drop=True)

if suodatettu_df.empty:
    st.warning("Ei tilauksia valitulle toimituspisteelle.")
    st.stop()

st.subheader(f"Tilaukset toimituspisteelle: {valittu_piste}")

# --- Lisää "Poista"-sarake ---
suodatettu_df["Poista"] = False

# --- Haetaan varastotuotteet alasvetovalikkoon ---
conn_varasto = sqlite3.connect('varasto.db')
varasto_tuotteet = pd.read_sql_query("SELECT DISTINCT tuote FROM varasto", conn_varasto)["tuote"].tolist()
conn_varasto.close()

# --- Näytetään muokattava taulukko, tuote-sarakkeessa alasvetovalikko ---
muokattu_df = st.data_editor(
    suodatettu_df,
    num_rows="dynamic",
    column_config={
        "tuote": st.column_config.SelectboxColumn("Tuote", options=varasto_tuotteet),
    }
)

with st.form("hallintalomake"):
    paivita = st.form_submit_button("💾 Päivitä valitut tilaukset")
    poista = st.form_submit_button("🗑️ Poista valitut tilaukset")

    if paivita:
        try:
            conn_tilaukset = sqlite3.connect('tilaukset.db')
            c_tilaukset = conn_tilaukset.cursor()

            conn_varasto = sqlite3.connect('varasto.db')
            c_varasto = conn_varasto.cursor()

            for _, rivi in muokattu_df.iterrows():
                if not rivi["Poista"]:
                    # Haetaan alkuperäinen määrä ja tuote
                    c_tilaukset.execute("SELECT maara, tuote FROM tilaukset WHERE id = ?", (rivi["id"],))
                    tulos = c_tilaukset.fetchone()
                    if tulos is None:
                        continue
                    alkuperainen_maara, alkuperainen_tuote = tulos
                    uusi_maara = rivi["maara"]
                    maara_ero = uusi_maara - alkuperainen_maara

                    # Päivitä tilaus
                    c_tilaukset.execute("""
                        UPDATE tilaukset SET
                            nimi = ?, tuote = ?, maara = ?, lisatiedot = ?,
                            toimituspiste = ?, toimituspaiva = ?
                        WHERE id = ?
                    """, (
                        rivi["nimi"], rivi["tuote"], uusi_maara, rivi["lisatiedot"],
                        rivi["toimituspiste"], rivi["toimituspaiva"], rivi["id"]
                    ))

                    # Päivitä varasto
                    c_varasto.execute("UPDATE varasto SET maara = maara - ? WHERE tuote = ?", (maara_ero, alkuperainen_tuote))

            conn_tilaukset.commit()
            conn_varasto.commit()
            conn_tilaukset.close()
            conn_varasto.close()

            st.success("Valitut tilaukset ja varasto päivitetty onnistuneesti.")
            st.rerun()

        except Exception as e:
            st.error(f"Virhe päivityksessä: {e}")

    if poista:
        try:
            conn_tilaukset = sqlite3.connect('tilaukset.db')
            c_tilaukset = conn_tilaukset.cursor()

            conn_varasto = sqlite3.connect('varasto.db')
            c_varasto = conn_varasto.cursor()

            poistettavat = muokattu_df[muokattu_df["Poista"]]

            for _, rivi in poistettavat.iterrows():
                c_varasto.execute("UPDATE varasto SET maara = maara + ? WHERE tuote = ?", (rivi["maara"], rivi["tuote"]))
                c_tilaukset.execute("DELETE FROM tilaukset WHERE id = ?", (rivi["id"],))

            conn_tilaukset.commit()
            conn_varasto.commit()
            conn_tilaukset.close()
            conn_varasto.close()

            st.success("Valitut tilaukset poistettu ja varasto päivitetty onnistuneesti.")
            st.rerun()

        except Exception as e:
            st.error(f"Virhe poistossa: {e}")
