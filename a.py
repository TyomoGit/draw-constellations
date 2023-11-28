from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos

from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos, mpc, stellarium
from skyfield.projections import build_stereographic_projection
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN

from matplotlib import pyplot as plt

class PopularConstellationKind:
    Andromeda = 'And'
    Antlia = 'Ant'
    UrsaMajor = 'UMa' # おおぐま座
    Orion = 'Ori'
    Scorpius = 'Sco' # さそり座
    Hydra = 'Hya' # うみへび座


# hipparcos dataset contains star location data
with load.open(hipparcos.URL) as f:
    stars = hipparcos.load_dataframe(f)

# constellation dataset
url = ('https://raw.githubusercontent.com/Stellarium/stellarium/master/skycultures/modern_st/constellationship.fab')

with load.open(url) as f:
    constellations = stellarium.parse_constellations(f)

constellationName = PopularConstellationKind.Orion

ALL_CONSTELLATION_NAMES = list(map(lambda x: x[0], constellations))

Orion = list(filter(lambda x: x[0] == constellationName, constellations))


def registerGraph(constellationName, ax):
    global constellations
    Orion = list(filter(lambda x: x[0] == constellationName, constellations))

    ax.grid(True)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(f'{constellationName}')

    hipparcosNums = set()

    for line in Orion[0][1]:
        hipparcosNums.add(line[0])
        hipparcosNums.add(line[1])

    global stars
    filteredStars = stars.filter(items=hipparcosNums, axis=0)
    x = filteredStars['ra_degrees']
    y = filteredStars['dec_degrees']

    mag = filteredStars['magnitude'] 
    mag = list(map(lambda x: (6-x)**2, mag))

    ax.scatter(x, y, s=mag)
    ax.invert_xaxis()

    #draw line
    for line in Orion[0][1]:
        star1 = stars.loc[line[0]]
        star2 = stars.loc[line[1]]
        ax.plot([star1['ra_degrees'], star2['ra_degrees']], [star1['dec_degrees'], star2['dec_degrees']], color='black', linewidth=0.5)

fig = plt.figure(figsize=(20, 20))
for name in ALL_CONSTELLATION_NAMES[:36]:
    ax = fig.add_subplot(6, 6, ALL_CONSTELLATION_NAMES.index(name)+1)
    registerGraph(name, ax)
plt.savefig('constellation_1.png')

fig = plt.figure(figsize=(20, 20))
for name in ALL_CONSTELLATION_NAMES[36:72]:
    ax = fig.add_subplot(6, 6, ALL_CONSTELLATION_NAMES.index(name)-35)
    registerGraph(name, ax)
plt.savefig('constellation_2.png')

fig = plt.figure(figsize=(20, 20))
for name in ALL_CONSTELLATION_NAMES[72:]:
    ax = fig.add_subplot(6, 6, ALL_CONSTELLATION_NAMES.index(name)-71)
    registerGraph(name, ax)
plt.savefig('constellation_3.png')

plt.show()