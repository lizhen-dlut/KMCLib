""" Module for holding common coordinate manipulating utility functions. """


# Copyright (c)  2012  Mikael Leetmaa
#
# This file is part of the KMCLib project distributed under the terms of the
# GNU General Public License version 3, see <http://www.gnu.org/licenses/>.
#


import numpy


def centerCoordinates(coordinates, index):
    """
    Center the coordinates around the given index.

    :param coordinates: The coordinates of the system.

    :param index: The index of the center to use as origin.
    :type index: int

    :returns: The coordinates centered at the specified index.
    """
    # Extract the centeral coordinate.
    center = coordinates[index]
    # Subtract.
    coordinates = numpy.array([ coord - center for coord in coordinates ])

    # Done.
    return coordinates


def sortCoordinates(coordinates, center, types1, types2=None):
    """
    Sort the coordinates with respect to distance form the provided center index and type.

    :param coordinates: The coordinates to sort.

    :param center: The index of the center to calculate distances from.
    :type center: int

    :param types1: The first list of site types to co-sort with the coordinates.
    :type types1:  a list of strings

    :param types2: The second, optional, list of site types to co-sort with the coordinates.
    :type types2:  a list of strings

    :returns: The sorted coordinates and sorted types.
    """
    if types2 is None:
        types2 = [ t for t in types1 ]

    # Get the types.
    dt = coordinates.dtype
    dtype = [('x',dt),('y',dt),('z',dt),('d',dt),('type1', numpy.array(types1).dtype),('type2', numpy.array(types2).dtype)]

    # Calculate the distance form the center.
    origin = coordinates[center]
    distances = numpy.array([ numpy.linalg.norm(coord) for coord in coordinates ])

    # Setup the data to sort.
    to_sort = numpy.array([ (c[0],c[1],c[2],d,t1,t2) for (c,d,t1,t2) in zip(coordinates,distances,types1, types2)],
                          dtype=dtype)

    # Sort.
    sorted_list = numpy.sort(to_sort, order=['d','type1','x','y','z'])

    # Extract the info.
    coordinates = numpy.array([[c[0],c[1],c[2]] for c in sorted_list])
    distances   = numpy.array([c[3] for c in sorted_list])
    types1      = [c[4] for c in sorted_list]
    types2      = [c[5] for c in sorted_list]

    # Done.
    return (coordinates, distances, types1, types2)

