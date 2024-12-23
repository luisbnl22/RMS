import streamlit as st
import pandas as pd
import plotly.express as px
from database import db_setup
import plotly
import utils as utils

st.set_page_config(layout='wide')

ui =    utils.AccessManagement()
db = db_setup.Database()
DataInteraction = db_setup.DataInteraction()


st.title("Dashboard")

raw_data = DataInteraction.GET_week_sales()



#st.dataframe(raw_data)

fig = px.bar(raw_data, 
             x='Order Time', 
             y='Count', 
             color='Item',
             title="Meals per day",
             #labels={"week": "Week", "quantity": "Quantity Ordered"},
             barmode="stack")



#MEALS SHARE

data = DataInteraction.GET_week_meals_share()

fig2 = px.line(data, 
             x='Order Time', 
             y='Share', 
             color='Item',
             title="Meals Share")
             #labels={"week": "Week", "quantity": "Quantity Ordered"},)


data_sales_hour = DataInteraction.GET_week_meals_share()

fig2 = px.line(data, 
             x='Order Time', 
             y='Share', 
             color='Item',
             title="Meals Share")
             #labels={"week": "Week", "quantity": "Quantity Ordered"},)





col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig2)


st.markdown("<hr>", unsafe_allow_html=True)

col3, col4 = st.columns(2)



with col3:
    b = st.date_input('Date to visualize hour meals')

    try:
        hourly_sales = DataInteraction.GET_hourly_sales(b)


        fig3 = px.line(hourly_sales, 
                    x='Hour', 
                    y='Count', 
                    title="Meals per hour")

        st.plotly_chart(fig3)
    except:
        st.write("No data for specific date")
    #st.pyplot(create_chart())

with col4:
    c = st.date_input('Date to visualize earnings (€)')

    #try:
    earnings_category = DataInteraction.GET_earnins_day(c)


    fig5 = px.pie(earnings_category, values='Gross Margin', names='Item',  title="Earnings per Item")

    st.plotly_chart(fig5)

st.markdown("<hr>", unsafe_allow_html=True)

col5, col6 = st.columns(2)

#MEALS SHARE

data_earnings = DataInteraction.GET_earnins_meals()

earnings = px.line(data_earnings, 
             x='Date', 
             y='Gross Margin', 
             color='Item',
             title="Earnings per item (€)")
             #labels={"week": "Week", "quantity": "Quantity Ordered"},)


with col5:
    st.plotly_chart(earnings)

with col6:

    # except:
    #     st.write("No data for specific date")
    #st.pyplot(create_chart())



    df = DataInteraction.GET_week_hour_day_sales()

    # Ensure 'Datetime' column is in datetime format
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Extract day of the week and hour of the day
    df['day_of_week'] = df['Datetime'].dt.day_name()  # 'Monday', 'Tuesday', etc.
    df['hour_of_day'] = df['Datetime'].dt.hour        # Hour (0-23)

    # Group by day and hour to count orders
    heatmap_data = df.groupby(['day_of_week', 'hour_of_day']).size().reset_index(name='order_count')

    # Reorder days of the week for display
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data['day_of_week'] = pd.Categorical(heatmap_data['day_of_week'], categories=days_order, ordered=True)

    # Pivot the data to create a matrix for the heatmap
    heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='hour_of_day', values='order_count').fillna(0)

    # Plotly Heatmap
    fig = px.imshow(heatmap_pivot,
                    labels=dict(x="Hour of Day", y="Day of Week", color="Number of Orders"),
                    x=heatmap_pivot.columns,
                    y=heatmap_pivot.index,
                    color_continuous_scale='Viridis')

    # Display the heatmap in Streamlit
    st.plotly_chart(fig)