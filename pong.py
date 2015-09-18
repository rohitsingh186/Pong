# Implementation of classic arcade game Pong
import simplegui
import random


# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 20
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

GUTTER1_POS = [[0, 0], [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], [0, HEIGHT]]
GUTTER2_POS = [[WIDTH - PAD_WIDTH, 0], [WIDTH, 0], [WIDTH, HEIGHT], [WIDTH - PAD_WIDTH, HEIGHT]]

paddle1_vel = 0
paddle2_vel = 0

score = [0, 0]
score_color = ["Silver", "Silver"]

pad_vel = 0

pong_text_width = 0 # We'll update it after creating a frame


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, pad_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    vel_x = random.randrange(2, 4)
    vel_y = random.randrange(1, 3)
    pad_vel = 2
    if direction == "LEFT":
        ball_vel = [- vel_x, - vel_y]
    elif direction == "RIGHT":
        ball_vel = [vel_x, - vel_y]
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score, score_color, pad_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [[0, (HEIGHT - PAD_HEIGHT) / 2], [PAD_WIDTH, (HEIGHT - PAD_HEIGHT) / 2], [PAD_WIDTH, (HEIGHT + PAD_HEIGHT) / 2], [0, (HEIGHT + PAD_HEIGHT) / 2]]
    paddle2_pos = [[WIDTH - PAD_WIDTH, (HEIGHT - PAD_HEIGHT) / 2], [WIDTH, (HEIGHT - PAD_HEIGHT) / 2], [WIDTH, (HEIGHT + PAD_HEIGHT) / 2], [WIDTH - PAD_WIDTH, (HEIGHT + PAD_HEIGHT) / 2]]
    paddle1_vel = 0
    paddle2_vel = 0
    score = [0, 0]
    score_color = ["Silver", "Silver"]
    pad_vel = 2
    dircn = random.choice(["LEFT", "RIGHT"])
    spawn_ball(dircn)

    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, pad_vel
    # Draw Pong Textual Icon
    canvas.draw_text("Pong", [(WIDTH - pong_text_width) / 2, 60], 70, "Purple")
    
    # update ball
    # Ball Position Update
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    # Collision with top/bottom walls
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = - ball_vel[1]
    
    # Collision with gutters
    if (ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH)) and (ball_pos[1] >= paddle1_pos[0][1]) and (ball_pos[1] <= paddle1_pos[3][1]):
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = 1.1 *  ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]
        pad_vel = 1.1 * pad_vel
    elif (ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS)) and (ball_pos[1] >= paddle2_pos[0][1]) and (ball_pos[1] <= paddle2_pos[3][1]):
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = 1.1 *  ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]
        pad_vel = 1.1 * pad_vel
    elif ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        spawn_ball("RIGHT")
        score[1] += 1
        if score[1] > score[0]:
            score_color[1] = "Orange"
        elif score[1] == score[0]:
            score_color[0] = "Silver"
    elif ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):
        spawn_ball("LEFT")
        score[0] += 1
        if score[0] > score[1]:
            score_color[0] = "Orange"
        elif score[0] == score[1]:
            score_color[1] = "Silver"
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "Black")
    canvas.draw_polygon(GUTTER1_POS, 1, "Black", "Red")
    canvas.draw_polygon(GUTTER2_POS, 1, "Black", "Red")
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Black", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_vel < 0):
        if (paddle1_pos[0][1] < (- paddle1_vel)):
            paddle1_pos[0][1] = 0
            paddle1_pos[1][1] = 0
            paddle1_pos[2][1] = PAD_HEIGHT
            paddle1_pos[3][1] = PAD_HEIGHT
        else:
            paddle1_pos[0][1] += paddle1_vel
            paddle1_pos[1][1] += paddle1_vel
            paddle1_pos[2][1] += paddle1_vel
            paddle1_pos[3][1] += paddle1_vel
    elif (paddle1_vel > 0):
        if (paddle1_pos[3][1] > (HEIGHT - paddle1_vel)):
            paddle1_pos[0][1] = HEIGHT - PAD_HEIGHT
            paddle1_pos[1][1] = HEIGHT - PAD_HEIGHT
            paddle1_pos[2][1] = HEIGHT
            paddle1_pos[3][1] = HEIGHT
        else:
            paddle1_pos[0][1] += paddle1_vel
            paddle1_pos[1][1] += paddle1_vel
            paddle1_pos[2][1] += paddle1_vel
            paddle1_pos[3][1] += paddle1_vel
    if (paddle2_vel < 0):
        if (paddle2_pos[0][1] < (- paddle2_vel)):
            paddle2_pos[0][1] = 0
            paddle2_pos[1][1] = 0
            paddle2_pos[2][1] = PAD_HEIGHT
            paddle2_pos[3][1] = PAD_HEIGHT
        else:
            paddle2_pos[0][1] += paddle2_vel
            paddle2_pos[1][1] += paddle2_vel
            paddle2_pos[2][1] += paddle2_vel
            paddle2_pos[3][1] += paddle2_vel
    elif (paddle2_vel > 0):
        if (paddle2_pos[3][1] > (HEIGHT - paddle2_vel)):
            paddle2_pos[0][1] = HEIGHT - PAD_HEIGHT
            paddle2_pos[1][1] = HEIGHT - PAD_HEIGHT
            paddle2_pos[2][1] = HEIGHT
            paddle2_pos[3][1] = HEIGHT
        else:
            paddle2_pos[0][1] += paddle2_vel
            paddle2_pos[1][1] += paddle2_vel
            paddle2_pos[2][1] += paddle2_vel
            paddle2_pos[3][1] += paddle2_vel
    
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, "Black", "Green")
    canvas.draw_polygon(paddle2_pos, 1, "Black", "Green")
    
    # draw scores
    canvas.draw_text(str(score[0]), [WIDTH / 4, 60], 60, score_color[0], "sans-serif")
    canvas.draw_text(str(score[1]), [3 * WIDTH / 4, 60], 60, score_color[1], "sans-serif")
        

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = - pad_vel
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = pad_vel
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = - pad_vel
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = pad_vel
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
        
     
def restart():
    new_game()

        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background("Teal")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart, 200)

# Pong Text Width
pong_text_width = frame.get_canvas_textwidth("Pong", 80)


# start frame
new_game()
frame.start()
