#!/usr/bin/env python3
"""
A tiny, tongue‑in‑cheek Snake game.

Run:
    python3 snake.py

The snake moves with the arrow keys. When it crashes into a wall or itself,
a friendly hiss is printed and the game ends.
"""

import curses, random, sys, time

WIDTH=40
HEIGHT=20
SNAKE_CHAR="🐍"
FOOD_CHAR="🍎"
# Base delays (seconds)
V_DELAY=0.1  # vertical movement delay
H_DELAY=0.05 # faster horizontal movement

def draw_border(win):
    for x in range(WIDTH+2):
        win.addch(0,x,"#")
        win.addch(HEIGHT+1,x,"#")
    for y in range(1,HEIGHT+1):
        win.addch(y,0,"#")
        win.addch(y,WIDTH+1,"#")

def place_food(snake):
    while True:
        pos=(random.randint(1,HEIGHT),random.randint(1,WIDTH))
        if pos not in snake:
            return pos

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    # initial timeout based on vertical delay
    stdscr.timeout(int(V_DELAY*1000))
    snake=[(HEIGHT//2,WIDTH//2-1),(HEIGHT//2,WIDTH//2),(HEIGHT//2,WIDTH//2+1)]
    direction=(0,1)
    food=place_food(snake)
    while True:
        try: key=stdscr.getkey()
        except curses.error: key=None
        if key in ("KEY_UP","w"): direction=(-1,0)
        elif key in ("KEY_DOWN","s"): direction=(1,0)
        elif key in ("KEY_LEFT","a"): direction=(0,-1)
        elif key in ("KEY_RIGHT","d"): direction=(0,1)
        elif key in ("q","Q"): break
        # Adjust timeout: faster when moving horizontally
        dy,dx=direction
        if dx!=0: stdscr.timeout(int(H_DELAY*1000))
        else: stdscr.timeout(int(V_DELAY*1000))
        hy,hx=snake[-1]
        nh=(hy+dy,hx+dx)
        if nh[0]<1 or nh[0]>HEIGHT or nh[1]<1 or nh[1]>WIDTH or nh in snake:
            stdscr.addstr(HEIGHT//2,WIDTH//2-5,"HISS! ☠️")
            stdscr.refresh(); time.sleep(1.5); break
        snake.append(nh)
        if nh==food:
            food=place_food(snake)
        else:
            snake.pop(0)
        stdscr.clear()
        draw_border(stdscr)
        fy,fx=food
        stdscr.addstr(fy,fx,FOOD_CHAR)
        for y,x in snake[:-1]: stdscr.addstr(y,x,"·")
        hy,hx=snake[-1]
        stdscr.addstr(hy,hx,SNAKE_CHAR)
        stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.addstr(HEIGHT+3,0,"Game over. Press any key to exit...")
    stdscr.getkey()

if __name__=="__main__":
    try: curses.wrapper(main)
    except KeyboardInterrupt: sys.exit(0)
