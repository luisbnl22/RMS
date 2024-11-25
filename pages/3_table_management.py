import streamlit as st
from database import db_setup

st.title("Table Management")

df = db_setup.GET_orders_df()
st.dataframe(df,width=1200,hide_index=1)

#st.dataframe(db_setup.GET_orders)


