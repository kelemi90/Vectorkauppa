import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Tilausten hallinta", layout="wide")
st.title("📦 Tilausten muokkaus ja poisto")

# Yhdistä tietokantaan ja hae tilaukset
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
# Toimituspisteen valinta
toimituspisteet = tilaukset_df["toimituspiste"].dropna().unique()
valittu_piste = st.selectbox("Valitse toimituspiste", toimituspisteet)

# Suodata tilaukset toimituspisteen mukaan
suodatettu_df = tilaukset_df[tilaukset_df["toimituspiste"] == valittu_piste].reset_index(drop=True)

if suodatettu_df.empty:
    st.warning("Ei tilauksia valitulle toimituspisteelle.")
    st.stop()

st.subheader(f"Tilaukset toimituspisteelle: {valittu_piste}")

# Lisää Poista-valintaruutu
suodatettu_df["Poista"] = False

# Näytä muokattava taulukko
muokattu_df = st.data_editor(suodatettu_df, num_rows="dynamic")

with st.form("hallintalomake"):
    paivita = st.form_submit_button("💾 Päivitä valitut tilaukset")
    poista = st.form_submit_button("🗑️ Poista valitut tilaukset")

    if paivita:
        try:
            conn = sqlite3.connect('tilaukset.db')
            c = conn.cursor()
            for _, rivi in muokattu_df.iterrows():
                if not rivi["Poista"]:
                    c.execute("""
                        UPDATE tilaukset SET
                            nimi = ?, tuote = ?, maara = ?, lisatiedot = ?,
                            toimituspiste = ?, toimituspaiva = ?
                        WHERE id = ?
                    """, (
                        rivi["nimi"], rivi["tuote"], rivi["maara"], rivi["lisatiedot"],
                        rivi["toimituspiste"], rivi["toimituspaiva"], rivi["id"]
                    ))
            conn.commit()
            conn.close()
            st.success("Valitut tilaukset päivitetty onnistuneesti.")
            st.rerun()
        except Exception as e:
            st.error(f"Virhe päivityksessä: {e}")

    if poista:
        try:
            conn = sqlite3.connect('tilaukset.db')
            c = conn.cursor()
            poistettavat = muokattu_df[muokattu_df["Poista"]]
            for _, rivi in poistettavat.iterrows():
                c.execute("DELETE FROM tilaukset WHERE id = ?", (rivi["id"],))
            conn.commit()
            conn.close()
            st.success("Valitut tilaukset poistettu onnistuneesti.")
            st.rerun()
        except Exception as e:
            st.error(f"Virhe poistossa: {e}")
