# LARS' TRON

## Introduction

After a long night of working on the new  LARS AI, aptly named the LARS TIRED (Totally Into Retro Entertainment Daemon) AI, Professor Peterson notices something strange happening to the internal system.

Digging Peter realizes that there has been an error with the TIRED AI and it has gone rogue! TIRED digitizes the intrusive Professor and brings him to where all bad programs go: THE GAME GRID.

**Your job is to write a program to help the professor destroy the malicious programs on the GAME GRID and survive!**

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