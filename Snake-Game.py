from tkinter import *
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 800
SPACE_SIZE = 50
BODY_PARTS = 4
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self,canvas):
        self.m_bodysize = BODY_PARTS
        self.m_coords = []
        self.m_squres = []
        self.m_dir = "down"
        
        for i in range(0,self.m_bodysize):
            self.m_coords.append([0,0])

        for x,y in self.m_coords:
            squre = canvas.create_rectangle(x,y,x+SPACE_SIZE,
                                            y+SPACE_SIZE,fill = SNAKE_COLOR, tags= "snake")
            self.m_squres.append(squre)

class Food:
    def __init__(self,canvas):
        x = random.randint(0,(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0,(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.m_coord = [x,y]

        canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill = FOOD_COLOR, tags= "food")

class SnackGameEnv:
    def __init__(self):
        self.m_window = Tk()
        self.m_score = 0
        self.m_label = Label(self.m_window, 
                             text="Score:{}".format(self.m_score), font=('consolas', 40))
        self.m_convas = Canvas(self.m_window, bg = BACKGROUND_COLOR, 
                               height = GAME_HEIGHT, width=GAME_WIDTH)
        self.m_snake = Snake(self.m_convas)
        self.m_food = Food(self.m_convas)
        self.m_isDone = 0
        self.CreateFood()

    def CreateFood(self):
        self.m_convas.delete("food")
        self.m_food = Food(self.m_convas)

        # To avoid Food create on the body of snake!
        # if overlap, recreate the food until no overlap
        while True :
            isOverlap = False
            x,y = self.m_food.m_coord
            for i in range(0, len(self.m_snake.m_coords)):
                if x == self.m_snake.m_coords[i][0] and y == self.m_snake.m_coords[i][1]:
                    isOverlap = True
                    self.m_convas.delete("food")
                    self.m_food = Food(self.m_convas)
                    break
            if isOverlap == False :
                break

            

    def DoEating(self):
        self.m_score += 1
        self.m_label.config(text="Score:{}".format(self.m_score))
        self.CreateFood()

    def RunEveryTurn(self):
        '''make move'''
        x,y = self.m_snake.m_coords[0]

        if self.m_snake.m_dir =="down":
            y += SPACE_SIZE
        elif self.m_snake.m_dir =="up":
            y -= SPACE_SIZE
        elif self.m_snake.m_dir =="left":
            x -= SPACE_SIZE
        elif self.m_snake.m_dir =="right":
            x += SPACE_SIZE
            
        self.m_snake.m_coords.insert(0,[x,y])
        square = self.m_convas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.m_snake.m_squres.insert(0, square)

        #check and do eating
        if x == self.m_food.m_coord[0] and y == self.m_food.m_coord[1]:
            self.DoEating()
        #move tail
        else:
            del self.m_snake.m_coords[-1]
            self.m_convas.delete(self.m_snake.m_squres[-1])
            del self.m_snake.m_squres[-1]

        if self.IsCollisions():
            self.DoEndingGame()
        else:
            self.m_window.after(SPEED,self.RunEveryTurn)

    def IsCollisions(self) -> bool:
        x,y = self.m_snake.m_coords[0]
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        
        for i in range(1, len(self.m_snake.m_coords)):
            if x == self.m_snake.m_coords[i][0] and y == self.m_snake.m_coords[i][1]:
                return True
            
        return False
        

    def DoEndingGame(self):
        self.m_convas.delete(ALL)
        self.m_convas.create_text(self.m_convas.winfo_width()/2, self.m_convas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
        self.m_isDone = 0
        
    def DoChangeDir(self,newdir):
        #Careful! if you change the direction twice within a Time interval,for example:
        #snake heads to right,so you can't turn left,but you can change to up ,then you change to right,that will cause Game Over
        #Solution: Get the Origin Dirction by snake's coord,then judge changing dirction can be done
        deltax = self.m_snake.m_coords[0][0] - self.m_snake.m_coords[1][0]
        deltay = self.m_snake.m_coords[0][1] - self.m_snake.m_coords[1][1]

        if deltax == 0 and deltay == SPACE_SIZE:
            oppoolddir = 'up'
        elif deltax == 0 and deltay == -SPACE_SIZE:
            oppoolddir = 'down'
        elif deltax == SPACE_SIZE and deltay == 0:
            oppoolddir = 'left'
        elif deltax == -SPACE_SIZE and deltay == 0:
            oppoolddir = 'right'

        if oppoolddir == newdir:
            return
        
        self.m_snake.m_dir = newdir
    
    def Perform(self):
        self.m_window.title("Snake game")
        self.m_window.resizable(False, False)

        #label = Label(self.m_window, text="Score:{}".format(self.m_score), font=('consolas', 40))
        self.m_label.pack()

        #canvas = Canvas(self.m_window, bg = BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
        self.m_convas.pack()

        self.m_window.update()
        window_width = self.m_window.winfo_width()
        window_height = self.m_window.winfo_height()
        screen_width = self.m_window.winfo_screenwidth()
        screen_height = self.m_window.winfo_screenheight()

        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))

        self.m_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.m_window.bind('<Left>', lambda event: self.DoChangeDir('left'))
        self.m_window.bind('<Right>', lambda event: self.DoChangeDir('right'))
        self.m_window.bind('<Up>', lambda event: self.DoChangeDir('up'))
        self.m_window.bind('<Down>', lambda event: self.DoChangeDir('down'))

        self.RunEveryTurn()
        self.m_window.mainloop()




env = SnackGameEnv()
env.Perform()