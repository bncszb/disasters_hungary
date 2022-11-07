import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl


import pandas as pd
import geopandas as gpd
import sqlite3

import seaborn as sns
sns.set_theme()
import datetime

from functools import partial


STEP=datetime.timedelta(days=100)
WINDOW=datetime.timedelta(days=100)
num_frames=20

def update(car_accidents, it):
    fig.clear()

    first_day_of_period=car_accidents.event_date.min()+it*STEP
    last_day=car_accidents.event_date.max()

    xlim=(car_accidents.longitude.min()-0.5,car_accidents.longitude.max()+0.5)
    ylim=(car_accidents.latitude.min()-0.5,car_accidents.latitude.max()+0.5)

    if first_day_of_period<last_day:

        accident_window=car_accidents[(car_accidents.event_date>first_day_of_period) & (car_accidents.event_date<first_day_of_period+WINDOW)]



        title=f'{datetime.datetime.strftime(first_day_of_period, format="%Y. %m. %d.")} - {datetime.datetime.strftime(first_day_of_period+WINDOW, format="%Y. %m. %d.")}'
        g=sns.scatterplot(accident_window, x="longitude" ,y="latitude", alpha=0.1, color="red")
    
        g.set(xlim=xlim,ylim=ylim, title=title)

if __name__ == '__main__':

    conn=sqlite3.connect("events/database/events.db")

    events = pd.read_sql_query("SELECT * FROM events_table", conn)

    events["event_date"]=events["event_date"].str.replace("-","").str.strip()
    events["event_date"]=pd.to_datetime(events["event_date"], format='%Y.%m.%d. %H:%M')

    events["longitude"]=events["longitude"].astype("float32")
    events["latitude"]=events["latitude"].astype("float32")

    car_accidents=events[(events["longitude"]!=0) & (events["latitude"]!=0) & (events["categoryName"]=="Közlekedési baleset")]

    print(events.event_date.max())

    first_day=car_accidents.event_date.min()
    last_day=car_accidents.event_date.max()

    next_frame=partial(update,car_accidents)
    fig=plt.figure(figsize=(12,8))
    ani = animation.FuncAnimation(fig, next_frame, frames=list(range(num_frames)),interval=500,repeat=True)
    ani.save("accidents.gif")


