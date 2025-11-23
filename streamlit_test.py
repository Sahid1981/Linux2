import os

import streamlit as st

import pandas as pd

import plotly.express as px

from streamlit_autorefresh import st_autorefresh

from cron import uunimakkara



def get_sakila_data():

    conn = st.connection('sakila', type='sql')

    query = "SELECT c.name AS genre, COUNT(f.film_id) AS film_count FROM category c JOIN film_category fc ON c.category_id = fc.category_id JOIN film f ON fc.film_id = f.film_id GROUP BY c.name ORDER BY film_count DESC;"

    df = conn.query(query, ttl=600)

    return df



def get_weather_data():

    conn = st.connection('weather', type='sql')

    df = conn.query("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50",ttl=600)

    return df

def main():

    st.title("Tietokannat, Sää , Uunimakkaravahti")

    count = st_autorefresh(interval=60000, limit=None, key="data_refresh")



    st.write(f"Sivu on päivittynyt {count} kertaa latauksen jälkeen.")



    tab1, tab2, tab3 = st.tabs(["🎬 Sakila Genretilastot", "🌤 Säädata Oulun Herukassa", "🌭 Uunimakkaravahti"])



    with tab1:

        st.write("Elokuvien määrä genrettäin")

        sakila_df = get_sakila_data()

        st.dataframe(sakila_df)

        fig = px.bar(sakila_df, x="genre", y="film_count", title="Elokuvien määrä per genre", color="genre")

        st.plotly_chart(fig, use_container_width=True)



    with tab2:

        st.subheader("Viimeisin säädata")

        weather_df = get_weather_data()

        st.line_chart(weather_df.set_index('timestamp')['temperature'])

        st.dataframe(weather_df)




    with tab3:

        # Alusta äänen tila session stateen (oletuksena mykistetty)
        if 'audio_muted' not in st.session_state:
            st.session_state.audio_muted = True

        # Otsikko ja mykistysnappi samalle riville
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Tarkista uunimakkarat")
        with col2:
            # Mykistysnappi
            mute_icon = "🔇" if st.session_state.audio_muted else "🔊"
            if st.button(mute_icon, key="mute_button", help="Klikkaa soittaaksesi/pois soittamasta ääntä"):
                st.session_state.audio_muted = not st.session_state.audio_muted
                st.rerun()

        # Näytä äänisoitin jos ääni on päällä
        if not st.session_state.audio_muted:
            audio_file = "OodiUunimakkaralle.mp3"
            if os.path.exists(audio_file):
                st.audio(audio_file, autoplay=True, loop=True)
            else:
                st.warning(f"Äänitiedostoa '{audio_file}' ei löytynyt. Lisää se projektikansioon.")

        city = st.text_input("Kaupunki (esim. oulu)", value="oulu").strip().lower()

        if st.button("Hae tämän päivän uunimakkarat"):

            with st.spinner("Haetaan tietoja..."):

                places = uunimakkara.find_places(city)

            st.success(f"Löytyi {len(places)} paikkaa.")

            for name, url in places:

                st.markdown(f"- **{name}** – [Linkki]({url})")



        if st.button("Hae koko viikon uunimakkarat"):

            with st.spinner("Haetaan viikon tiedot..."):

                week_results = uunimakkara.find_week_places(city)

            st.success(f"Löytyi {len(week_results)} paikkaa, joissa uunimakkaraa tällä viikolla.")

            if week_results:

                for name, url, days_found in week_results:

                    days_str = ", ".join(days_found)

                    st.markdown(f"- **{name}** – [Linkki]({url}) ({days_str})")

            else:

                st.info("Ei löytynyt paikkoja, joissa olisi uunimakkaraa tällä viikolla.")

if __name__ == "__main__":

    main()

