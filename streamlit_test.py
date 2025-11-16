import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_resource
def get_data():
    conn = st.connection('mysql', type='sql')
    query = """
    SELECT c.name AS genre, COUNT(f.film_id) AS film_count
    FROM category c
    JOIN film_category fc ON c.category_id = fc.category_id
    JOIN film f ON fc.film_id = f.film_id
    GROUP BY c.name
    ORDER BY film_count DESC;
    """
    df = conn.query(query, ttl=600)
    return df

def main():
    st.title("Sakila: Elokuvien määrä genreittäin")
    st.write("Näytetään kuinka monta elokuvaa on per genre")
    data = get_data()
    df = pd.DataFrame(data)
    st.dataframe(df)

    fig = px.bar(df, x="genre", y="film_count", title="Elokuvien määrä per genre", color="genre")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
