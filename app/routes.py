from app import app
from app.forms import LoginForm, AddressForm
from config import directory
from flask import (Flask, render_template,
    redirect, url_for, request, flash)
from dependencies import (
    GeoTIFF, get_lambert)
from random import randint
import plotly.graph_objects as go

@app.route("/", methods=["GET","POST"])
@app.route("/signup", methods=["GET","POST"])
def signup():
    version = randint(0,1000000) 
    login = LoginForm()
    address = AddressForm()
    if address.validate_on_submit():
        x,y = get_lambert(address.address.data)
        size = int(address.window.data)
        tif = GeoTIFF.get_tif_from_point(x,y).crop_location(x,y,size,size)
        if address.projection.data == "2D": tif.png()
        else:
            xaxis = go.XAxis(range=[0.2,1], showgrid=False, zeroline=False, visible=False)
            yaxis = go.YAxis(range=[0.2,1], showgrid=False, zeroline=False, visible=False)
            layout = go.Layout(
                xaxis = xaxis,
                yaxis = yaxis,
                paper_bgcolor='rgba(0,0,0,0)',
                scene_aspectmode='manual',
                scene_aspectratio=dict(x=1.5, y=1.5, z=0.5),
                margin=dict(l=0, r=0, b=0, t=0))
            fig = go.Figure(data=[go.Surface(z=tif.arr)], layout=layout)
            fig.write_image(directory +"/app/static/plot.png")

    return render_template("geoloc.html", version=version,
            form={"login":login,"address":address})

@app.route("/index", methods=["GET","POST"])
def index():
    return render_template("index.html", title="Home")
