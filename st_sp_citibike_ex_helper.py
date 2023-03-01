#!/usr/bin/env python
# Author: Vinod Shiv
# Date: 2022-06-23

# Snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col, lit

# Misc
import pandas as pd

# Streamlit
import streamlit as st

# Plotly
import plotly.express as px

# helper for showcode
import helper

#st.experimental_memo(ttl=600)

st.set_page_config(
    page_title="Citibike",
    page_icon="🚴‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://developers.snowflake.com',
        'About': "This is an *extremely* cool app powered by Snowpark for Python, Streamlit, and Snowflake Data Marketplace"
    }
)


# Create Session object
def create_session_object():
    session = Session.builder.configs(
        st.secrets["snowflake"]).create()
    return session



if __name__ == "__main__":
    # Declare variables required
    


    TABS = '\t' * 8

    ########### Create a session to Snowflake ############
    # Create a session object
    
    session = create_session_object()

    # context header
    session.sql("use role analyst_citibike;").collect()
    session.sql("use schema citibike.demo;").collect()
    session.sql("use warehouse bi_medium_wh;").collect()

    # Add header and a subheader
    st.header("Citibike - Snowflake ❄️ ")
    st.markdown("###### Powered by Snowpark for Python  | Made with Streamlit ")
    st.markdown("---")

    st.write("Steps taken")
    st.write("1. Connect to Snowflake via Snowpark for Python  \n 2. Load data into local Pandas dataframes  \n 3. Render Plotly Charts for Analytics")
    st.markdown("---")

    ########### Collect Data from Queries into DFs ###########
    with st.spinner(f'Collecting data from Snowflake..'):
        # Use columns to display the three dataframes side-by-side along with their headers
        col1, col2 = st.columns(2)
        with col1:
                with helper.echoExpander():
                    # Trips over time from trips_vw
                    tot_sql = """SELECT DATE_TRUNC('DAY', STARTTIME) START_DAY,\
                            COUNT(*) AS NUM_TRIPS \
                            FROM TRIPS_VW GROUP BY 1 ORDER BY 1;"""

                    tot_df = session.sql(tot_sql).to_pandas() 
                    st.markdown('\n#### Trips over Time')
                    fig = px.area(tot_df, x="START_DAY", y="NUM_TRIPS")
                    st.plotly_chart(fig)


            
        with col2:
            with helper.echoExpander():
                hod_sql = """SELECT HOUR(STARTTIME) HOUR_OF_DAY,\
                        IFNULL(START_BOROUGH, 'NOT IN NY') BOROUGH,\
                        COUNT(*) NUM_TRIPS\
                        FROM DEMO.TRIPS_STATIONS_WEATHER_VW GROUP BY 1, 2;"""

                hod_df = session.sql(hod_sql).to_pandas() 
                st.markdown('\n#### Hour of Day')
                fig = px.bar(hod_df, x="HOUR_OF_DAY", y="NUM_TRIPS",color="BOROUGH")
                st.plotly_chart(fig)
        
        st.markdown('---')

        ### Donut charts for rentals by type 
        with helper.echoExpander():
            st.markdown('\n#### Bike Rentals by Member and Bike Type')
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go
            from plotly.offline import plot

            classic_df = session.sql("""SELECT \
                            MEMBER_TYPE,COUNT(TRIPID) AS NUM_TRIPS \
                            FROM DEMO.TRIPS_STATIONS_WEATHER_VW \
                            WHERE BIKE_TYPE = 'classic' \
                            GROUP BY 1;""").to_pandas()
            
            ebike_df = session.sql("""SELECT \
                            MEMBER_TYPE,COUNT(TRIPID) AS NUM_TRIPS \
                            FROM DEMO.TRIPS_STATIONS_WEATHER_VW \
                            WHERE BIKE_TYPE = 'ebike' \
                            GROUP BY 1;""").to_pandas()

            fig = make_subplots(rows=1, cols=2, 
            specs=[[{"type": "domain"}, {"type": "domain"}]],
            subplot_titles=['Classic Bike', 'eBike'])


            fig.add_trace(go.Pie(
                values=classic_df['NUM_TRIPS'],
                labels=classic_df['MEMBER_TYPE'],
                scalegroup='one',
                name="Classic Rentals"),
                row=1, col=1)

            fig.add_trace(go.Pie(
                values=ebike_df['NUM_TRIPS'],
                labels=ebike_df['MEMBER_TYPE'],
                scalegroup='one',
                name="eBike Rentals"),
                row=1, col=2)

            # Use `hole` to create a donut-like pie chart
            fig.update_traces(hole=.3, hoverinfo="label+value+name")

            st.plotly_chart(fig, use_container_width=True)
            st.markdown('---')
        
        st.snow()
