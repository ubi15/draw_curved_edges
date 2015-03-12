## Draw a network with curved edges

A simple and not (yet) flexible script to plot a network in a circular layout 
and with curved edges using matplotlib and networkx.

The link are interpolated as parabolic curves passing from the source node to 
the target one and with their vertex on a specifically computed node on the 
axis of the connecting line.

Some features are tunable as the possibility to change (or not) the nodes and 
edges size.

Usage is straightforward: just install python2, numpy, matplotlib and networkx 
and prepare a file with the following syntax (with no header lines):

SourceID   TargetID   EdgeWeight

and you're ready to go!


A little sample of what *draw_curved_edges* can do when reading the  
file *edgelist.dat* in the Examples folder is the following

![](https://github.com/ubi15/draw_curved_edges/blob/master/My_Graph.jpg 
'Cool image of a cool network')


There is still a lot to do so as to make this script more powerful and 
flexible, specifically:

- set colors and sizes of nodes and edges in the initial settings;
- set the keyword used to compute both the nodes and edges size;
- adapt the calculation of the edge shape to a generic layout fo the nodes;
- comment more and better the piece of code;
- etc. (end of thinking capacity);
