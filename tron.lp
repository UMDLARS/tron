# Apple Example Bot
# Name: Example Bot
# You must set move to east, west, south, or north to move in the respective directions.
# Any invalid move will be taken as no move.
# You will be given 8 sensors that you can move around the grid:
# s0-s8
# You will also be given a map object in the form of a 2D array:
# You can use the width and height to iterate through the map array as well
# directly above the robot
#s1x = 0
#s1y = -1

# above and to left
#s2x = -1
#s2y = -1

# above and to right
#s3x = 1
#s3y = -1

# remember sensors s4-s8!

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

# random bot
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
