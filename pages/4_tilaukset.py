import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import os

# Tuotekokonaisuudet
tuotekokonaisuudet = {
    "Pöydät ja tuolit": ["Valkoiset muovipöydät", "Ikeapöydät", "Vaneripöydät B", "Vaneripöydät C", "Vaneripöydät D", "Vaneripöydät E", "Vaneripöydät G", "Vaneripöydät H", "Vaneripöydät F-info", "Tuoli", "Sohva", "Säkkituoli, musta"],
    "Koneet ja toimistotarvikkeet": ["Tehokone", "Pelikone", "Yleisnäyttö", "Pelinäyttö", "Medialäppäri", "PROVO Matto - Hiirimatto", "PROVO KUMU PRO - 7.1 tilaäänipelikuuloke", "PROVO NOSTE PRO - hiiri", "PROVO KAJO OPTO - Näppäimistö", "Esperanza EG102", "Toimisto näppäimistö", "Toimistohiiri", "Taittojalka"],
    "TV": ["info-tv", "Kuluttaja-tv", "TV virtakaapeli ja hdmi kaapeli", "Tv lattiajalat", "TV Trussi-kiinnitys", "Tv pöytäjalat"],
    "Sähkö ja verkko": ["Sähköt 1x16A 230V 3000W", "Sähköt 3x16A 400V 9000W", "Sähköt 3x32A 400V 15000W", "Sähköt Muu", "verkko-1G Base-T", "verkko-10G SR", "verkko-10G LR", "Verkkokaapeli"],
    "Standipaketit ja loossit": ["Standi paketti Custom, ota yhteys yhteistyo@vectorama.fi", "Ständialueen matotus per neliömetri", "Standipaketti 4x4m", "Loossi", "Standipaketti 6x4m", "Standipaketti 6x8m"],
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

    if toimipiste:
        toimipiste = toimipiste.lower().strip()
    else:
        toimipiste = None

    for tilaus in tilaukset:
        tila_toimipiste = tilaus[5].lower()
        if toimipiste and toimipiste not in tila_toimipiste:
            continue
        
        tuote = tilaus[2]
        for kategoria in kategoriat:
            if tuote in tuotekokonaisuudet[kategoria]:
                suodatetut_tilaukset.append(tilaus)
                break
    return suodatetut_tilaukset

# Funktio taulukon luomiseen ja PDF-lataukseen vaakatasossa
def nayta_tilaukset_taulukkona(tilaukset, otsikko):
    if tilaukset:
        # Muunna tilaukset DataFrameksi ja poista ID ja Päivämäärä
        df = pd.DataFrame(tilaukset, columns=["ID", "Nimi", "Tuote", "Määrä", "Lisätiedot", "Toimituspiste", "Toimituspäivä", "Päivämäärä"])
        df = df[["Nimi", "Toimituspiste", "Tuote", "Määrä", "Lisätiedot", "Toimituspäivä"]]

        # Ryhmittele toimituspisteittäin
        grouped = df.groupby("Toimituspiste")

        st.write(f"### {otsikko}")


        grouped = df.groupby("Toimituspiste")
        
        for toimipiste, group in grouped:
            tilausten_maara = len(group)

            with st.expander(f"Toimituspiste: {toimipiste} ({tilausten_maara} tilausta)", expanded=False):
                st.dataframe(group, use_container_width=True)

        # PDF:n valmistelu
        grouped = df.groupby("Toimituspiste")
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        elements = []
        styles = getSampleStyleSheet()

        # Otsikko PDF:lle
        elements.append(Paragraph(otsikko, styles['Heading1']))
        elements.append(Paragraph(" ", styles['Normal']))

        # Lisätiedot-sarakkeen rivitystyylit
        custom_style = ParagraphStyle(
            name='Custom',
            fontSize=10,
            leading=12,
            spaceAfter=4,
            wordWrap='CJK',
        )

        for toimipiste, group in grouped:
            elements.append(Paragraph(f"Toimituspiste: {toimipiste}", styles['Heading2']))

            # Muodosta rivit ja rivitä 'Lisätiedot'-kenttä (indeksi 3)
            group_data = []
            for _, row in group.drop(columns=["Toimituspiste"]).iterrows():
                rivi = list(row)
                rivi[3] = Paragraph(str(rivi[3]), custom_style)  # 'Lisätiedot'
                group_data.append(rivi)

            # Taulukon otsikko + data
            data = [["Nimi", "Tuote", "Määrä", "Lisätiedot", "Toimituspäivä"]] + group_data

            # Sarakeleveydet PDF:lle (yhteensä noin 750 pistettä vaakatasossa)
            col_widths = [100, 150, 50, 250, 200]

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
            elements.append(PageBreak())

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
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        if st.button("Kaikki"):
            valitut_kategoriat = valitut_kategoriat
    with col2:
        if st.button("Build"):
            valitut_kategoriat = ["Pöydät ja tuolit", "Muut"]
    with col3:
        if st.button("Deco"):
            valitut_kategoriat = ["Standipaketit ja loossit", "Valot", "Muut"]
    with col4:
        if st.button("Infra"):
            valitut_kategoriat = ["TV", "Sähkö ja verkko", "Valot", "Muut"]
    with col5:
        if st.button("Game"):
            valitut_kategoriat = ["Koneet ja toimistotarvikkeet", "Pöydät ja tuolit", "Valot", "Muut"]
    with col6:
        if st.button("Sähkö"):
            valitut_kategoriat = ["Sähkö ja verkko"]
    with col7:
        if st.button("Verkko"):
            valitut_kategoriat = ["Sähkö ja verkko"]

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