import tkinter as tk
import random
import time

stop = False

def nothing():
    pass




score = 0
speed = 0
speed_set = 5
acceleration = -10
gravity = 1
gravity_change_time = 10000

RANDOM_WALLS = True
SHOW_HITBOX = False

wall_thickness = 30
hole_size = 200
hole_pos = 250
wall_speed = 200
wall_time_distance = 500
wall = []
best_score = 0
root = tk.Tk()

#jobs
tick_job = root.after(0, nothing)
move_job = root.after(0, nothing)
create_wall_job = root.after(0, nothing)
wall_move_job = root.after(0, nothing)
crash_test_job = root.after(0, nothing)
gravity_job = root.after(0, nothing)
score_counting_job = root.after(0, nothing)
ingame_score_job = root.after(0, nothing)

#helpers
def get_pos():
    global obj, hitbox
    pos = canvas.coords(obj)
    return pos

# creating and deleting
canvas = tk.Canvas(root, width=800, height=600, bg="green")
canvas.pack()

obj = 0
hitbox = 0
score_text = 0
ingame_score_text = 0

def creat_obj():
    global obj, hitbox
    if (SHOW_HITBOX):
        hitbox = canvas.create_rectangle(50, 285, 80, 315, outline="red")
    else:
        hitbox = canvas.create_rectangle(50, 285, 80, 315, outline="green")
    obj = canvas.create_oval(50, 285, 80, 315, fill="black")

def delete_obj():
    global obj, hitbox
    canvas.delete(obj)
    canvas.delete(hitbox)

def print_score():
    global score_text, best_score, score

    if (score > best_score):
        best_score = score

    score_text = canvas.create_text(400, 300,
                    text=f"GAME OVER!\nScore: {score}\nBest score: {best_score}",
                    fill="black", font=("Arial", 50))

def delete_score():
    global score_text
    canvas.delete(score_text)

def key_pressed(event):
    global speed, stop
    if (event.keysym == "space" and not stop):
        speed = speed_set * gravity
    elif(event.keysym == "c"):
        stop = True
    elif(event.keysym == "space" and stop):
        restart()


#job functions
def move():
    global obj, hitbox, move_job, gravity
    if (stop):
        return
    global speed
    canvas.move(obj, 0, -speed)
    canvas.move(hitbox, 0, -speed)
    move_job = root.after(20, move)

def tick():
    global tick_job
    if (stop):
        return
    global speed
    speed = speed + acceleration * 0.001 * gravity
    tick_job = root.after(1, tick)

def creat_wall():
    global wall_time_distance, hole_pos, hole_size, create_wall_job
    hole_pos_last = hole_pos
    if (stop):
        return
    if (RANDOM_WALLS):
        wall_time_distance = random.randint(1200, 2000)
        hole_size = random.randint(80, 300)
        hole_pos_new = random.randint(50, 600 - hole_size - 50)
        hole_pos = (hole_pos_last + hole_pos_new) // 2
        if (hole_pos < 50):
            hole_pos = 50
        elif (hole_pos > 600 - hole_size - 50):
            hole_pos = 600 - hole_size - 50
    
    
    
    wall.append([])
    wall_count = len(wall) - 1
    wall[wall_count].append(
        canvas.create_rectangle(800, 0, 800 + wall_thickness, hole_pos, fill="red")
    )
    wall[wall_count].append(
        canvas.create_rectangle(800, hole_size + hole_pos, 800 + wall_thickness, 600, fill="red")
    )
    wall[wall_count].append(
        canvas.create_rectangle(800 - 10, hole_pos - 50, 800 + wall_thickness + 10, hole_pos, fill="red")
    )
    wall[wall_count].append(
        canvas.create_rectangle(800 - 10, hole_pos + hole_size + 50, 800 + wall_thickness + 10, hole_pos + hole_size, fill="red")
    )
    wall[wall_count].append(0) #0 = not counted, 1 = counted

    create_wall_job = root.after(wall_time_distance, creat_wall)

def wall_move():
    global wall_move_job
    if (stop):
        return
    global wall_speed
    for i in wall:
        for j in i:
            canvas.move(j, -wall_speed * (20/1000), 0)
    wall_move_job = root.after(20, wall_move)

def crash_test():
    global crash_test_job
    global obj, hitbox
    global stop
    if (stop):
        return
    pos = get_pos()
    hits = canvas.find_overlapping(*pos)
    num = len(hits)
    #print(num)
    if (num > 2 or (pos[1] < 0 or pos[3] > 600)):
        stop = True
        print_score()
        cancel_jobs()
    crash_test_job = root.after(20, crash_test)

def gravity_change():
    global gravity_job, gravity, gravity_change_time
    if (stop):
        return
    if (RANDOM_WALLS):
        gravity_change_time = random.randint(5000, 15000)

    canvas.configure(bg="cyan")
    gravity_job = root.after(1000, gravity_change_2)

def gravity_change_2():
    global gravity_job, gravity, gravity_change_time
    gravity *= -1
    if (gravity == 1):
        canvas.configure(bg="green")
    else:
        canvas.configure(bg="blue")

    gravity_job = root.after(gravity_change_time, gravity_change)

def score_counting():
    global score_counting_job, score
    if (stop):
        return
    for i in wall:
        _, _, wall_x2, _ = canvas.coords(i[2])
        obj_x1, _, _, _ = get_pos()
        if (wall_x2 < obj_x1):
            if (i[4] == 0): # Check if wall has not been counted yet
                score += 1
                i[4] = 1 # Mark as counted
    #print(score)
    for i in wall:
        _, _, wall_x2, _ = canvas.coords(i[2])
        if (wall_x2 < 0 and i[4] == 1): # Check if wall has moved off screen and has been counted
            for j in i:
                canvas.delete(j)
            wall.remove(i)
    score_counting_job = root.after(20, score_counting)

def delete_ingame_score():
    global ingame_score_text
    canvas.delete(ingame_score_text)

def print_ingame_score():
    global ingame_score_text, score, ingame_score_job
    delete_ingame_score()
    ingame_score_text = canvas.create_text(80, 20,
                    text=f"Score: {score}",
                    fill="black", font=("Arial", 30))
    ingame_score_job = root.after(20, print_ingame_score)

def cancel_jobs():
    for i in [tick_job,
              move_job,
              create_wall_job,
              wall_move_job,
              crash_test_job,
              gravity_job,
              score_counting_job,
              ingame_score_job
              ]:
        root.after_cancel(i)


def delete_all():
    global wall, stop
    for i in wall:
        for j in i:
            canvas.delete(j)
    delete_obj()
    delete_score()
    cancel_jobs()


def start():
    global wall, stop, speed, gravity, score
    stop = False
    speed = 0
    gravity = 1
    score = 0
    canvas.configure(bg="green")
    wall = []
    creat_obj()

    creat_wall()
    wall_move()

    move()
    tick()
    crash_test()
    score_counting()
    print_ingame_score()
    root.after(10000, gravity_change)


def restart():
    delete_all()
    start()

start()


root.bind("<Key>", key_pressed)
root.mainloop()