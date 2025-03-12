import streamlit as st

st.markdown(
    """
    Pöydät ja tuolit: 
    | Nimi | Pituus | Leveys | Korkeus | Lisätieto |
    |-------|------|---------|------|----|
    |Valkoiset muovipöydät | | | | |
    |Ikeapöydät | | | | Tilaa tarvittaessa |
    |Vaneripöydät B | | | | |
    |Vaneripöydät C | | | | |
    |Vaneripöydät D | | | | |
    |Vaneripöydät E | | | | |
    |Vaneripöydät G | | | | |
    |Vaneripöydät H | | | | |
    |Vaneripöydät F-info | | | | Infolle varattu |
    |Tuoli | | | | |
    |Sohva | | | | |
    
    Koneet ja toimistotarvikkeet:
    | Nimi | Kuvaus |
    |-------|------|
    Tehokone | |
    Pelikone | | 
    Yleisnäyttö  | |
    Pelinäyttö | |
    Medialäppäri | |
    PROVO Matto - Hiirimatto | |
    PROVO KUMU PRO - 7.1 tilaäänipelikuuloke | |
    PROVO NOSTE PRO - hiiri | |
    PROVO KAJO OPTO - Näppäimistö | |
    Esperanza EG102 | |
    Toimisto näppäimistö | |
    Toimistohiiri | |

    TV:
    | Nimi | Pituus | Leveys | Korkeus |
    |-------|------|---------|------|
    info-tv | |
    Kuluttaja-tv | |
    TV virtakaapeli ja hdmi kaapeli | |
    Tv lattiajalat | |
    TV Trussi-kiinnitys | |
    Tv pöytäjalat | |

    Standipaketit ja loossit:
    | Nimi | Pituus | Leveys | Korkeus |
    |-------|------|---------|------|
    Standi paketti Custom, ota yhteys yhteistyo@vectorama.fi
    Ständialueen matotus per neliömetri | |
    Standipaketti 4x4m | |
    Standipaketti 6x4m | |
    Standipaketti 6x8m | |
    Custom standi paketti | |
    Looss | |

    Valot:
    | Nimi | Pituus | Leveys | Korkeus |
    |-------|------|---------|------|
    Spottivalot | |
    Valaistus | |
    
    Kodinkoneet:
    | Nimi | Pituus | Leveys | Korkeus |
    |-------|------|---------|------|
    Lasiovinen jääkaappi | |
    Lasi-ikkunallinen arkkupakastin | |
    Pullonkeräys tynnyri | |
    Arkkupakastin | |
    Jenkkikaappi | |
    Jääkaappipakastin | |
    Kiertoilmauun | |
    Kylmälaari | |
    Metallinen jääkaappi/pakastin | |
    Mikro | |
    Induktioliesi | |
    Lisätuote | |
    
    Muut: 
    | Nimi | Pituus | Leveys | Korkeus |
    |-------|------|---------|------|
    Lisätuote | |
    Taittojalka | |
"""
)

    

standipaketit = {
    "Peruspaketti": ["Info-TV", "Matto", "Pöytä"],
    "Premium-paketti": ["Info-TV", "Matto", "Pöytä", "Tuoli", "Valaistus"]
}

valittu_paketti = st.selectbox("Valitse standipaketti", list(standipaketit.keys()))
st.write("Paketin sisältö:", standipaketit[valittu_paketti])