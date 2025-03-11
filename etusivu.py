import streamlit as st

st.set_page_config(
    page_title="Etusivu",
)

st.title("Vector infrashop kauppa")

st.markdown(
    """
    Tältä sivustolta löydät kaikki tilattavat tuotteet, kuten esim. pöydät, 
    tuolit, TV:t, yms.

    Kun lisäätte useita kappaleita samasta tuotteesta valikkoon, niin tarkastakaa
    että valikkoon on tullut oikea määrä kyseisiä tuotteita. Tällä hetkellä sivusto
    päivittää jokaisen valinnan pienellä viiveellä, joten nopeasti klikkaamalla 
    sivu saattaa valita vain ensimmäisen lisäyksen, jättäen loput huomioimatta.
    """
)

