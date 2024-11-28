import streamlit as st
from database import db_setup

st.title("Table Management")

df = db_setup.GET_orders_df()
#st.dataframe(df,width=1200,hide_index=1)

#st.dataframe(db_setup.GET_orders)



# Placeholder for actions
st.write("Select a row to mark as finished:")

# Create a container for row interactions
for index, row in df.iterrows():
    col1, col2 = st.columns([3, 1])  # Columns for layout
    with col1:
        st.write(f"Row {index + 1}: {row['Item']} - Quantity: {row['Quantity']} - Status: {row['Status']}")
    with col2:
        if st.button(f"Mark Row {index + 1} as Finished", key=f"finish_{index}"):
            # Update the row's status and finished quantity
            df.at[index, "Finished Quantity"] = df.at[index, "Quantity"]
            df.at[index, "Status"] = "Finished"
            st.success(f"Row {index + 1} marked as finished!")
            st.experimental_rerun()  # Rerun to refresh the table

# Display updated DataFrame
st.write("Updated Data:")
st.dataframe(df)