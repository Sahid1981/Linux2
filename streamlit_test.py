import streamlit as st
import pandas as pd
import plotly.express as px
def main():
	st.title("Sähkön hinta")
	df = pd.read_csv("chart2.csv")
	ff = px.scatter(df, x="category", y="Hinta")
	st.plotly_chart(ff, use_container_width=True)
if __name__ == "__main__":
	main()
