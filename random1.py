import tkinter as tk
import random
import time

stop = False

#jobs
tick_job = 0
move_job = 0
create_wall_job = 0
wall_move_job = 0
crash_test_job = 0

speed = 0
speed_set = 5
acceleration = -10

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
    global score_text, best_score
    score = 0
    for i in wall:
        _, _, wall_x2, _ = canvas.coords(i[0])
        obj_x1, _, _, _ = get_pos()
        if (wall_x2 < obj_x1):
            score += 1
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
    if (event.keysym == "space"):
        speed = speed_set
    elif(event.keysym == "c"):
        stop = True
    elif(event.keysym == "r"):
        restart()


#job functions
def move():
    global obj, hitbox, move_job
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
    speed = speed + acceleration * 0.001
    tick_job = root.after(1, tick)

def creat_wall():
    global wall_time_distance, hole_pos, hole_size, create_wall_job
    if (stop):
        return
    if (RANDOM_WALLS):
        wall_time_distance = random.randint(1200, 2000)
        hole_size = random.randint(50, 400)
        hole_pos = random.randint(0, 600 - hole_size)
    wall.append([])
    wall_count = len(wall) - 1
    wall[wall_count].append(
        canvas.create_rectangle(800, 0, 800 + wall_thickness, hole_pos, fill="red")

    )
    wall[wall_count].append(
        canvas.create_rectangle(800, hole_size + hole_pos, 800 + wall_thickness, 600, fill="red")
    )
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
    print(num)
    if (num > 2 or (pos[1] < 0 or pos[3] > 600)):
        stop = True
        print_score()
        cancel_jobs()
    crash_test_job = root.after(20, crash_test)


def cancel_jobs():
    for i in [tick_job, move_job, create_wall_job, wall_move_job, crash_test_job]:
        root.after_cancel(i)


def delete_all():
    global wall, stop
    for i in wall:
        for j in i:
            canvas.delete(j)
    delete_obj()
    delete_score()


def start():
    global wall, stop
    stop = False
    wall = []
    creat_obj()

    creat_wall()
    wall_move()

    move()
    tick()
    crash_test()



def restart():
    delete_all()
    start()

start()


root.bind("<Key>", key_pressed)
root.mainloop()