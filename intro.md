# LARS' TRON

## Introduction

After a long night of working on the new  LARS AI, aptly named the LARS TIRED (Totally Into Retro Entertainment Daemon) AI, Professor Peterson notices something strange happening to the internal system.

Digging Peter realizes that there has been an error with the TIRED AI and it has gone rogue! TIRED digitizes the intrusive Professor and brings him to where all bad programs go: THE GAME GRID.

**Your job is to write a program to help the professor beat the malicious programs on the GAME GRID in a game of light cycles!**

# Game
TRON is a game adapted from the [1982 Documentary of the same name](https://en.wikipedia.org/wiki/Tron). In the game, you control one robot riding a *light cycle*, a kind of motorcycle that makes 90-degree turns and leaves an impenetrable *jetwall* behind it. If you crash into a any jetwall, you are out of the game. When a robot leaves the game, their jetwall disappears. The winner is the last robot standing.

# Scoring

Currently, your score is your rank, where higher is better. We are going to change this to reflect both your rank and the number of turns you play.

# Motion

Your light cycle can go `north`, `south`, `east`, or `west`. At the end of every turn, you must set the variable `move` to one of these directions. You can't stay in the same place!

# Sensors

Robot can access two basic types of information: configurable point sensors, and the map array.

## Configurable point sensors

Your robot has nine configurable point sensors (`s0`, `s1`, `s2`, `s3`, `s4`, `s5`, `s6`,`s7`, and `s8`) that tell you what is located at a particular point on the map. In TRON, a space can be one of three values: 

 * `TAKEN` (it has a robot in it), 
 * `WALL` (there is a jetwall there)
 * `EMPTY` (it is empty space).

You can choose where you want the sensor to "look" (relative to your own position) by setting the variables `sNx` and `sNy` (where `N` is the sensor number 0-8). For example, if you set `s1x` to 0 and `s1y` to 0, the sensor `s1` will always have you in it, because your `x + 0` and your `y + 0` is where you are. If you set `s1x` to 0 and `s1y` to -1, the sensor `s1` will tell you what is immediately north of you. By setting the `x` and `y` values accordingly, you can check ever space next to you.

## The Map Array

The variable `map_array` is a *two-dimensional array* containing the entire map. A 2D array is an array of arrays -- here, it is an array of columns (where each column is, itself, an array). 

If that's confusing, don't worry. The important thing is that you can find out what is at any location in the map by accessing the array as `map_array[x][y]`, where `x` is the x-value and `y` is the y-value. Unlike you have learned in math class, in computer graphics it is common for coordinates (0,0) to be the upper left corner of the map, and to have numbers increase going down and to the right. In this scheme, the lower-right corner of the map is represented as `map_array[width][height]` (the variables `width` and `height` have the width and height of the map).

Using `for` loops, you can search through the entire map array.

## The Default Program

### Random and the Modulo (Remainder) Operator

Your initial program is programmed in Little Python (LP), a variant of the Python programming language.

The first thing your robot does is generates a random number between 0 and 3 (0, 1, 2 or 3). 

    a = rand % 4

The above code picks one of four numbers using two things -- `rand` and the *modulo* operator `%`. 

The special `rand` variable always returns a random number every time it is read. 

The *modulo* operator can be thought of as "division remainder". So, `4 % 3` is *1*, because `4 / 3` has a remainder of 1. 

If you take a random number from `rand` and apply `% 4` to it, you will end up with a random number between 0 and 3 (try it on a piece of paper to convince yourself!). That random number is saved into the variable `a` using the assignment operation `a = rand % 4`.

### Conditionals: The 'if' Statement

Once your robot has a random number between 0 and 3, it can test that value using the `if` statement and choose to go in one of four directions based on the random number selected.

In an `if` statement, a program asks a question. If the question is **true**, the program executes the code between the curly braces (`{` and `}`). If the question is **false**, nothing happens.

So, the code:

    if x is y {
      z = 3
    }

... will set `z` to 3 *if and only if* the value of `x` equals the value of `y`. **Please note**: the conditional and left bracket (`{`) must be on the first line, followed by the conditional code (here `z = 3`) and finally by the right bracket (`}`) on its own line. 

In addition to `is`, you can test whether something `is not` something else.

Here's the first conditional statement from the default program:


    if a is 0 {
      move = east
    }


This code says "if the variable `a` is equal to *0*, set the variable `move` to *east*." (Remember, `a` was set using `rand` and the modulo (`%`) operator.  

The remaining 3 `if` statements cover west, north and south.

    if a is 1 { 
      move = west 
    } 
    if a is 2 { 
      move = north 
    } 
    if a is 3 { 
      move = south 
    } 

As you may have already guessed, your robot will move in whatever direction the variable `move` is set at the end of your program. Your program will run **300** times, and your score is the number of apples your robot manages to find during that time.

Of course, your current program just walks around randomly. So it's not very good.


## Level 1: Helping Peter Navigate the Grid

Use your l337 skills to help Peter navigate the GRID!
