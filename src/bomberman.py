from __future__ import print_function
import random
import signal
import sys
import copy
import time
from getchunix import *
import os
from termcolor import colored as clr


class AlarmException(Exception):
    pass


getch = GetchUnix()


def alarmHandler(signum, frame):
    raise AlarmException


def input_to(timeout=1):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    enem1.motion()
    enem2.motion()
    enem3.motion()
    if (board.level == 2 or board.level == 3):
        enem4.motion()
    if (board.level == 3):
        enem5.motion()
    try:
        # enem.motion()
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        pass
        # enem.motion()
        #print("\n Prompt timeout. Continuing...")
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''


w = 68
h = 34
array = [[' ' for x in range(w)] for y in range(h)]


class Walls:
    def display(self):
        for i in range(0, 2):
            for j in range(0, 68):
                array[i][j] = 'X'
        for i in range(32, 34):
            for j in range(0, 68):
                array[i][j] = 'X'
        for i in range(2, 32):
            for j in range(0, 4):
                array[i][j] = 'X'
        for i in range(2, 32):
            for j in range(64, 68):
                array[i][j] = 'X'
        for x in range(1, 8):
            for i in range(1, 8):
                for j in range(4 * x, 4 * x + 2):
                    for k in range(8 * i, 8 * i + 4):
                        array[j][k] = 'X'


class Bricks:
    def display(self):
        for i in range(6, 8):
            for j in range(16, 24):
                array[i][j] = '/'
        for i in range(10, 12):
            for j in range(48, 52):
                array[i][j] = '/'
        for i in range(12, 14):
            for j in range(20, 24):
                array[i][j] = '/'
        for i in range(22, 24):
            for j in range(32, 52):
                array[i][j] = '/'
        for i in range(30, 32):
            for j in range(20, 24):
                array[i][j] = '/'
        for i in range(30, 32):
            for j in range(60, 64):
                array[i][j] = '/'
        for i in range(18, 20):
            for j in range(4, 16):
                array[i][j] = '/'
        for i in range(2, 4):
            for j in range(44, 52):
                array[i][j] = '/'
        for i in range(14, 16):
            for j in range(36, 40):
                array[i][j] = '/'
        for i in range(6, 8):
            for j in range(60, 64):
                array[i][j] = '/'
        for i in range(26, 28):
            for j in range(8, 16):
                array[i][j] = '/'
        for i in range(10, 12):
            for j in range(4, 8):
                array[i][j] = '/'


class Person:
    def __init__(self, h1, w1):
        self.h1 = h1
        self.w1 = w1

    def move_up(self, h1, w1):
        if (array[h1 - 2][w1] != 'X' and array[h1 - 2][w1] !=
                '/' and array[h1 - 2][w1] != 'E' and array[h1 - 2][w1] != '['):
            for i in range(w1, w1 + 4):
                array[h1 - 2][i] = array[h1][i]
                array[h1 - 1][i] = array[h1 + 1][i]
                array[h1][i] = ' '
                array[h1 + 1][i] = ' '
            return 1
        return 0

    def move_down(self, h1, w1):
        if (array[h1 + 2][w1] != 'X' and array[h1 + 2][w1] !=
                '/' and array[h1 + 2][w1] != 'E' and array[h1 + 2][w1] != '['):
            for i in range(w1, w1 + 4):
                array[h1 + 3][i] = array[h1 + 1][i]
                array[h1 + 2][i] = array[h1][i]
                array[h1][i] = ' '
                array[h1 + 1][i] = ' '
            return 1
        return 0

    def move_left(self, h1, w1):
        if (array[h1][w1 - 4] != 'X' and array[h1][w1 - 4] !=
                '/' and array[h1][w1 - 4] != 'E' and array[h1][w1 - 4] != '['):
            for i in range(h1, h1 + 2):
                array[i][w1 - 4] = array[i][w1]
                array[i][w1 - 3] = array[i][w1 + 1]
                array[i][w1 - 2] = array[i][w1 + 2]
                array[i][w1 - 1] = array[i][w1 + 3]
                array[i][w1] = ' '
                array[i][w1 + 1] = ' '
                array[i][w1 + 2] = ' '
                array[i][w1 + 3] = ' '
            return 1
        return 0

    def move_right(self, h1, w1):
        if (array[h1][w1 + 4] != 'X' and array[h1][w1 + 4] !=
                '/' and array[h1][w1 + 4] != 'E' and array[h1][w1 + 4] != '['):
            for i in range(h1, h1 + 2):
                array[i][w1 + 7] = array[i][w1 + 3]
                array[i][w1 + 6] = array[i][w1 + 2]
                array[i][w1 + 5] = array[i][w1 + 1]
                array[i][w1 + 4] = array[i][w1]
                array[i][w1] = ' '
                array[i][w1 + 1] = ' '
                array[i][w1 + 2] = ' '
                array[i][w1 + 3] = ' '
            return 1
        return 0


class Bomberman(Person):
    lives = 3
    score = 0

    def __init__(self, h1, w1):
        Person.__init__(self, h1, w1)

    def display(self):
        for i in range(2, 4):
            for j in range(4, 8):
                array[i][j] = 'B'

    def death(self):
        if (self.h1 == 2 and self.w1 == 4 and array[4][4] == 'E'):
            self.display()
            self.h1 = 2
            self.w1 = 4
        if (array[self.h1 - 2][self.w1] == 'E' or array[self.h1 + 2][self.w1] ==
                'E' or array[self.h1][self.w1 + 4] == 'E' or array[self.h1][self.w1 - 4] == 'E'):
            bman.lives -= 1
            for i in range(self.h1, self.h1 + 2):
                for j in range(self.w1, self.w1 + 4):
                    array[i][j] = 'B'
            for i in range(self.h1, self.h1 + 2):
                for j in range(self.w1, self.w1 + 4):
                    array[i][j] = ' '
            bman.display()
            bman.h1 = 2
            bman.w1 = 4


bman = Bomberman(2, 4)
bman.display()
bricks = Bricks()
bricks.display()
walls = Walls()
walls.display()


class Board:
    level = 1

    def print(self):
        os.system('clear')

        print("                              LEVEL " + str(self.level))
        print("")
        for i in range(34):
            for j in range(68):
                if (array[i][j] == 'E'):
                    print(clr(array[i][j], 'red'), end='')
                elif (array[i][j] == 'B'):
                    print(clr(array[i][j], 'green'), end='')
                else:
                    print(array[i][j], end='')
            print("")
        print("")
        if (bman.lives<0):
        	bman.lives = 0
        print("Score: " +
              str(bman.score) +
              "                                                " +
              "Lives: " +
              str(bman.lives))
        print("")


board = Board()


class Enemy(Person):
    def __init__(self, h1, w1):
        Person.__init__(self, h1, w1)

    def display(self):
        numh1 = self.h1 * 2
        numw1 = self.w1 * 4
        if (array[numh1][numw1] != 'X' and array[numh1][numw1] !=
                '/' and array[numh1][numw1] != 'B' and array[numh1][numw1] != 'E'):
            for i in range(numh1, numh1 + 2):
                for j in range(numw1, numw1 + 4):
                    array[i][j] = 'E'
            self.h1 = numh1
            self.w1 = numw1
            return 1
        return 0

    def motion(self):
        if (array[self.h1 - 2][self.w1] == " " or array[self.h1 + 2][self.w1] ==
                " " or array[self.h1][self.w1 + 4] == " " or array[self.h1][self.w1 - 4] == " "):
            while(1):
                if (array[self.h1][self.w1] == 'B'):
                    break
                num = random.randint(1, 4)
                if (num == 1):
                    if (self.move_up(self.h1, self.w1)):
                        self.h1 -= 2
                        bman.death()
                        board.print()
                        break
                elif (num == 2):
                    if (self.move_down(self.h1, self.w1)):
                        self.h1 += 2
                        bman.death()
                        board.print()
                        break
                elif (num == 3):
                    if (self.move_left(self.h1, self.w1)):
                        self.w1 -= 4
                        bman.death()
                        board.print()
                        break
                elif (num == 4):
                    if (self.move_right(self.h1, self.w1)):
                        self.w1 += 4
                        bman.death()
                        board.print()
                        break


while(1):
    enem1 = Enemy(random.randint(2, 15), random.randint(2, 15))
    if (enem1.display()):
        break
while(1):
    enem2 = Enemy(random.randint(2, 15), random.randint(2, 15))
    if (enem2.display()):
        break
while(1):
    enem3 = Enemy(random.randint(2, 15), random.randint(2, 15))
    if (enem3.display()):
        break


board.print()


# while(1):
#		enem.motion()


class Bomb:
    cnt = 0
    flag = 0
    count = 3

    def display(self):
        array[boh][bow] = '['
        array[boh + 1][bow] = '['
        array[boh][bow + 3] = ']'
        array[boh + 1][bow + 3] = ']'
        for i in range(boh, boh + 2):
            for j in range(bow + 1, bow + 3):
                array[i][j] = bomb.count

    def timer(self):
        while (bomb.count != 0):
            x = input_to()
            if (x):
                bomb.flag = 1
                if (x == 'w'):
                    if (bman.move_up(bman.h1, bman.w1)):
                        bman.h1 -= 2
                    bomb.display()
                elif (x == 's'):
                    if (bman.move_down(bman.h1, bman.w1)):
                        bman.h1 += 2
                    bomb.display()
                elif (x == 'a'):
                    if (bman.move_left(bman.h1, bman.w1)):
                        bman.w1 -= 4
                    bomb.display()
                elif (x == 'd'):
                    if (bman.move_right(bman.h1, bman.w1)):
                        bman.w1 += 4
                    bomb.display()
            board.print()
            bomb.count -= 1
            if (bomb.flag == 1):
                bomb.display()
        bomb.explosion()

    def explosion(self):
        expl = 0
        recr = 0
        if (array[boh][bow] == 'B'):
            expl = 1
            bman.lives -= 1

        for i in range(boh, boh + 2):
            for j in range(bow, bow + 4):
                array[i][j] = 'e'

        if (boh >= 4):
            if (array[boh - 2][bow] != 'X'):
                if (array[boh - 2][bow] == 'E'):
                    bman.score += 100
                if (array[boh - 4][bow] == 'E'):
                    bman.score += 100
                if (array[boh - 2][bow] == '/'):
                    bman.score += 20
                if (array[boh - 4][bow] == '/'):
                    bman.score += 20
                if (array[boh - 2][bow] == 'B'):
                    bman.lives -= 1
                    recr = 1
                if (array[boh - 4][bow] == 'B'):
                    bman.lives -= 1
                    recr = 1
                for i in range(boh - 4, boh):
                    for j in range(bow, bow + 4):
                        if (array[i][j] != 'X'):
                            array[i][j] = 'e'

        if (boh <= 28):
            if (array[boh + 2][bow] != 'X'):
                if (array[boh + 2][bow] == 'E'):
                    bman.score += 100
                if (array[boh + 4][bow] == 'E'):
                    bman.score += 100
                if (array[boh + 2][bow] == '/'):
                    bman.score += 20
                if (array[boh + 4][bow] == '/'):
                    bman.score += 20
                if (array[boh + 2][bow] == 'B'):
                    bman.lives -= 1
                    recr = 1
                if (array[boh + 4][bow] == 'B'):
                    bman.lives -= 1
                    recr = 1
                for i in range(boh + 2, boh + 6):
                    for j in range(bow, bow + 4):
                        if (array[i][j] != 'X'):
                            array[i][j] = 'e'

        if (bow >= 8):
            if (array[boh][bow - 4] != 'X'):
                if (array[boh][bow - 4] == 'E'):
                    bman.score += 100
                if (array[boh][bow - 8] == 'E'):
                    bman.score += 100
                if (array[boh][bow - 4] == '/'):
                    bman.score += 20
                if (array[boh][bow - 8] == '/'):
                    bman.score += 20
                if (array[boh][bow - 4] == 'B'):
                    bman.lives -= 1
                    recr = 1
                if (array[boh][bow - 8] == 'B'):
                    bman.lives -= 1
                    recr = 1
                for i in range(boh, boh + 2):
                    for j in range(bow - 8, bow):
                        if (array[i][j] != 'X'):
                            array[i][j] = 'e'

        if (bow <= 56):
            if (array[boh][bow + 4] != 'X'):
                if (array[boh][bow + 4] == 'E'):
                    bman.score += 100
                if (array[boh][bow + 8] == 'E'):
                    bman.score += 100
                if (array[boh][bow + 4] == '/'):
                    bman.score += 20
                if (array[boh][bow + 8] == '/'):
                    bman.score += 20
                if (array[boh][bow + 4] == 'B'):
                    bman.lives -= 1
                    recr = 1
                if (array[boh][bow + 8] == 'B'):
                    bman.lives -= 1
                    recr = 1
                for i in range(boh, boh + 2):
                    for j in range(bow + 4, bow + 12):
                        if (array[i][j] != 'X'):
                            array[i][j] = 'e'

        board.print()
        time.sleep(0.2)
        bomb.clear()

        if (expl == 1):
            bman.display()
            bman.h1 = 2
            bman.w1 = 4
        if (recr == 1):
            bman.display()
            bman.h1 = 2
            bman.w1 = 4

        fin = 0
        for i in range(2, 32):
            for j in range(4, 64):
                if (array[i][j] == 'E'):
                    fin = 1
                    break
        if (fin != 1):
            if (board.level == 1):
                board.level += 1
                walls = Walls()
                walls.display()
                bricks = Bricks()
                bricks.display()
                for i in range(2, 4):
                    for j in range(28, 36):
                        array[i][j] = '/'
                for i in range(14, 16):
                    for j in range(56, 64):
                        array[i][j] = '/'
                for i in range(bman.h1, bman.h1 + 2):
                    for j in range(bman.w1, bman.w1 + 4):
                        array[i][j] = ' '
                bman.display()
                bman.h1 = 2
                bman.w1 = 4
                while(1):
                    enem1 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem1
                    if (enem1.display()):
                        break
                while(1):
                    enem2 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem2
                    if (enem2.display()):
                        break
                while(1):
                    enem3 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem3
                    if (enem3.display()):
                        break
                while(1):
                    enem4 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem4
                    if (enem4.display()):
                        break

            elif (board.level == 2):
                board.level += 1
                walls = Walls()
                walls.display()
                bricks = Bricks()
                bricks.display()
                for i in range(2, 4):
                    for j in range(28, 36):
                        array[i][j] = '/'
                for i in range(14, 16):
                    for j in range(56, 64):
                        array[i][j] = '/'
                for i in range(18, 20):
                    for j in range(48, 56):
                        array[i][j] = '/'
                for i in range(30, 32):
                    for j in range(36, 48):
                        array[i][j] = '/'
                for i in range(bman.h1, bman.h1 + 2):
                    for j in range(bman.w1, bman.w1 + 4):
                        array[i][j] = ' '
                bman.display()
                bman.h1 = 2
                bman.w1 = 4
                while(1):
                    enem1 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem1
                    if (enem1.display()):
                        break
                while(1):
                    enem2 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem2
                    if (enem2.display()):
                        break
                while(1):
                    enem3 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem3
                    if (enem3.display()):
                        break
                while(1):
                    enem4 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem4
                    if (enem4.display()):
                        break
                while(1):
                    enem5 = Enemy(random.randint(2, 15), random.randint(2, 15))
                    global enem5
                    if (enem5.display()):
                        break

            elif (board.level == 3):
                print("CONGRATULATIONS!!! You win the game.")
                print("Your final score is : " + str(bman.score))
                print("Thanks for Playing :)")
                print("")
                sys.exit()

        board.print()

    def clear(self):
        for i in range(boh - 4, boh + 6):
            for j in range(bow, bow + 4):
                if (i >= 0 and i < 34):
                    if (array[i][j] == 'e'):
                        array[i][j] = ' '
        for i in range(boh, boh + 2):
            for j in range(bow - 8, bow + 12):
                if (j >= 0 and j < 68):
                    if (array[i][j] == 'e'):
                        array[i][j] = ' '
        board.print()


while(1):
    vis = 0
    c = input_to()
    if (bman.lives > 0):
        for i in range(2, 32):
            for j in range(4, 60):
                if (array[i][j] == 'B'):
                    vis = 1
                    break
        if (vis != 1):
            aa = bman.h1
            bb = bman.w1
            li = bman.lives
            sco = bman.score
            bman = Bomberman(aa, bb)
            bman.lives = li
            bman.score = sco
            for i in range(aa, aa + 2):
                for j in range(bb, bb + 4):
                    array[i][j] = 'B'

    if (bman.lives <= 0):
        print("Game Over")
        print("Your final score is : " + str(bman.score))
        print("Thanks for Playing :)")
        print("")
        break
    elif (c == 'w'):
        if (bman.move_up(bman.h1, bman.w1)):
            bman.h1 -= 2
        board.print()
    elif (c == 's'):
        if (bman.move_down(bman.h1, bman.w1)):
            bman.h1 += 2
        board.print()
    elif (c == 'a'):
        if (bman.move_left(bman.h1, bman.w1)):
            bman.w1 -= 4
        board.print()
    elif (c == 'd'):
        if (bman.move_right(bman.h1, bman.w1)):
            bman.w1 += 4
        board.print()
    elif (c == 'b'):
        boh = bman.h1
        bow = bman.w1
        bomb = Bomb()
        bomb.timer()
    elif (c == 'q'):
        print("Game Over")
        print("Your final score is : " + str(bman.score))
        print("Thanks for Playing :)")
        print("")
        break
