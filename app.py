from tkinter import *
import random
import os , sys


GAME_WIDTH = 800
GAME_HEIGht = 650
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"



class Snake:
    def __init__(self) -> None:
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = canva.create_rectangle(x, y, x+ SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    
    def __init__(self) -> None:
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGht / SPACE_SIZE) - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        
        canva.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")



def change_directions(new_direction):
    global direction
    # print(new_direction, direction)
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction
     
#  for the restart function to work witjhout destroying the previous window use beliow function 

# def return_home(data):
    # print("hi")
    # os.execl(sys.executable, sys.executable, *sys.argv)
    # global score
    # score = 0
    # label.config(text="Score: {}".format(score))
        
    # canva.delete(ALL)
    # snake = Snake()
    # food = Food()
    # next_turn(snake, food)
    # window.unbind("<space>")
    
    


def game_over():
    global score
    canva.delete(ALL)
    
    max_score = read_scores()
    if score> max_score[0]:
        canva.create_text(canva.winfo_width()/2, canva.winfo_height()/2 - 270, font=("consolas", 50), text="You made a High Score", fill="green", tag="highscore")
    else:
        canva.create_text(canva.winfo_width()/2, canva.winfo_height()/2 - 270, font=("consolas", 50), text="The High Score is:-", fill="green", tag="highscore")
        canva.create_text(canva.winfo_width()/2, canva.winfo_height()/2 - 200, font=("consolas", 30), text=max_score[1], fill="green", tag="highscore")
        canva.create_text(canva.winfo_width()/2, canva.winfo_height()/2 - 100, font=("consolas", 20), text="You Didn't make it to the High Score", fill="red", tag="lowscore")
    
    
    canva.create_text(canva.winfo_width()/2, canva.winfo_height()/2 - 20, font=("consolas", 70), text="GAME OVER", fill="red", tag="gameover")
    
    restart = canva.create_text(canva.winfo_width()/2, canva.winfo_height()/2 + 50, font=("consolas", 30), text="Press SPACE to restart", fill="white", tag="restart")
    
    window.bind("<space>", lambda event: os.execl(sys.executable, sys.executable, *sys.argv))
    
    name_label = Label(window, text="Name: ", font=("consolas", 20))
    canva.create_window(canva.winfo_width()/2 - 150, canva.winfo_height()/2 + 100, window=name_label)
    
    name_entry = Entry(window, font=("consolas", 20))
    name_entry.focus()
    canva.create_window(canva.winfo_width()/2 + 70 , canva.winfo_height()/2 + 100, window=name_entry)
    
    submit_button = Button(window, text="Submit", font=("consolas", 20), command=lambda: submit_score(name_entry.get(), score, name_entry))
    canva.create_window(canva.winfo_width()/2, canva.winfo_height()/2 + 150, window=submit_button)
    window.bind("<Return>", lambda event: submit_score(name_entry.get(), score, name_entry))
    
    


def submit_score(name, score, name_entry):
    with open("scores.txt", "a") as f:
        f.write(f"{name} : {score}\n")
    f.close()
    name_entry.delete(0, END)
    # os.execl(sys.executable, sys.executable, *sys.argv)


def read_scores():
    max_data = 0
    max_arr = ["User", ":", "0"]
    with open("scores.txt", "r") as f:
        for line in f.readlines():
            data = line.strip()
            if max_data < int(data.split()[-1]):
                max_data = int(data.split()[-1])
                max_arr = data.split()
        f.close()

    return (max_data," ".join(max_arr))
    


def check_collisions(snake ):
    x, y = snake.coordinates[0]
    
    if x<0 or x>= GAME_WIDTH:
        return True
    elif y<0 or y>= GAME_HEIGht:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False


def next_turn(snake, food):
    # print("in turn_function", direction)
    x, y = snake.coordinates[0]
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y +=SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x +=SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))
    
    square = canva.create_rectangle(x, y, x+ SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        global SPEED
        score +=1
        if score > 5 and score <= 10:
            SPEED = 90
        elif score > 10 and score <= 15:
            SPEED = 70
        elif score > 15 and score <= 20:
            SPEED = 50
        elif score > 20 and score <= 25:
            SPEED = 30
        elif score > 25:
            SPEED = 10
        canva.delete("food")
        food = Food()
        label.config(text="Score: {}".format(score))
    
    else:
        del snake.coordinates[-1]
        canva.delete(snake.squares[-1])
        del snake.squares[-1]

    
    if check_collisions(snake):
        game_over()
    
    else:
        window.after(SPEED, next_turn, snake, food)
        
    



window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0

direction = "down"

canva = Canvas(window, width=GAME_WIDTH, height=GAME_HEIGht, bg=BACKGROUND_COLOR)
canva.pack()

label = Label(window, text="Score: {}".format(score), font=("consolas", 40))
label.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int(screen_width/2 - window_width/2)
y = int(screen_height/2 - window_height/2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Up>", lambda event: change_directions("up"))
window.bind("<Down>", lambda event: change_directions("down"))
window.bind("<Left>", lambda event: change_directions("left"))
window.bind("<Right>", lambda event: change_directions("right"))


snake  = Snake()
food = Food()
next_turn(snake, food)
window.mainloop()

