import streamlit as st
import pandas as pd
import plotly.express as px
from database import db_setup
import plotly





st.title("Dashboard")

raw_data = db_setup.GET_week_sales()


#st.dataframe(raw_data)

fig = px.bar(raw_data, 
             x='Item', 
             y='Count', 
             title="Items Ordered by Week",
             #labels={"week": "Week", "quantity": "Quantity Ordered"},
             barmode="stack")

st.plotly_chart(fig)



df = db_setup.GET_week_hour_day_sales()

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

