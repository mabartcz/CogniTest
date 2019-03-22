# Martin Barton, CTU, 2019
# martin.barton@skaut.cz

# DODELAT #
# anticheat v RT
# Vic desetinejch mist u RT ?

# RT 10x 2-5 sec

import pgzrun, random, time, datetime


WIDTH = int(1280/2)
HEIGHT = int(720/2)

TITLE = "CogniTest"
WHITE   =   (255, 255, 255)
BLACK   =   (0  ,   0,   0)
RED     =   (255,   0,   0)
GREEN   =   (0  , 255,   0)
BLUE    =   (0  ,   0, 255)
BG      =   (190, 190, 190)
FONT = "bastardussans"

# Events
# 1 - Reaction time
# 2 - DSST
# 3 - VAS


# Variables for all
event = 0
saved = False

# Variables for 1
press = False
time_start = 0
reaction_time = []

# Variables for 2
sim = Actor('znak_blank')
sim1 = Actor('znak_blank')
sim2 = Actor('znak_blank')
sim3 = Actor('znak_blank')
sim4 = Actor('znak_blank')
sim5 = Actor('znak_blank')
sim6 = Actor('znak_blank')
sim7 = Actor('znak_blank')
sim8 = Actor('znak_blank')
sim9 = Actor('znak_blank')

wide = 50
gap = int(wide/5)
wpul = int((WIDTH - 9*wide - 10*gap)/2) + int(wide/2)
h_h = int((HEIGHT/3)*1)
s_h = h_h + wide*3.3

sim.pos = int(WIDTH/2), s_h
sim1.pos = int(wpul + gap), h_h
sim2.pos = int(wpul + gap*2 +wide), h_h
sim3.pos = int(wpul + gap*3 +wide*2), h_h
sim4.pos = int(wpul + gap*4 +wide*3), h_h
sim5.pos = int(wpul + gap*5 +wide*4), h_h
sim6.pos = int(wpul + gap*6 +wide*5), h_h
sim7.pos = int(wpul + gap*7 +wide*6), h_h
sim8.pos = int(wpul + gap*8 +wide*7), h_h
sim9.pos = int(wpul + gap*9 +wide*8), h_h

shuffled = [1, 2, 3, 4, 5, 6, 7, 8, 9]

pressed = []
correct = []
round = 0
dsst_start_time = time.time() + 1000000 # Does not affect duration, only placeholder
dsst_correct_sum = 0
dsst_false_sum = 0


def draw():
    load()
    if event == 4 or event == 5:
        dsst_draw()

def update():
    global event, saved

    dsst_duration = 1                                  # DSST duration
    if event == 4 or event == 5:
        if dsst_start_time + dsst_duration < time.time():
            event = 6



def on_key_down(key):
    global event, time_end, press
    if key == keys.SPACE:
        if event == 1:
            reaction()
        elif event == 3:
            event = 4
        elif event == 4:
            dsst_move(key)
            event = 5


    numbers = [keys.K_1, keys.K_2, keys.K_3, keys.K_4, keys.K_5, keys.K_6, keys.K_7, keys.K_8, keys.K_9 ]
    if key in numbers:
        if event == 5:
            dsst_move(key)


#-----------------------------------------------------------------------------------------------
#***********************************************************************************************
#-----------------------------------------------------------------------------------------------
# Other

def load():
    global event, saved
    if event == 0:
        screen.fill(BG)
        text1 = "REACTION TIME TEST\n\npress SPACE for start"
        screen.draw.text(text1, center=(int(WIDTH / 2), int(HEIGHT / 2)), fontname=FONT, fontsize=32, color=BLACK)
        event = 1
    elif event == 2:
        screen.fill(BG)
        text1 = "DSST\n\npress SPACE for LOAD\nthan\npress SPACE for START"
        screen.draw.text(text1, center=(int(WIDTH / 2), int(HEIGHT / 2)), fontname=FONT, fontsize=32, color=BLACK)
        event = 3
    elif event == 6:
        screen.fill(BG)
        text1 = "VAS\n\npress SPACE for START"
        screen.draw.text(text1, center=(int(WIDTH / 2), int(HEIGHT / 2)), fontname=FONT, fontsize=32, color=BLACK)
        event = 7
    elif event == 7:
        if saved == False:
            save_file()
            #print("File not saved!")
            saved = True

def save_file():
    print("Saving!")
    screen.fill(BG)
    # autosave data
    f_name = "./results/dsst-" + str(datetime.datetime.now().strftime("%d-%m-%y-%H%M%S") + ".csv")
    file = open(f_name, "w")
    file.write("Time of test," + str(datetime.datetime.now().strftime("%H:%M %d.%m. %Y")))
    file.write("\nReaction time")
    file.write("\nSample,Reaction time (sec)")
    for k in range(len(reaction_time)):
        file.write("\n" + str(k + 1) + "," + "{0:.3f}".format(reaction_time[k]))
        # file.write("\n" + str(k + 1) + "," + str(reaction_time[k]))
    file.write("\nDSST")
    file.write("\nCorrect,False\n")
    file.write(str(dsst_correct_sum))
    file.write(",")
    file.write(str(dsst_false_sum))
    file.close()
    print("Saved!")

# -----------------------------------------------------------------------------------------------
# ***********************************************************************************************
# -----------------------------------------------------------------------------------------------
# Reaction time

def reaction():
    global event
    if time_start < time.time():
        if press == True:
            time_end = time.time()
            print("Reaction time: " + str(time_end - time_start))
            reaction_time.append(time_end - time_start)     # Add RT to array

            if len(reaction_time) == 1:                     # Number of measurements
               event = 2
            else:
                start_reaction()

        if press == False:
            start_reaction()
    else:
        pass                                                # Dodelat pripadne anticheat

def start_reaction():
    global delay, time_start, press

    #delay = random.uniform(1,1)                            # Generate random number
    delay = 0.1                                             # Generate random number
    screen.fill(BG)
    clock.schedule(show_circle, delay)                      #Circle appear after delay

    time_start = time.time() + delay
    press = True

def show_circle():
    screen.draw.filled_circle(((int(WIDTH / 2), int(HEIGHT / 2))), int(HEIGHT / 2.1), RED)

#-----------------------------------------------------------------------------------------------
#***********************************************************************************************
#-----------------------------------------------------------------------------------------------
# DSST

def dsst_move(key):
    global shuffled, pressed, correct, round, dsst_start_time, event, dsst_correct_sum, dsst_false_sum

    random.shuffle(shuffled)
    sim_random = random.randint(1, 9)

    sim.image = "znak_" + str(sim_random)
    sim1.image = "znak_" + str(shuffled[0])
    sim2.image = "znak_" + str(shuffled[1])
    sim3.image = "znak_" + str(shuffled[2])
    sim4.image = "znak_" + str(shuffled[3])
    sim5.image = "znak_" + str(shuffled[4])
    sim6.image = "znak_" + str(shuffled[5])
    sim7.image = "znak_" + str(shuffled[6])
    sim8.image = "znak_" + str(shuffled[7])
    sim9.image = "znak_" + str(shuffled[8])


    pressed.append(key.value - 48)
    correct.append(shuffled.index(sim_random)+1)

    if round != 0:
        if pressed[round] == correct[round - 1]:
            dsst_correct_sum += 1
            print(True)
        else:
            print(False)
            dsst_false_sum += 1
    else:
        dsst_start_time = time.time()


    round += 1

def dsst_draw():
    screen.fill(BG)
    sim.draw()
    sim1.draw()
    sim2.draw()
    sim3.draw()
    sim4.draw()
    sim5.draw()
    sim6.draw()
    sim7.draw()
    sim8.draw()
    sim9.draw()

    for x in range(1, 10):
        screen.draw.text(str(x), center=(int(wpul + gap * x + wide * (x - 1)), h_h + wide), fontname=FONT, fontsize=32,
                         color=BLACK)



pgzrun.go()

