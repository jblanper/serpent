'''
SERPENT
Ascii version of game 'Snake'

Copyright (C) 2016  Jose Blanco Perales

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import os, time, random
if os.name == 'nt':
    import unicurse as curses
else:
    import curses

def conf_screen(screen):
    '''configure curses.'''
    
    curses.noecho() # don't output keys on screen
    curses.cbreak() # don't wait to key press
    screen.keypad(1) # can use some special values, like KEY_RIGHT
    screen.nodelay(1) # If yes is 1, getch() will be non-blocking.
    curses.curs_set(0)  # hide cursor
    #screen.border() # set border

def end_screen(screen):
    '''set default conf of terminal and end curses.'''
    
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    os.system('cls')

# greetings screen
def set_initial_screen(block):
    '''INTRO screen.'''
    
    title = [
'                                   ',
'  ####  #   #   ###   #   #  ##### ',
' #      ##  #  #   #  #  #   #     ',
'  ###   # # #  #####  ###    ####  ',
'     #  #  ##  #   #  #  #   #     ',
' ####   #   #  #   #  #   #  ##### ',
'                                   '
    ]
    message = 'Press "b" to begin playing.'

    while True:
        g_screen = curses.newwin(23, 45, 1, 1)
        g_screen.border(block, block, block, block, block, block, block, block)
        for i, v in enumerate(title):
            g_screen.addstr(7 + i, 5, v, curses.A_REVERSE)
        g_screen.addstr(15, 9, message)
        
        key = g_screen.getch()
        if key == ord('b'):
            break

# game over screen
def set_game_over_screen(block):
    '''GAME OVER screen.'''
    
    while True:
        pause_screen = curses.newwin(7, 22, 7, 12)
        pause_screen.border(block, block, block, block, block, block, block, block)
        pause_screen.addstr(2, 6, 'GAME OVER', curses.A_REVERSE)
        pause_screen.addstr(4, 3, 'Type "q" to exit')
        pause_screen.refresh()
        
        key = pause_screen.getch()
        if key == ord('q'):
            break

def move(head_coord, body_coord, grow_count):
    '''Return the coordinates of the head and the body for the movement.'''
    
    dir_dic = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)}
    dir, h_coord = head_coord
    new_head_coord = [a + b for (a, b) in zip(h_coord, dir_dic[dir])]
    
    # append the cold coordinates to the body coordinates list and pop first coordinate.
    body_coord.append(h_coord)
    # check if body is growing after having eaten
    if grow_count:
        grow_count -= 1
    elif not grow_count:
        body_coord.pop(0)
    
    return [dir, new_head_coord], body_coord, grow_count

def check_hit(head_coord, fruit_char, body_char, window):
    '''Check if the sneaks head hit something.'''
    
    dir, (y, x) = head_coord
    height, width = window.getmaxyx()
    init_y, init_x = window.getbegyx()
    
    if window.inch(y, x) == ord(fruit_char) + curses.color_pair(2) + curses.A_BLINK:
        return 'fruit'
    if window.inch(y, x) == ord(body_char) + curses.color_pair(1):
        return 'collision'
    if y == height - 1 or y == init_y -1 or x == width - 1 or x == init_x - 1:
        return 'collision'

def set_fruit_coord(window):
    '''Return random coordinates for the fruit.'''
    
    height, width = window.getmaxyx()
    init_y, init_x = window.getbegyx()
    
    # Check if random coordinate already has something
    while True:
        y = random.randint(init_y, height - 2)
        x = random.randint(init_x, width - 2)
        if window.inch(y, x) == ord(' '):
            break
    
    return (y, x)

def main():
    #initiate screen
    os.system("mode con cols=47 lines=25")
    screen = curses.initscr()
    curses.start_color()
    conf_screen(screen)
    
    # color pairs
    block = curses.ACS_BLOCK
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    
    # Variables
    score = 0
    hit = ''
    
    head_char = '.'
    head_coord = ['e', (12, 20)]
    body_char = ':'
    body_coord = [(head_coord[1][0], head_coord[1][1] + n) for n in range(-15, 0)]
    grow_count = 0
    fruit_char = '`'
    fruit_coord = ()
    
    set_initial_screen(block)
    
    while True:
        # print window and score board
        game_screen = curses.newwin(23, 45, 1, 1)
        game_screen.border(block, block, block, block, block, block, block, block)
        game_screen.addstr(22, 3, ' Score: ' + str(score) + ' ')
        
        # check keys
        key = screen.getch()
        if key == ord('q') or hit == 'collision':
            break
        if key == curses.KEY_RIGHT and head_coord[0] != 'w':
            head_coord[0] = 'e'
        if key == curses.KEY_LEFT and head_coord[0] != 'e':
            head_coord[0] = 'w'
        if key == curses.KEY_UP and head_coord[0] != 's':
            head_coord[0] = 'n'
        if key == curses.KEY_DOWN and head_coord[0] != 'n':
            head_coord[0] = 's'
        
        # print snake
        head_coord, body_coord, grow_count = move(head_coord, body_coord, grow_count)
        game_screen.addstr(head_coord[1][0], head_coord[1][1], head_char, curses.color_pair(1) + curses.A_BLINK)
        for (y, x) in body_coord:
            game_screen.addstr(y, x, body_char, curses.color_pair(1))
        
        # print fruit
        if not fruit_coord:
            fruit_coord = set_fruit_coord(game_screen)
        game_screen.addstr(fruit_coord[0], fruit_coord[1], fruit_char, curses.color_pair(2) + curses.A_BLINK)
        
        # refresch window, check hit and check if fruit
        game_screen.refresh()
        hit = check_hit(head_coord, fruit_char, body_char, game_screen)
        if hit == 'fruit':
            score += 1
            fruit_coord = ()
            grow_count += 6
        
        time.sleep(0.09)
    
    set_game_over_screen(block)
    end_screen(screen)

main()
