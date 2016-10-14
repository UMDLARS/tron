# Apple Example Bot
# Two variables you have access to are x_dir and y_dir to the nearest apple
# x_dir will be set to 0, east, or west
# y_dir will be set to 0, north, or south
# You must set move to east, west, south, or north to move in the respective directions.
# Any invalid move will be taken as no move.

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
