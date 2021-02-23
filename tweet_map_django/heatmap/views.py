from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
import folium
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import tweepy

def generate_map(search_hash):
    m = folium.Map(location=[39.304232, -100.590900], zoom_start=4)
    df = pd.DataFrame(list(Tweet.objects.all().values()))
    if not df.empty:
        if(search_hash == None):
            coordinate_array = df[['latitude', 'longitude']].values
            m.add_child(plugins.HeatMap(coordinate_array, radius=15))
        else:
            df = pd.DataFrame(list(Tweet.objects.filter(hashtags__contains=[search_hash]).values()))
            if(not df.empty):
                coordinate_array = df[['latitude', 'longitude']].values
                m.add_child(plugins.HeatMap(coordinate_array, radius=15))
    m.save('heatmap/templates/heatmap/map.html')

    m_html = m._repr_html_()
    file1 = open("heatmap/templates/heatmap/map.html","w") 
    file1.write(m_html)
    file1.close() 
    return m_html

def home(request):
    m_html = generate_map(None)
    context = {"map": m_html}
    return render(request, "heatmap/home.html", context)

def search(request):
    search_hashtag = request.POST["hashtag"]
    m_html = generate_map(search_hashtag)
    context = {"map": m_html}
    return render(request, "heatmap/home.html", context)

def about(request):
    return render(request, "heatmap/about.html")