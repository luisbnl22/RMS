import streamlit as st
from database import db_setup
from streamlit_js_eval import streamlit_js_eval

st.title("Table Management")

df = db_setup.GET_orders_df('Pending')
#st.dataframe(df,width=1200,hide_index=1)


if df is None:
    st.write("No pending orders")
else:
    ranks = list(df['dense_rank'].unique().tolist())

    # Create a container for row interactions
    for iter_rank in ranks:

        df_iter = df.query(f"dense_rank == {iter_rank}").copy()

        # Check if df_iter is not empty before accessing its columns
        if not df_iter.empty:

            time_parts = df_iter['order_time'].iloc[0].split(":")
            
            # Extract hour, minute, and second
            hour = time_parts[0][-2:]
            minute = time_parts[1]

            # Display the first value of the 'Table' column for the current rank
            st.write(f"# {df_iter['Table'].iloc[0]} | Ordered at {hour}:{minute}")

            #st.dataframe(df_iter)
            for index, row in df_iter.iterrows():

                # Display the filtered DataFrame
                #st.dataframe(df_iter)

                            # Create two columns
                col1, col2 = st.columns([3, 1])  # 3:1 ratio, so col1 takes more space

                # Center text in the first column
                with col1:  
                    st.markdown(f"<h3 style='text-align: left;'>{row['Item']}</h3>", unsafe_allow_html=True)

                # Place button in the second column (right side)
                with col2:
                    if st.button("Click Me",key=f"{df_iter['id'].iloc[0]}-{df_iter['order_time'].iloc[0]}-{index}"):
                        #st.write(f"{df_iter['id'].iloc[index]}")
                        db_setup.POST_finish_order(df_iter['id'].iloc[index])
                        
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
                        

            #st.write(df_iter["Table"])

            # col1, col2 = st.columns([3, 1])  # Columns for layout
            # with col1:
            #     st.write(f"Row {index + 1}: {row['Item']} - Quantity: {row['Quantity']} - Status: {row['Status']}")
            # with col2:
            #     if st.button(f"Mark Row {index + 1} as Finished", key=f"finish_{index}"):
            #         # Update the row's status and finished quantity
            #         df.at[index, "Finished Quantity"] = df.at[index, "Quantity"]
            #         df.at[index, "Status"] = "Finished"
            #         st.success(f"Row {index + 1} marked as finished!")
            #         st.experimental_rerun()  # Rerun to refresh the table

    # Display updated DataFrame
    #st.write("Updated Data:")
    #st.dataframe(df)