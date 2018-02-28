# Name: ALAN1
   
# to the north
s1x = 0 
s1y = -1
# to the east
s3x = 1
s3y = 0
# to the south
s5x = 0
s5y = 1
# to the west
s7x = -1
s7y = 0

if (move is 0) {
    a = rand % 4
    if (a is 0) {
        move = north
    }
    if (a is 1) {
    	move = east
    }
    if (a is 2) {
        move = south
    }
    if (a is 3) {
        move = west
    }
}

if (move is east) {
    ahead = s3
}
if (move is south) {
    ahead = s5
}
if (move is west) {
    ahead = s7
}
if (move is north) {
    ahead = s1
}

if (ahead is WALL) {
    
    searching = 1
    
    if (move is east or move is west) {
        if (s1 is OPEN) {
            move = north
        } else {
            move = south
        }
    } else {
    
        if (s3 is OPEN) {
            move = east
        } else {
            move = west
        }
    }
}

