import csv
from math import pi, sin, cos, asin, isnan
import sys

from mlpack import emst
import numpy as np
from astropy import units as u
import networkx as nx
# import

DATAPATH = '~/bigdata/I_239/hip_main.dat'


def astrometric_to_cartesian(right_ascension, declination, parallax):
    """Puts a triple of astrometric coordinates into cartesian coordinates.

    right_ascension in degrees
    declination in degrees
    parallax in milliarcseconds

    coordinates x, y, z given in lightyears.
    """

    # Distance in lightyears (converting from milliarcseconds)
    parallax_arcseconds = float(parallax) / 1000 * u.arcsec
    r = parallax_arcseconds.to(u.lyr, equivalencies=u.parallax()).value

    if np.isinf(r) or np.isnan(r):
        raise ValueError("Parallax value error")

    # Spherical coordinate phi in radians (using the physics convention)
    phi = 2 * pi * right_ascension / 360
    assert 0 <= phi <= 2 * pi

    # Spherical coordinate theta in radians
    theta = pi / 2 - 2 * pi * declination / 360

    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    if np.isnan(x) or np.isnan(y) or np.isnan(z):
        raise ValueError("Not a number", x, y, z, r, theta, phi)

    return x, y, z


# Include (0,0,0) initially for our sun.

fieldnames = [
    "Catalog", "HIP", "Proxy", "RAhms", "DEdms", "Vmag", "VarFlag", "r_Vmag",
    "RAdeg", "DEdeg", "AstroRef", "Plx", "pmRA", "pmDE", "e_RAdeg", "e_DEdeg",
    "e_Plx ", "e_pmRA", "e_pmDE", "DE:RA", "Plx:RA", "Plx:DE", "pmRA:RA",
    "pmRA:DE", "pmRA:Plx", "pmDE:RA", "pmDE:DE", "pmDE:Plx", "pmDE:pmRA",
    "F1", "F2", "---", "BTmag", "e_BTmag", "VTmag", "e_VTmag", "m_BTmag",
    "B-V", "e_B-V", "r_B-V", "V-I", "e_V-I", "r_V-I", "CombMag", "Hpmag",
    "e_Hpmag", "Hpscat", "o_Hpmag", "m_Hpmag", "Hpmax", "HPmin", "Period",
    "HvarType", "moreVar", "morePhoto", "CCDM", "n_CCDM", "Nsys", "Ncomp",
    "MultFlag", "Source", "Qual", "m_HIP", "theta", "rho", "e_rho", "dHp",
    "e_dHp", "Survey", "Chart", "Notes", "HD", "BD", "CoD", "CPD", "(V-I)red",
    "SpType", "r_SpType"
]

# Read the data file and compile the stars into a list of data points
all_star_data = []
with open(DATAPATH, newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter='|')
    for row in reader:
        # Only insert stars with nonzero parallax measurements
        if row["Plx"] != '       ' and float(row["Plx"]) > 0:
            all_star_data.append(row)

# Construct an array of coordinates for the stars
star_coords = []

for row in all_star_data:
    cartesian = astrometric_to_cartesian(float(row["RAdeg"]),
                                         float(row["DEdeg"]),
                                         float(row["Plx"]))

    star_coords.append(cartesian)


star_coords = np.array(star_coords)

# Sort the stars by distance
indexlist = np.argsort(np.linalg.norm(star_coords, axis=1))
sortedStars = star_coords[indexlist]

star_index_names = {}

# Print the distances of the 10 nearest stars
print("The ten nearest stars are:")
for i in indexlist[:10]:
    distance = np.linalg.norm(star_coords[i])
    RAhms = all_star_data[i]["RAhms"]
    DEdms = all_star_data[i]["DEdms"]
    hip = all_star_data[i]["HIP"].strip(" ")

    print(f"A star at distance {distance}, at right ascension {RAhms} and declination {DEdms}: HIP Number {hip}")


# Add the sun before running the minimum spanning tree
star_coords = np.concatenate((star_coords, [[0.0, 0.0, 0.0]]))

sun_index = star_coords.shape[0] - 1

print("Computing MST")
spanning_tree = emst(input=star_coords, leaf_size=1, naive=False)

print("Creating Networkx Graph")
mst = nx.Graph()
mst.add_weighted_edges_from([(int(n0), int(n1), dist) for n0, n1, dist in spanning_tree["output"]])

nx.relabel_nodes(mst, {
    sun_index: "Sun",
    68224: "Proxima Centauri",
    68973: "Alpha Centauri B",
    68976: "Alpha Centauri A",
    84553: "Barnard\'s Star",
    52041: "Lalande 21185",
    31195: "Sirius",
    88787: "Ross 154",
    15997: "Epsilon Eridani",
    109580: "Lacaille 9352",
    55410: "Ross 128",
}, copy=False)


# Iteratively remove the longest edge and take the connected component of Sun
# Start with edges under length
mst.remove_edges_from([edge for edge in mst.edges if mst.edges[edge]["weight"] >= 20])
while True:

    # Get the connected component of the sun
    component = mst.subgraph(nx.node_connected_component(mst, "Sun"))
    # How many stars
    size = len(component)
    # Get the maximum distance in the graph
    max_dist = max([component.edges[edge]["weight"] for edge in component.edges])

    print(f"Drawing MST {max_dist}, {size} stars")
    A = nx.nx_agraph.to_agraph(component)
    A.graph_attr['label'] = f'MST of {size} local stars, maximum distance {max_dist}'
    A.draw(f'img/mst_with_{size}_stars.png', format='png', prog='dot')

    # Remove the longest edge
    mst.remove_edges_from([edge for edge in component.edges if component.edges[edge]["weight"] >= max_dist])
