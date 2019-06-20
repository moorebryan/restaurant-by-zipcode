#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:18:53 2019

@author: Bryan
"""

from flask import Flask, render_template, request, redirect
import bokeh
import pandas as pd
import json
# import os
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import inferno
from bokeh.io import show, output_notebook
from bokeh.embed import components
# import math

app = Flask(__name__)


def loadData():
    """
    Load
    """
    # import os
    import urllib.request
    json_data = 'https://raw.githubusercontent.com/hvo/' + \
                'datasets/master/nyc_restaurants_by_cuisine.json'
    with urllib.request.urlopen(json_data) as url:
        data = json.loads(url.read().decode())
        restaurants_df = pd.io.json.json_normalize(data)
    return restaurants_df

data = loadData()
list_of_zips=[int(item.split('.')[1]) for item in list(data.columns)[1:-1]]

def showViz(data, zip_code):
    """
    data=pandas data frame for resturant
    zip_code=zip code where resturants are located
    """
    
    data = data.fillna('')
    column_name='perZip'+'.'+str(zip_code)
    #print(column_name)
    cuisine=data['cuisine'].tolist()
    counts=list(data[column_name].values)
    # Needed for using bokeh
    source = ColumnDataSource(data=dict(cuisine=cuisine, count=counts))

    p = figure(x_range=cuisine,plot_height=1000, plot_width=1000,toolbar_location=None, title="Resturant counts by cusine")

    renderers = p.vbar(x='cuisine', top='count', width=0.9, source=source,
                       line_color='white', fill_color=factor_cmap('cuisine', palette=inferno(len(cuisine)), factors=cuisine))

    p.xgrid.grid_line_color = None
#     p.xaxis.major_label_orientation = math.pi/4
    p.xaxis.major_label_text_font_size = "8pt"
    p.xaxis.major_label_orientation = "vertical"

    # Implement interactivity
    my_hover = HoverTool()
    my_hover.tooltips = [('Cuisine','@cuisine'),('Number of Locations','@count')]
    p.add_tools(my_hover)
    return p

@app.route('/')
def visualize():
    '''
    Returns a flask visualization by filtering the data by zip-code
    '''
    # Method=POST is never triggered
    # Method=GET gives server error if zip code call below is commented out, meaning it is called every time
    #first determine the selected zip code
    zip_code = request.args.get("zip_code")
    if zip_code == None:
       zip_code=11238
        
       #create the plot
    plot=showViz(data,zip_code)
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("cuisine_index1.html", script=script, div=div,list_of_zips=list_of_zips,zip_code=zip_code)

if __name__ == '__main__':
	app.run(port=33507, debug=True)