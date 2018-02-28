# Name: Example Bot
#       ^^^^^^^^^^^--- change the name of your bot!
#
# You must set move to east, west, south, or north to move in the
# respective directions.  Any invalid move will be taken as no move.
#
# SENSORS
#
# You have 8 sensors (s1 through s8) that you can use to query the map
# state at a given point. To tell them "where to look" you must set
# their X and Y value relative to your own position.
#
# The space (0,0) is the upper left corner of the map, so "up" is
# negative and "down" is positive. Right is positive and left is
# negative. The following instructions set s1 to north, s2 to east, s3 to
# south and s4 to west:

# to the north
s1x = 0 
s1y = -1
# to the east
s2x = 1
s2y = 0
# to the south
s3x = 0
s3y = 1
# to the west
s4x = -1
s4y = 0

# remember you can change these and you also have sensors s5-s8!

#The return values of these sensors correspond with the values shown below:
#   TAKEN = 8912
#    OPEN = 12312
#    WALL = 323423

# use the sensors s1-s8 to make decisions. For example, to move up if the area
# directly above you is open, do something like the following (in your program,
# not as a comment):
# s1x = 0
# s1y = -1
# if s1 is OPEN {
#     move = north
# }
#
# ADVANCED: MAP ARRAY
#
# You can use the variable `map` as a 2D array (using the variables
# `height` and `width`) to access the entire map state. For example, you
# can use loops to search regions of the map. Access the 2D map array
# which is between map[0][0] and map[width][height].

# random bot that does not use sensors
a = rand % 4

if a is 0 {
  move = east
}
if a is 1 {
  move = west
}
if a is 2 {
  move = north
}
if a is 3 {
  move = south
}

