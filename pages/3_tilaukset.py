import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os

# Tuotekokonaisuudet
tuotekokonaisuudet = {
    "Pöydät ja tuolit": ["Valkoiset muovipöydät", "Ikeapöydät", "Vaneripöydät B", "Vaneripöydät C", "Vaneripöydät D", "Vaneripöydät E", "Vaneripöydät G", "Vaneripöydät H", "Vaneripöydät F-info", "Tuoli", "Sohva"],
    "Koneet ja toimistotarvikkeet": ["Jimms tehokone", "Jimms pelikone", "jimms yleisnäyttö", "Jimms pelinäyttö", "Medialäppäri", "PROVO Matto - Hiirimatto", "PROVO KUMU PRO - 7.1 tilaäänipelikuuloke", "PROVO NOSTE PRO - hiiri", "PROVO KAJO OPTO - Näppäimistö", "Esperanza EG102", "Toimisto näppäimistö", "Toimistohiiri", "Taittojalka"],
    "TV": ["info-tv", "Kuluttaja-tv", "TV virtakaapeli ja hdmi kaapeli", "Tv lattiajalat", "TV Trussi-kiinnitys", "Tv pöytäjalat"],
    "Sähkö ja verkko": ["Sähköt 1x16A 230V 3000W", "Sähköt 3x16A 400V 9000W", "Sähköt 3x32A 400V 15000W", "Sähköt Muu", "verkko-1G Base-T", "verkko-10G SR", "verkko-10G LR", "Verkkokaapeli"],
    "Standipaketit ja loossit": ["Standi paketti Custom, ota yhteys yhteistyo@vectorama.fi", "Ständialueen matotus per neliömetri", "Standipaketti 4x4m", "Loossi", "Standipaketti 6x4m", "Standipaketti 6x8m", "Custom standi paketti"],
    "Valot": ["Spottivalot", "Valaistus"],
    "Kodinkoneet": ["Lasiovinen jääkaappi", "Lasi-ikkunallinen arkkupakastin", "Pullonkeräys tynnyrit", "Arkkupakastin", "Jenkkikaappi", "Jääkaappipakastin", "Kiertoilmauuni", "Kylmälaari", "Metallinen jääkaappi/pakastin", "Mikro", "Induktioliesi", "Lisätuote"],
    "Muut": ["Lisätuote", "Taittojalka"]
}

# Funktio tietokannan hakemiseen
def hae_tilaukset():
    conn = sqlite3.connect('tilaukset.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tilaukset")
    tilaukset = c.fetchall()
    conn.close()
    return tilaukset

# Funktio tilausten suodattamiseen kategorioiden ja toimipisteen perusteella
def suodata_tilaukset(kategoriat, toimipiste=None):
    tilaukset = hae_tilaukset()
    suodatetut_tilaukset = []
    kaytetyt_tuotteet = set()
    
    for tilaus in tilaukset:
        tuote = tilaus[2]  # Tuote on sarakkeessa 2
        if toimipiste and tilaus[5] != toimipiste:  # Toimituspiste on sarakkeessa 5
            continue
        
        for kategoria in kategoriat:
            if tuote in tuotekokonaisuudet[kategoria] and tuote not in kaytetyt_tuotteet:
                suodatetut_tilaukset.append(tilaus)
                kaytetyt_tuotteet.add(tuote)
                break
    
    return suodatetut_tilaukset

# Funktio taulukon luomiseen ja PDF-lataukseen vaakatasossa
def nayta_tilaukset_taulukkona(tilaukset, otsikko):
    if tilaukset:
        # Muunna tilaukset DataFrameksi ja poista ID ja Päivämäärä
        df = pd.DataFrame(tilaukset, columns=["ID", "Nimi", "Tuote", "Määrä", "Lisätiedot", "Toimituspiste", "Toimituspäivä", "Päivämäärä"])
        df = df[["Nimi", "Toimituspiste", "Tuote", "Määrä", "Lisätiedot", "Toimituspäivä"]]  # Uusi järjestys, ID ja Päivämäärä pois
        
        # Näytä taulukko Streamlitissä
        st.write(f"### {otsikko}")
        st.dataframe(df, use_container_width=True)
        
        # Ryhmittele toimipisteen mukaan PDF:ää varten
        grouped = df.groupby("Toimituspiste")
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))  # Vaakataso
        elements = []
        styles = getSampleStyleSheet()
        
        # Otsikko PDF:lle
        elements.append(Paragraph(otsikko, styles['Heading1']))
        elements.append(Paragraph(" ", styles['Normal']))  # Tyhjä rivi
        
        for toimipiste, group in grouped:
            # Toimipisteen otsikko
            elements.append(Paragraph(f"Toimituspiste: {toimipiste}", styles['Heading2']))
            
            # Poista Toimituspiste-sarake ryhmän riveiltä ja luo taulukko
            group_data = group.drop(columns=["Toimituspiste"]).values.tolist()
            data = [["Nimi", "Tuote", "Määrä", "Lisätiedot", "Toimituspäivä"]] + group_data
            
            # Määritä sarakkeiden leveydet (yhteensä 750 pistettä vaakatasossa A4:lle)
            col_widths = [100, 200, 50, 200, 200]  # Säädetty sopimaan vaakasivulle ilman ID:tä ja Päivämäärää
            
            # Luo taulukko
            table = Table(data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(table)
            elements.append(Paragraph(" ", styles['Normal']))  # Tyhjä rivi ryhmien välissä
        
        doc.build(elements)
        
        # Tarjoa PDF-lataus
        pdf_data = buffer.getvalue()
        buffer.close()
        st.download_button(
            label="Lataa PDF",
            data=pdf_data,
            file_name=f"{otsikko.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
    else:
        st.write("Ei tilauksia vielä.")

# Päänäkymä filttereillä
def main():
    st.set_page_config(page_title="Tilausten katselu", initial_sidebar_state="collapsed")
    st.title("Tilausten katselu")

    # Toimipisteen syöttökenttä
    toimipiste = st.text_input("Syötä toimipiste (jätä tyhjäksi nähdäksesi kaikki)", "")

    # Monivalinta tuotekategorioille
    kategoriat = list(tuotekokonaisuudet.keys())
    valitut_kategoriat = st.multiselect(
        "Valitse tuotekategoriat",
        options=kategoriat,
        default=kategoriat  # Oletuksena kaikki valittu
    )

    # Esivalmiit filtterivaihtoehdot (Build, Deco, Infra, Game)
    st.write("### Esivalmiit suodattimet")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Build (Kaikki)"):
            valitut_kategoriat = kategoriat
    with col2:
        if st.button("Deco"):
            valitut_kategoriat = ["Standipaketit ja loossit", "Valot", "Muut"]
    with col3:
        if st.button("Infra"):
            valitut_kategoriat = ["TV", "Sähkö ja verkko", "Valot", "Muut"]
    with col4:
        if st.button("Game"):
            valitut_kategoriat = ["Koneet ja toimistotarvikkeet", "Pöydät ja tuolit", "Sähkö ja verkko", "Valot", "Muut"]

    # Päivitä multiselect valinnat esivalmiiden suodattimien perusteella
    if 'valitut_kategoriat' in locals():
        st.session_state['valitut_kategoriat'] = valitut_kategoriat
    else:
        valitut_kategoriat = st.session_state.get('valitut_kategoriat', [])

    # Suodata ja näytä tilaukset
    if valitut_kategoriat:
        tilaukset = suodata_tilaukset(valitut_kategoriat, toimipiste if toimipiste else None)
        otsikko = f"Tilaukset - {', '.join(valitut_kategoriat)}" if valitut_kategoriat else "Kaikki tilaukset"
        nayta_tilaukset_taulukkona(tilaukset, otsikko)
    else:
        st.write("Valitse ainakin yksi kategoria nähdäksesi tilaukset.")

if __name__ == "__main__":
    main()