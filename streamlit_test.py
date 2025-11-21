import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

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
    st.title("Tietokannat")
    count = st_autorefresh(interval=60000, limit=None, key="data_refresh")
    st.write(f"Sivu päivittyy 10 minuutin välein.")
    st.write(f"Sivu on päivittynyt {count} kertaa latauksen jälkeen.")
    
    tab1, tab2 = st.tabs(["🎬 Sakila Genretilastot", "🌤 Säädata Oulun Herukassa"])

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
if __name__ == "__main__":
    main()
