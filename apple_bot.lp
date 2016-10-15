# Apple Example Bot
# You must set move to east, west, south, or north to move in the respective directions.
# Any invalid move will be taken as no move.
# LEVEL 1: Two variables you have access to are x_dir and y_dir to the nearest apple
# x_dir will be set to 0, east, or west
# y_dir will be set to 0, north, or south
# LEVEL 2: Advanced: check for pit traps with is_pit_east, is_pit_west, is_pit_south or is_pit_north!

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
