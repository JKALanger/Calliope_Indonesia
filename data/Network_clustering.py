# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:45:17 2022

@author: sup-jkalanger
"""

import pypsa
import re
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
from pypsa.networkclustering import get_clustering_from_busmap, busmap_by_kmeans
import os
import csv
# import geopandas as gpd

os.chdir('C:\\Users\\sup-jkalanger\\Downloads')

network = pypsa.Network()

nodes = pd.read_csv('nodes_unique_500kV.csv',delimiter=',')
edges = pd.read_csv('grid_lines_500kV.csv',delimiter=';')

n_buses = len(nodes)
n_edges = len(edges)

for i in range(n_buses):
    network.add("Bus", int(nodes.iloc[i][0]), x=nodes.iloc[i][1], y=nodes.iloc[i][2], sub_network=nodes.iloc[i][3])
    
for j in range(n_edges):
    c_th_line = 1786 # thermal capacity of 500 kV transmission line, from Floris' thesis
    # if edges.iloc[j][1] == 150:
    #     c_th_line = 401.4 # thermal capacity of 150 kV transmission line, from Floris' thesis
    # elif edges.iloc[j][1] == 275:
    #     c_th_line = 895.9 # thermal capacity of 275 kV transmission line, interpolated from 150 and 500 kV values in Floris' report
    network.add("Line", int(edges.iloc[j][0]), bus0=int(edges.iloc[j][4]), bus1=int(edges.iloc[j][5]), s_nom=c_th_line)
    

groups = network.buses.sub_network
busmap = groups.where(groups != "", network.buses.index)

C = get_clustering_from_busmap(network, busmap)

nc = C.network

edges_nc = nc.lines
nodes_nc = nc.buses

edges_nc.to_csv('clustered_grid_lines_500kV.csv', index=False)
nodes_nc.to_csv('clustered_nodes_500kV.csv', index=False)

fig, (ax, ax1) = plt.subplots(
    1, 2, subplot_kw={"projection": ccrs.EqualEarth()}, figsize=(12, 12)
)
plot_kwrgs = dict(bus_sizes=1e-3, line_widths=0.5)
network.plot(ax=ax, title="original", **plot_kwrgs)
nc.plot(ax=ax1, title="clustered by operator", **plot_kwrgs)
fig.tight_layout()

plt.savefig('Figure_500kV',dpi=300)



# weighting = pd.Series(1, network.buses.index)
# busmap2 = busmap_by_kmeans(network, bus_weightings=weighting, n_clusters=50)

# C2 = get_clustering_from_busmap(network, busmap2)
# nc2 = C2.network

# fig, (ax, ax1) = plt.subplots(
#     1, 2, subplot_kw={"projection": ccrs.EqualEarth()}, figsize=(12, 12)
# )
# plot_kwrgs = dict(bus_sizes=1e-3, line_widths=0.5)
# network.plot(ax=ax, title="original", **plot_kwrgs)
# nc2.plot(ax=ax1, title="clustered by kmeans", **plot_kwrgs)
# fig.tight_layout()

