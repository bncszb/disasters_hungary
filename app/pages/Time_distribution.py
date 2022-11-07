import streamlit as st
import  streamlit_toggle as tog

import plotly.express as px

import pandas as pd
import geopandas as gpd
import sqlite3
import contextily as cx

import plotly.figure_factory as ff

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
import datetime
import numpy as np

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


def time_plot(x, subcat=False):
    fig, ax=plt.subplots(1, figsize=(12,8))

    events_in_cat=st.session_state.events[(st.session_state.events["longitude"]!=0) & (st.session_state.events["latitude"]!=0) & (st.session_state.events["categoryName"]==categories)]
    # sns.countplot(events_in_cat,x=x,hue="subCategoryName", ax=ax)
    if subcat:
        events_in_cat["dummy"]=1
        events_in_cat=events_in_cat[events_in_cat["subCategoryName"]!=""]
        events_in_cat=events_in_cat.pivot_table(index=[x], columns=["subCategoryName"], values=['dummy'], aggfunc="count")
        events_in_cat=events_in_cat.fillna(0)
        events_in_cat.columns=events_in_cat.columns.droplevel()
        # events_in_cat=events_in_cat.rename_axis([None], axis=1)
        print(len(events_in_cat.columns[0]))
        events_in_cat.plot(kind="bar",stacked=True,ax=ax)

    else:
        sns.countplot(events_in_cat, hue="categoryName",x=x, ax=ax)
    
    return fig
            
if __name__ == '__main__':
    st.set_page_config(
        layout="wide"
    )

    categories=st.selectbox("Select categories",st.session_state.events.categoryName.unique())

    subcats=tog.st_toggle_switch(label="Visualize subcategories", 
                    default_value=False, 
                    label_after = False, 
                    inactive_color = '#D3D3D3', 
                    active_color="#11567f", 
                    track_color="#29B5E8"
                    )
    st.write(st.session_state.events.head())

    col1, col2, col3 = st.columns([1,1,1])

    if categories:
        with col1:
            fig=time_plot("month",subcats )
            st.pyplot(fig)

        with col2:
            fig=time_plot("weekday",subcats)
            st.pyplot(fig)

        with col3:
            fig=time_plot("hour",subcats)
            st.pyplot(fig)