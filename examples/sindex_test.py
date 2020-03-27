"""
Using an R-tree spatial index with geopandas
--------------------------------

A simple spatial indexing class is included with geopandas, which allows
for more efficient spatial operations such as searches for nearest neighbors
and intersections between objects in multiple dimensions.

"""


from geopandas import sindex

print('sindex stuff')

# first, let's construct an instance of a SpatialIndex and add a 
# simple bounding box to it
idxs = sindex.SpatialIndex()
idxs.insert(2321, (0.0, 0.0, 1.0, 1.0))

# this box has an id of 2321. It has a bottom-left corner located at (0,0) upper-right corner at (1,1)

# each SpatialIndex has a property called ''interleaved'' that specifies
# how to interpret the boundary box parameters.
# When interleaved == True,the boundaries are interpreted in the order of 
# xmin, ymin, ... kmin, xmax, ymax..., kmax for a k-dimensional index.
# When interleaved == False, the boundaries are interpreted in the order of
# xmin, xmax, ... kmin, kmax.
# By default, interleaved is True.

# the above code has the same effect as:
idxs = sindex.SpatialIndex()
idxs.interleaved = False
idxs.insert(2321, (0.0, 1.0, 0.0, 1.0))

# Now, let's make an index with a couple more boxes
idxs = sindex.SpatialIndex()
idxs.insert(2321, (0.0, 0.0, 1.0, 1.0))
idxs.insert(2343, (20.0, 20.0, 30.0, 30.0))
idxs.insert(4351, (0.0, 0.0, 10.0, 10.0))
idxs.insert(4212, (5.0, 5.0, 7.0, 7.0))

# The geopandas sindex can be used to search for regions in an index whose
# boundaries or interiors intersect with a given box.
hits = list(idxs.intersection((0, 0, 6, 6), objects=True))
# These results can also be queried for certain criteria, such as to find 
# results whose id value falls within a certain range
result = [(item.id, item.bbox) for item in hits if item.id > 4000]
print(result)

# The nearest method searches for the n nearest neighbors to a given region.
# Here, we are searching for the 2 nearest neighbors to the box from (1,1) to (2,2)
n = list(idxs.nearest((1.0, 1.0, 2.0, 2.0), 2, objects = True))
result = [(item.id, item.bbox) for item in n]
print(result)

# For these methods, the parameter ''objects'' specifies the return type of the search.
# When objects == True, a pointer to the bounding box object is returned.
# When objects == False, only the integer-valued ids of the bounding box objects are returned.
# By default, objects == False:

hits = list(idxs.intersection((0, 0, 6, 6)))
hits = [item for item in hits if item > 4000]
print(hits)
n = list(idxs.nearest((1.0, 1.0, 2.0, 2.0), 2))
print(n)

# Now, let's apply the same principles to an sindex generated from a geodataframe
# First, I will just create a small geodataframe with a couple of dummy points

import geopandas as gpd
from shapely.geometry import Point

coors = list()
coors.append(Point(0,0))
coors.append(Point(0,1))
coors.append(Point(1,0))
coors.append(Point(1,1))
coors.append(Point(2,2))
coors.append(Point(4,6))

gdf = gpd.GeoDataFrame({
    'Name': ['Point0','Point1','Point2','Point3','Point4','Point5'],
    'Coordinates': coors
}, geometry = 'Coordinates')

print(gdf)

# Now, we can generate a spatial index for the points in this geodataframe
spatial_index = gdf.sindex

# Now we can do an intersection with a small bounding box stretching from (0,0) to (0,1).
# hits = list(spatial_index.intersection((0, 0, 1, 1), objects=True))
# result = [(item.id, item.bbox) for item in hits]
# print(result)

hits_index = list(spatial_index.intersection((0, 0, 1, 1)))
hits = gdf.iloc[hits_index]
print(hits)

# Evidently, the points included in the result are points 1 through 4 which lie in the box.

n = list(spatial_index.nearest((0, 0, 0, 0), 3))
result = gdf.iloc[n]
print(result)


"""
more sources:

https://geoffboeing.com/2016/10/r-tree-spatial-index-python/

"""



from rtree import index

print('rtree stuff')
idx = index.Index()
# idx.interleaved = False
# xmin, ymin, xmax, ymax... if interleaved True
# xmin, xmax, ymin, ymax... if interleaved False
left, bottom, right, top = (0.0, 0.0, 1.0, 1.0)
idx.insert(0, (left, bottom, right, top))
result = list(idx.intersection((0.0, 1.0, 2.0, 2.0)))
print(result)

"""
https://toblerity.org/rtree/class.html

insert(id, coordinates, obj=None)
Inserts an item into the index with the given coordinates.

Parameters:	
id – long integer A long integer that is the identifier for this index entry. IDs need not be 
unique to be inserted into the index, and it is up to the user to ensure they are unique if 
this is a requirement.
coordinates – sequence or array This may be an object that satisfies the numpy array protocol, 
providing the index’s dimension * 2 coordinate pairs (i.e. xmin, xmax, ymin, ymax ....) representing 
the mink and maxk coordinates in each dimension defining the bounds of the query window.
obj – a pickleable object. If not None, this object will be stored in the index with the id.
The following example inserts an entry into the index with id 4321, and the object it stores 
with that id is the number 42. The coordinate ordering in this instance is the default 
(interleaved=True) ordering:


intersection - Return ids or objects in the index that intersect the given coordinates.

Parameters:	
coordinates – sequence or array This may be an object that satisfies the numpy array protocol, 
providing the index’s dimension * 2 coordinate pairs representing the mink and maxk coordinates 
in each dimension defining the bounds of the query window.
objects – True or False or ‘raw’ If True, the intersection method will return index objects that 
were pickled when they were stored with each index entry, as well as the id and bounds of the 
index entries. If ‘raw’, the objects will be returned without the rtree.index.Item wrapper.
"""
idx = index.Index()
idx.insert(2,(34.3776829412, 26.7375853734, 49.3776829412, 41.7375853734))
# what does objects do?
hits = list(idx.intersection((0, 0, 60, 60), objects=True))
result = [(item.object, item.bbox) for item in hits if item.id == 0]
print(result)


idx.insert(1, (34.0, 26.0, 49.0, 41.0))
idx.insert(2, (33.0, 25.0, 48.0, 40.0))
idx.insert(3, (32.0, 23.0, 47.0, 39.0))
idx.insert(4, (31.0, 22.0, 46.0, 38.0))


idx.insert(5, (1, 2, 3, 4))

# nearest neighbors:
n = list(idx.nearest((31.0, 22.0, 46.0, 38.0), 3))
print(n)