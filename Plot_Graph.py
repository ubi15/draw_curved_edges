import networkx as nx
import numpy as np
import matplotlib as matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys, os




'''
Image settings:
'''

'''
    - s_min and s_max set the range of nodes size depending on their final
        degree if VaryNodesSize is True;
    - min_ew max_ew set the minimum and maximum width of the represented edges
        if VaryEdgesSize is True;
'''

VaryNodesSize = True
s_min = 4.
s_max = 10.

VaryEdgesSize = True
min_ew = 2
max_ew = 10

'''
    min_d sets the minimum distance of an edge from the circle and
        IT MUST FALLS IN THE (.1, max_d) interval

    max_d sets the maximum distance of an edge from the center of the circle and
        IT MUST FALLS IN THE (min_d, .95) interval
'''
min_d = .15
max_d = .825

FigFileName = 'My_Graph.pdf'  # Where to save the figure and its extension...

##################################################
##################################################

Sources = []
Targets = []
Weights = []

IFile = sys.argv[1]
if not os.path.exists(IFile):
    print 'Please provide an existing file!'
    print 'Usage:'
    print 'python2 Plot_Graph.py ../path/to/edge_lists_file.dat'
    sys.exit()

if not os.path.isfile(IFile):
    print 'Please provide a regular file!'
    print 'Usage:'
    print 'python2 Plot_Graph.py ../path/to/edge_lists_file.dat'
    sys.exit()

try:
    f = open(IFile, 'r')
except:
    print 'Error opening %s file in reading mode!' % IFile

for i, l in enumerate(f):
    v = l.strip().split()
    if len(v) < 2:
        print 'Error reading input file at line %d' % i
        print 'Only %d values found while 3 are requested!' % len(v)
        f.close()
        sys.exit()

    Sources.append(v[0])
    Targets.append(v[1])
    Weights.append(float(v[2]))
f.close()

G = nx.Graph()
for s,t,weight in zip(Sources, Targets, Weights):
    G.add_edges_from([(s,t)], w=weight)

degrees = [G.degree(n) for n in G.nodes()]
k_max = max(degrees)

# Pos is a dictionary containing the positions of the nodes...
Pos = nx.circular_layout(G)


ew = [G[e[0]][e[1]]['w'] for e in G.edges()]
w_min = min(ew)
w_max = max(ew)
ec = [plt.cm.Blues(.5 + .45*(float(W)/w_max)) for W in ew]

ns = [s_min*(1 + s_max*k/k_max) for k in degrees]
nc = [plt.cm.Oranges(.75) if k == k_max-1 else plt.cm.Blues(.6)\
      for k in degrees]

nx.draw(G, edge_color=ec, width=ew, node_color=nc, node_size=ns,pos=Pos)
plt.gcf().set_size_inches(9,9)


step = 1e-3
center = [.5,.5]
radius = .5

def circle(r, c, theta):
    return np.array([np.cos(theta)*r+c[0], np.sin(theta)*r+c[1]])

radi = np.arange(0,2.*np.pi,step)
Coord = np.array([circle(radius, center, th) for th in radi])
xc = Coord[:,0]
yc = Coord[:,1]


def distanza(p1,p2):
    return np.sqrt(((p1-p2)**2.).sum())

def medio(p1,p2):
    return (p1+p2)/2.

def Vertex(p1,p2,c):
    m = medio(p1,p2)
    direttrice = c-m
    return m+direttrice*(min_d+max_d*(1.-distanza(m,c)/distanza(c,p1)))

def gimme_angle(p,c):
    r = distanza(p,c)
    [dx,dy] = p-c

    if dx == .0:
        if dy > .0:
            return np.pi/2.
        else:
            return np.pi*3./2.
    elif dx>.0:
        if dy>=.0:
            return np.arctan(dy/dx)
        else:
            return 2.*np.pi+np.arctan(dy/dx)
    elif dx<.0:
        return np.pi+np.arctan(dy/dx)



# the center and radius of the circle...
centro = np.array([.5,.5])
raggio = .5

# minimum (second minimum) distances...
min_ds = sorted([distanza(Pos[G.nodes()[-1]],Pos[n])\
        for n in G.nodes()[:-1]])[1]

def xy_edge(i,j,c,r):
    i=np.array(i)
    j=np.array(j)
    c=np.array(c)

    m = medio(i,j)
    if distanza(m,c)<1e-6:
        x = np.linspace(i[0],j[0],10)
        y = np.linspace(i[1],j[1],10)
        return x,y
    elif distanza(i,j)<min_ds:
        ti = gimme_angle(i,c)
        tj = gimme_angle(j,c)
        if max(ti,tj)-min(ti,tj) > np.pi:
            radi = np.linspace(max(ti,tj)-2.*np.pi,min(ti,tj))
        else:
            radi = np.linspace(min(ti,tj),max(ti,tj))

        return r*np.cos(radi)+c[0],r*np.sin(radi)+c[1]

    Vertice = Vertex(i,j,c)

    a = distanza(Vertice, m)/((distanza(i,j)/2.)**2.)

    yp = np.linspace(-distanza(i,j)/2., distanza(i,j)/2.,100)
    xp = a*(yp**2.)
    xp += distanza(c,Vertice)

    theta_m = gimme_angle(medio(i,j),c)
    xpr = np.cos(theta_m)*xp - np.sin(theta_m)*yp
    ypr = np.sin(theta_m)*xp + np.cos(theta_m)*yp

    xpr += c[0]
    ypr += c[1]

    return xpr,ypr


# Plotting!
plt.figure(figsize=(12,12))

edge_weight = lambda w: (w-w_min)/w_max*(max_ew-min_ew) + min_ew
for e in G.edges():
    x,y=xy_edge(Pos[e[0]],Pos[e[1]],centro,raggio)
    plt.plot(x,y,'-',c=plt.cm.Blues(.9),\
            lw=edge_weight(G[e[0]][e[1]]['w']) if VaryEdgesSize else min_ew,\
            alpha=.7)

for i, n in enumerate(G.nodes()):
    plt.plot(Pos[n][0],Pos[n][1],'o', c=plt.cm.Blues(.6),\
            ms=ns[i] if VaryNodesSize else 15)

plt.xlim(-.1,1.1)
plt.ylim(-.1,1.1)
plt.axis('off')
plt.tight_layout()
plt.savefig(FigFileName, bbox_inches='tight')
print 'Figure saved in %s' % FigFileName

