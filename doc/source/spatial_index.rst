Using an R-tree spatial index with geopandas
--------------------------------------------

A spatial indexing class is included with geopandas, which allows for
more efficient spatial operations such as searches for nearest neighbors
and intersections between objects in multiple dimensions. This is a
simple wrapper class for the spatial index implemented in rtree which
allows it to be used with geodataframes.

First, let’s construct an instance of sindex and add a simple bounding
box to it.

.. code:: ipython3

    from geopandas import sindex
    
    idx = sindex.SpatialIndex()
    idx.insert(2321, (0.0, 0.0, 1.0, 1.0))

This box has an id of 2321. It has a bottom-left corner located at (0,0)
upper-right corner at (1,1)

Each SpatialIndex has a property called ‘’interleaved’’ that specifies
how to interpret the boundary box parameters. When interleaved ==
True,the boundaries are interpreted in the order of xmin, ymin, … kmin,
xmax, ymax…, kmax for a k-dimensional index. When interleaved == False,
the boundaries are interpreted in the order of xmin, xmax, … kmin, kmax.
By default, interleaved is True.

.. code:: ipython3

    # this creates an identical box to the code in the previous cell:
    
    # idx = sindex.SpatialIndex()
    # idx.interleaved = False
    # idx.insert(2321, (0.0, 1.0, 0.0, 1.0))

Let’s add a few more boxes to the index.

.. code:: ipython3

    idx.insert(2343, (20.0, 20.0, 30.0, 30.0))
    idx.insert(4351, (0.0, 0.0, 10.0, 10.0))
    idx.insert(4212, (5.0, 5.0, 7.0, 7.0))

Intersections
-------------

The geopandas sindex can be used to search for regions in an index whose
boundaries or interiors intersect with a given box.

.. code:: ipython3

    intersect = list(idx.intersection((0, 0, 6, 6), objects=True))
    result = [(item.id, item.bbox) for item in intersect]
    result




.. parsed-literal::

    [(2321, [0.0, 0.0, 1.0, 1.0]),
     (4351, [0.0, 0.0, 10.0, 10.0]),
     (4212, [5.0, 5.0, 7.0, 7.0])]



Nearest neighbor search
-----------------------

The sindex can also be used to search for the nearest neighbors to a
given region. Here, we are searching for the 2 nearest neighbors to the
box from (1,1) to (2,2).

.. code:: ipython3

    near = list(idx.nearest((1.0, 1.0, 2.0, 2.0), 2, objects = True))
    result = [(item.id, item.bbox) for item in near]
    result




.. parsed-literal::

    [(2321, [0.0, 0.0, 1.0, 1.0]), (4351, [0.0, 0.0, 10.0, 10.0])]



For these methods, the parameter ‘’objects’’ specifies the return type
of the search. When objects == True, a pointer to the bounding box
object is returned. When objects == False, only the integer-valued ids
of the bounding box objects are returned. By default, objects == False.

.. code:: ipython3

    intersect = list(idx.intersection((0, 0, 6, 6)))
    intersect




.. parsed-literal::

    [2321, 4351, 4212]



.. code:: ipython3

    near = list(idx.nearest((1.0, 1.0, 2.0, 2.0), 2))
    near




.. parsed-literal::

    [2321, 4351]



Integration with geodataframes
------------------------------

We can apply the same principles to an sindex generated from a
geodataframe. For demonstration purposes, let’s create a small
geodataframe with a couple of dummy points.

.. code:: ipython3

    import geopandas as gpd
    from shapely.geometry import Point

.. code:: ipython3

    coors = list()
    coors.append(Point(0,0))
    coors.append(Point(0,1))
    coors.append(Point(1,0))
    coors.append(Point(1,1))
    coors.append(Point(2,2))
    coors.append(Point(4,6))
    
    gdf = gpd.GeoDataFrame({
        'Coordinates': coors
    }, geometry = 'Coordinates')
    
    gdf




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Coordinates</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>0</td>
          <td>POINT (0.00000 0.00000)</td>
        </tr>
        <tr>
          <td>1</td>
          <td>POINT (0.00000 1.00000)</td>
        </tr>
        <tr>
          <td>2</td>
          <td>POINT (1.00000 0.00000)</td>
        </tr>
        <tr>
          <td>3</td>
          <td>POINT (1.00000 1.00000)</td>
        </tr>
        <tr>
          <td>4</td>
          <td>POINT (2.00000 2.00000)</td>
        </tr>
        <tr>
          <td>5</td>
          <td>POINT (4.00000 6.00000)</td>
        </tr>
      </tbody>
    </table>
    </div>



Now, we can generate a spatial index for the points in this geodataframe
and use it to perform the same intersection and nearest-neighbor
searches.

.. code:: ipython3

    spatial_index = gdf.sindex

.. code:: ipython3

    # intersection
    
    intersect = list(spatial_index.intersection((0, 0, 1, 1)))
    result = gdf.iloc[intersect]
    result




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Coordinates</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>0</td>
          <td>POINT (0.00000 0.00000)</td>
        </tr>
        <tr>
          <td>1</td>
          <td>POINT (0.00000 1.00000)</td>
        </tr>
        <tr>
          <td>2</td>
          <td>POINT (1.00000 0.00000)</td>
        </tr>
        <tr>
          <td>3</td>
          <td>POINT (1.00000 1.00000)</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    # nearest neighbors
    
    near = list(spatial_index.nearest((0, 0, 0, 0), 3))
    result = gdf.iloc[near]
    result




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Coordinates</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>0</td>
          <td>POINT (0.00000 0.00000)</td>
        </tr>
        <tr>
          <td>2</td>
          <td>POINT (1.00000 0.00000)</td>
        </tr>
        <tr>
          <td>1</td>
          <td>POINT (0.00000 1.00000)</td>
        </tr>
      </tbody>
    </table>
    </div>


