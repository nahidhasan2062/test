#%%
import pandas as pd
#import pip install pygwalker as pyg
import numpy as np
import plotly.express as px
import pymysql
import streamlit as st
#%%
# Set page configuration
#st.set_page_config(
    #page_title="PyGWalker Demo",
    #page_icon=":snake:",
    #layout="wide",
    #initial_sidebar_state="expanded",
#)
#%%
def main():
    password_placeholder = st.empty()

    password = password_placeholder.text_input("Enter Password:", type="password")

    if password == "1234":
        
        st.success("Password is correct. Access granted!")
        # Clear the password field
        password_placeholder.empty()
        # Put the content of your app here
        st.write("Welcome to the protected Streamlit app!")
        # %%
        st.title("Greenville River View Ltd")
        st.write("Greenville City Financial Statement")

        # %%
        conn = pymysql.connect(host='103.138.150.6',
                                port=int(3306),
                                user='greenvil_greenville',
                                # username='ds_reports',
                                passwd='Pqsn%~i3]CxD'
                                )
        # %%
        # Create two columns for input
        col1, col2 = st.columns(2)

        # Get the input dates from the user
        with col1:
            from_date = st.date_input("From:", value=None)

        with col2:
            to_date = st.date_input("To:", value=None)
            
            
        # %%
        #from_date = '2023-11-01'
        #to_date = '2023-11-30' 
        #%%
        query1 = f"""
            select c.client_id as Client_ID,
                c.sector_id as Sector,
                c.p_plot as Plot,
                c.p_block as Block,
                c.p_size as Katha,
                c.p_price_p_k as Per_katha_price,
                sum(c.p_size*c.p_price_p_k) as Total_Amount,
                c.p_total_p as Total_Price,
                sum(c.p_size*20000) as booking_Money,
                #sum(b.credit_amount) as Totol_Credit_amount,
                c.mp_type as Sales_Type,
                c.status as Sales_Status,
                c.sales_person as Sales_person,
                date(c.created) as Created_Date,
                c.app_name as Customer_Name,
                c.c_personal as phone_Number,
                c.profetion as Profession,
                c.p_ps as Customer_Area,
                c.p_dist as Distirct
            from greenvil_test.wg_tbl_client c
            where date(c.created) >= '{from_date}'
            AND date(c.created) <= '{to_date}'
            group by Client_ID
            ;

            """

            #df = pd.read_sql_query(query1, conn)
        Cat = pd.read_sql_query(query1.format(
            from_date=from_date, to_date=to_date), conn)

                                   
        # %%
        #st.write('All Customer List With Details')
        #st.dataframe(Cat) 
        # %%
        st.sidebar.header("Please_Filter_Here")

        #  %%
        sales_Officer = st.sidebar.multiselect(
            "Select the Sales_Officer Name:",
            options=Cat["Sales_person"].unique(),
            default=Cat["Sales_person"].unique()
        )
        #%%
        orderSts = st.sidebar.multiselect(
            "Select the Order Status:",
            options=Cat["Sales_Status"].unique(),
            default=Cat["Sales_Status"].unique()
        )

        # %%
        df_selection = Cat.query(
            "Sales_person == @sales_Officer  & Sales_Status==@orderSts" 
        )
                # Check if the dataframe is empty:
        if df_selection.empty:
            st.warning("No data available based on the current filter settings!")
            st.stop() # This will halt the app from further execution.

        ##%
        st.write('Booking and Installment/Onetime Money Overall_Data')
        st.dataframe(df_selection)

        # TOP KPI's
        #%%
        # Step 1: Convert Size to numeric and remove invalid entries
        df_selection["Katha"] = pd.to_numeric(df_selection["Katha"], errors='coerce')  # invalid string → NaN

        # Step 2: Replace NaN with 0 or drop them (optional)
        df_selection = df_selection.dropna(subset=["Katha"])  # or use fillna(0) if you want to treat them as 0

        # Step 3: Then safely do the sum
        Total_Sold_Katha = int(df_selection["Katha"].sum())
        #Total_Sold_Katha = int(df_selection["Size"].count())
        # %%
        CIN_Count =  int(df_selection["Client_ID"].nunique())
        # %%
        left_column,  right_column = st.columns(2)

        with right_column:
            st.subheader("CIN_Count:")
            st.subheader(f"{CIN_Count:}")
            st.markdown("""---""")
        with left_column:
            st.subheader("Total_Sold_Katha:")
            st.subheader(f"{Total_Sold_Katha:}")
            st.markdown("""---""")
# %%
        sales_by_product_line = (
            df_selection.groupby(by=["Sales_person"])
            .agg({
                'Katha':'sum',
                'booking_Money': 'sum',
                'Total_Price': 'sum',
                'Client_ID': 'nunique'
            }).reset_index()

        )
        # %%
        st.write('Sales person Wise Performance')
        st.dataframe(sales_by_product_line) 

    elif password != "":
        st.error("Incorrect password. Access denied.")

if __name__ == "__main__":
    main()

