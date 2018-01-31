# Apple Example Bot
# Name: Example Bot
# You must set move to east, west, south, or north to move in the respective directions.
# Any invalid move will be taken as no move.
# You will be given 8 sensors that you can move around the grid:
# s0-s8
# directly in front of robot
#s1x = 0
#s1y = -1

# ahead and to left
#s2x = -1
#s2y = -1

# ahead and to right
#s3x = 1
#s3y = -1

# remember sensors s4-s8!

#The return values of these sensors correspond with the values shown below:
#   TAKEN = 8912
#    OPEN = 12312
#    WALL = 323423

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
