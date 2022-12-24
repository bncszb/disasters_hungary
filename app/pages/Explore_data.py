import streamlit as st
import plotly.express as px

import pandas as pd
import geopandas as gpd
import sqlite3
import contextily as cx


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
import datetime

if "events" not in st.session_state:
    conn=sqlite3.connect("data/events.db")

    events = pd.read_sql_query("SELECT * FROM events_table", conn)

    events["event_date"]=events["event_date"].str.replace("-","").str.strip()
    events["event_date"]=pd.to_datetime(events["event_date"], format='%Y.%m.%d. %H:%M')
    events["date"]=events["event_date"].dt.date
    events["month"]=events["event_date"].dt.month
    events["weekday"]=events["event_date"].dt.weekday
    events["hour"]=events["event_date"].dt.hour

    events["longitude"]=events["longitude"].astype("float32")
    events["latitude"]=events["latitude"].astype("float32")

    st.session_state.events=events


def create_map():

    events_in_cat=st.session_state.events[(st.session_state.events["longitude"]!=0) & (st.session_state.events["latitude"]!=0) & (st.session_state.events["categoryName"].isin(categories))]
    fig = px.density_mapbox(events_in_cat, lat='latitude', lon='longitude', radius=10, hover_data=["date","categoryName","subCategoryName", "title"],
                            center=dict(lat=47.2, lon=19.5), zoom=6.5,
                            mapbox_style="stamen-terrain", width=1200, height=800)
    return fig

                            
if __name__ == '__main__':
    st.set_page_config(
        layout="wide"
    )

    categories=st.multiselect("Select categories",st.session_state.events.categoryName.unique())

    fig=create_map()
    st.plotly_chart(fig)