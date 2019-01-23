from tkinter import *
import time
import random

root = Tk()
root.title("Bounce")
root.geometry("600x570")
root.resizable(0, 0)
root.wm_attributes("-topmost",1)
canvas = Canvas(root, width=600, height=500, bd=0, highlightthickness=2, highlightbackground="Red", bg="lightgreen")
canvas.pack(padx=0, pady=20)
score = Label(height=50, width=100, text="Score: 000", font="Time 15 ")
score.pack(side="left")
root.update()


class Ball:
    def __init__(self, canvas, color, paddle, bricks, score):
        self.bricks = bricks
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.bottom_hit = False
        self.hit =0
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color, width=1)
        self.canvas.move(self.id, 230,460)
        start = [4, 3.8, 3.6, 3.4, 3.2, 3, 2.8, 2.6]
        random.shuffle(start)
        #print(start)
        self.x = start[0]
        self.y = -start[0]
        self.canvas.move(self.id, self.x, self.y)
        self.canvas_height = canvas.winfo_height()
        self.canvas_width = canvas.winfo_width()
    
    def brick_hit(self, pos):
        for brick_line in self.bricks:
            for brick in brick_line:
                brick_pos = self.canvas.coords(brick.id)
                #print(brick_pos)
                try:
                    if pos[2] >= brick_pos[0] and pos[0] <= brick_pos[2]:
                        if pos[3] >= brick_pos[1] and pos[1] <= brick_pos[3]:
                            canvas.bell()
                            self.hit += 10
                            self.score.configure(text="Score: " + str(self.hit))
                            self.canvas.delete(brick.id)
                            return True
                except:
                    continue
        return False
    
        
    def paddle_hit(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
                #print("paddle hit")
                return True
            return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        #print(pos)
        start = [4, 3.8, 3.6, 3.4, 3.2, 3, 2.8, 2.6]
        random.shuffle(start)
        if self.brick_hit(pos):
            self.y = start[0]
        if pos[1] <= 0:
            self.y = start[0]
        if pos[3] >= self.canvas_height:
            self.bottom_hit = True
        if pos[0] <= 0:
            self.x = start[0]
        if pos[2] >= self.canvas_width:
            self.x = -start[0]
        if self.paddle_hit(pos):
            self.y = -start[0]

        
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 485)
        self.x = 0
        self.pausec=0
        self.canvas_width = canvas.winfo_width()
        self.canvas.bind_all("<Left>", self.turn_left)
        self.canvas.bind_all("<Right>", self.turn_right)
        self.canvas.bind_all("<space>", self.pauser)
        

    def draw(self):
        pos = self.canvas.coords(self.id)
        #print(pos)
        if pos[0] + self.x <= 0:
            self.x = 0
        if pos[2] + self.x >= self.canvas_width:
            self.x = 0
        self.canvas.move(self.id, self.x, 0)

    def turn_left(self, event):
        self.x = -5

    def turn_right(self, event):
        self.x = 5

    def pauser(self,event):
        self.pausec+=1
        if self.pausec==2:
            self.pausec=0
    

class Bricks:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_oval(5, 5, 26, 26, fill=color, width=1)


playing = False


def start_game(event):
    global playing
    if playing is False:
        playing = True
        score.configure(text="Score: 000")
        canvas.delete("all")
        BALL_COLOR = ["red", "yellow", "white"]
        BRICK_COLOR = ["royalblue1", "maroon2", "rosy brown", "light goldenrod yellow", "turquoise3", "salmon",
                       "light steel blue", "limegreen", "pale violet red", "sandybrown", "tan", "MistyRose2",
                       "springgreen", "indigo", "tan2", "tomato3", "violetred"]
        random.shuffle(BALL_COLOR)
        paddle = Paddle(canvas, "blue")
        bricks = []
        for i in range(0, 8):
            b = []
            for j in range(0, 25):
                random.shuffle(BRICK_COLOR)
                tmp = Bricks(canvas, BRICK_COLOR[0])
                b.append(tmp)
            bricks.append(b)

        for i in range(0, 8):
            for j in range(0, 25):
                canvas.move(bricks[i][j].id, 25 * j, 25 * i)

        ball = Ball(canvas, BALL_COLOR[0], paddle, bricks, score)
        root.update_idletasks()
        root.update()

        time.sleep(1)
        while 1:
            if paddle.pausec !=1:
                try:
                    canvas.delete(m)
                    del m
                except:
                    pass
                if not ball.bottom_hit:
                    ball.draw()
                    paddle.draw()
                    root.update_idletasks()
                    root.update()
                    time.sleep(0.0001)
                    if ball.hit==500:
                        canvas.create_text(300, 300, text="YOU WON !!", fill="yellow", font="Time 20 ")
                        root.update_idletasks()
                        root.update()
                        playing = False
                        break
                else:
                    canvas.create_text(300, 300, text="GAME OVER!!", fill="red", font="Time 24 ")
                    root.update_idletasks()
                    root.update()
                    playing = False
                    break
            else:
                try:
                    if m==None:pass
                except:
                    m=canvas.create_text(250, 250, text="PAUSE!!", fill="green", font="Consolas 24 ")
                root.update_idletasks()
                root.update()
                
root.bind_all("<Return>", start_game)
canvas.create_text(250, 225, text="WELCOME TO  GAME!!!", fill="gray", font="Time 18")

name=Label(root,text="USERNAME").place(x = 0,y = 1)
e1= Entry(root).place(x=80, y= 1)
canvas.create_text(260, 275, text="Press Enter to start Game!!", fill="orange", font="System 18")
j=canvas.find_all()
root.mainloop()