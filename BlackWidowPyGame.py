import pygame
from pygame import mixer
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
 
pygame.init()
pygame.display.set_caption("Black Widow")
clock = pygame.time.Clock()
#SFX for player projectile
shoot_sound = pygame.mixer.Sound('Contra SFX (15).wav')
shoot_sound.set_volume(0.6)
#In game music
music = pygame.mixer.Sound('The House of the Dead OST - Boss Theme - Arcade Ver. (Actual Hardware).mp3')
music.set_volume(0.5)
music.play(-1)
#SFX for collecting a point
collect_sound = pygame.mixer.Sound('Crash Bandicoot Sounds - Wumpa Fruit.mp3')
collect_sound.set_volume(0.6)
 
 
#For background
gx=14
gy=10
ground_verticies=((gx,gy,10),#V0
                  (-gx,gy,10),#V1
                  (-gx,gy,-10),#V2
                  (gx,gy,-10))#V3
ground_edges=((0,1),(1,2),(2,3),(3,0))
ground_faces=((0,1,2,3))
ground_coords=((0,1),(1,1),(1,0),(0,0))
 
#For cone
scale=0.5
cm=+0.5
Triverticies = (
    (-1.018606*scale, -0.999790*scale, -0.100324*scale),
    (-0.791166*scale, -0.999696*scale, 0.649293*scale),
    (-0.100325*scale, -0.999805*scale, 1.018614*scale),
    (0.649293*scale, -0.999696*scale, 0.791166*scale),
    (1.018606*scale, -0.999790*scale, 0.100324*scale),
    (0.791166*scale, -0.999696*scale, -0.649293*scale),
    (0.100325*scale, -0.999805*scale, -1.018614*scale),
    (-0.649293*scale, -0.999696*scale, -0.791166*scale),
    (0.000000, 1.000000*scale, 0.000000)
    )
Triedges = (
    (0,1),
    (0,8),
    (1,2),
    (1,8),
    (2,3),
    (2,8),
    (3,4),
    (3,8),
    (4,5),
    (4,8),
    (5,6),
    (5,8),
    (6,7),
    (6,8),
    (7,0),
    (7,8),
    )
 
#For cubes
verticies = ((1, -1, -1),(1, 1, -1),(-1, 1, -1),(-1, -1, -1),(1, -1, 1),(1, 1, 1),(-1, -1, 1),(-1, 1, 1))
edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
faces = ((0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))
colors = ((1,0,0),(0,1,0),(0,0,1),(0,1,1),(1,0,1),(1,1,0)) 
colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,1),
    (1,0,1),
    (1,1,0),
    )
normals = [
( 0,  0, -1),  # surface 0
(-1,  0,  0),  # surface 1
( 0,  0,  1),  # surface 2
( 1,  0,  0),  # surface 3
( 0,  1,  0),  # surface 4
( 0, -1,  0)   # surface 5
    ]
#Displays text on screen
def drawText(x, y, text, size):   
    font = pygame.font.SysFont('arial', size)     
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)                                        
    textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
#Method Places textures on 3D objects
def load_texture(image_name):
    image = pygame.image.load(image_name) 
    data = pygame.image.tostring(image, 'RGBA')
    texID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,texID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return texID
 
# draw cube function
def Box():
    glColor3fv((1,1,1))
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    for face in faces:
        for i, vertex in enumerate(face):
            glTexCoord2fv(ground_coords[i])
            glVertex3fv(verticies[vertex])
            
    glEnd()
    glColor3fv((1,1,1))
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()
    glDisable(GL_TEXTURE_2D)
 
#Draw Tri
def Tri():
    glBegin(GL_LINES)
    for edge in Triedges:
        for vertex in edge:
            glVertex3fv(Triverticies[vertex])
            glColor3f(1,0,0)
    glEnd()
 
#draw sphere function
def Sphere():
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    sphere = gluNewQuadric()
    gluSphere(sphere, 1.0, 32, 16) #x,y,z
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
#draw square function
def Cube():
    glBegin(GL_QUADS)
    i = -2
    for face in faces: 
        i += 1
        for vertex in face:
            glColor3fv(colors[i])
            glVertex3fv(verticies[vertex]) 
    glEnd()
    
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((1,1,1))
            glVertex3fv(verticies[vertex])
    glEnd()
 
#Beetle RocketBug Mosquito GrenadeBug
def enemy(bug):
    if(bug=="Mosquito"):
        enemy_texID = load_texture('Mosquito.jpg')
    if(bug=="Beetle"):
        enemy_texID = load_texture('Beetle.jpg')
    if(bug=="GrenadeBug"):
        enemy_texID = load_texture('GrenadeBug.jpg')
    if(bug=="RocketBug"):
        enemy_texID = load_texture('RocketBug.jpg')
    if(bug=="Widow"):
        enemy_texID = load_texture('Widow.jpg')
    glColor3fv((1,1,1))
    glEnable(GL_TEXTURE_2D)
    
    glBegin(GL_QUADS)
    for face in ground_faces:
        for i,vertex in enumerate(ground_faces):
            glTexCoord2fv(ground_coords[i])
            glVertex3fv(ground_verticies[vertex])
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_LINES)
    for edge in ground_edges:
        for vertex in edge:
            glVertex3fv(ground_verticies[vertex])
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
#Setting up the gameplay loop
pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL)
gluPerspective(45, (800/600), 0.5, 50.0)
glTranslatef(0.0,0.0, -5)
Highscore=0

#Gameplay loop
def game_loop():
    #Skybox vars
    cx = 0
    cy = 0
    cz = 0 
    GameOver=0
    
    #Player vars
    sx = 0
    sy = 0#-0.01
    sz = -10   
    anglep = 0
    speed = 0.1
    
    #Projectile vars
    distance=0
    pspeed=0.1
    wangle=0
    px=0
    py=0
    pz=-10
    setUp = True
    
    #Grub points
    gx=[0,0,0,0,0,0,0]
    gy=[-7,-7,-7,-7,-7,-7,-7]
    grad=0.5
    
    #Box1 vars
    CX = 7.5
    CY = 5.5
    
    #Timer vars
    start_ticks=pygame.time.get_ticks()
    time_elapsed=0
    wave = 1;
    
    #TICKS PER FRAME
    clock.tick(60)
    elapDivide = 565
    
    #HUD and gameplay vars
    score=-6
    redo=0
    freeze = False
    gameExit = False  
    global Highscore
    
    #Enemy vars
    ez=-10
    ex=[0,0,0,0,0,0,0]
    ey=[0,0,0,0,0,0,0]
    etype=["","","","","","",""]
    ehits=[1,1,1,1,1,1,1]
    bugs=["Mosquito","Beetle","GrenadeBug","RocketBug"]
    bughits=[1,3,1,1]
    espeed=[0.04,0.02,0.03,0.01]
    erad=0.8
    esize=0.05
    bbool=[1,1,1,1,1,1,1]
    bway=[-1,-1,-1,-1,-1,-1,-1]
    #Explosion attack
    xrad=0.8
    xbool=0
    xx=[14,14,14,14,14,14,14]
    xy=[14,14,14,14,14,14,14]
    xadd=0
    xhold=0
    maxE=5
    ex_change=[0,0,0,0,0,0,0]
    ey_change=[0,0,0,0,0,0,0]
    
    #Loads the bounding box texture.
    box_texID = load_texture('Web.jpg')
    
    #Input vars
    pos = pygame.Vector2(0, 0)
    move_map = {pygame.K_a: pygame.Vector2(-speed, 0),
            pygame.K_d: pygame.Vector2(speed, 0),
            pygame.K_w: pygame.Vector2(0, speed),
            pygame.K_s: pygame.Vector2(0, -speed)}
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
            #This takes in input for when the player shoots.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    anglep=0
                    wangle=90
                    distance=pspeed
                    shoot_sound.play()
                elif event.key == pygame.K_DOWN:
                    anglep=180
                    wangle=-90
                    distance=pspeed
                    shoot_sound.play()
                elif event.key == pygame.K_LEFT:
                    anglep=90
                    wangle=-180
                    distance=pspeed
                    shoot_sound.play()
                elif event.key == pygame.K_RIGHT:
                    anglep=-90
                    wangle=0
                    distance=pspeed
                    shoot_sound.play()
                    
            elif event.type == pygame.KEYUP:
                #Pauses the game
                if event.key == pygame.K_RETURN and GameOver == 0:
                    freeze = not freeze
                #Exits the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                #Resets the game
                if event.key == pygame.K_r:
                    time_elapsed = 0
                    gameExit = True
                    game_loop()
                    
            #This text is displayed when the game is paused. 
            if(GameOver != 1):
                drawText(320, 300, "Paused", 60)
                    
        #Beginning of Freeze loop that can pause game.    
        if(freeze == False):
            #Handles Player Movement
            pressed = pygame.key.get_pressed()
            move_vector = pygame.Vector2(0, 0)
            #Moves the player
            for m in (move_map[key] for key in move_map if pressed[key]):
                move_vector += m
                
            if move_vector.length() > 0:
                move_vector.normalize_ip()
                
            move_vector *= speed
            
            pos +=move_vector
                    
            clock.tick(60)
            
            #Variables for player movement
            sx = pos.x
            sy = pos.y
            
            #Collision for border
            if sx >= CX:
                pos.x -=speed
            if sx <= -CX:
                pos.x +=speed
                
            if sy >= CY:
                pos.y -=speed
            if sy <= -CY:
                pos.y +=speed
                
            sz += 0
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            #Environment Box
            glPushMatrix()
            cxx=2.2
            cyy=1.6
            glTranslatef(cx, cy, cz)
            glScalef(cxx,cyy,1)
            glRotatef(-90, 0.0, 0.0, 1.0)
            glBindTexture(GL_TEXTURE_2D, box_texID)
            Box()
            glPopMatrix()
            
            #Player
            glPushMatrix()
            glTranslatef(sx, sy, sz)
            glRotatef(anglep, 0.0, 0.0, 1.0)
            glRotatef(90, 0.0, 0.0, 1.0)
            glRotatef(90, 1.0, 0.0, 0.0)
            glRotatef(-90, 0.0, 1.0, 0.0)
            glScalef(esize, esize, esize)
            enemy("Widow")
            glPopMatrix()
            
            #Projectiles
            glPushMatrix()
            glColor3f(255.0, 255.0, 255.0)
            #Projectile boundaries.
            if distance > 0:
                px=(distance*math.cos(math.pi/180.0*wangle))
                py=(distance*math.sin(math.pi/180.0*wangle))
                if distance < 14:
                    if(wangle==90):#Up
                        px=sx
                        py+=sy
                        pz=sz
                        glTranslatef(px, py, pz)
                    elif(wangle==-90):#Down
                        px=sx
                        py+=sy
                        pz=sz
                        glTranslatef(px, py, pz)
                    elif(wangle==-180):#Left
                        px+=sx
                        py=sy
                        pz=sz
                        glTranslatef(px, py, pz)
                    elif(wangle==0):#Right
                        px+=sx
                        py=sy
                        pz=sz
                        glTranslatef(px, py, pz)
                    glScalef(0.2, 0.2, 0.2)
                    Cube()
                    distance = distance + 0.5
                else:
                    distance = 0
                    pz=-9
                    px=0
                    py=0
                    glTranslatef(px, py, pz)
            glPopMatrix()
            
            #Enemy 1
            i = 0
            while i <= maxE:
                glPushMatrix()
                #Behavior per enemy
                if etype[i]=="Mosquito":#Chase player
                    if ex[i]>sx:
                        ex[i] -=espeed[0]
                    elif ex[i]<sx:
                        ex[i] +=espeed[0]
                    if ey[i]>sy:
                        ey[i] -=espeed[0]
                    elif ey[i]<sy:
                        ey[i] +=espeed[0]
                if etype[i]=="Beetle":#Eat points
                    j = 0
                    while j <= 5:
                        if gy[j] > -7:
                            if ex[i]>gx[j]:
                                ex[i] -=espeed[1]
                            elif ex[i]<gx[j]:
                                ex[i] +=espeed[1]
                            if ey[i]>gy[j]:
                                ey[i] -=espeed[1]
                            elif ey[i]<gy[j]:
                               ey[i] +=espeed[1]
                            distb = math.sqrt((ex[i] - gx[j])**2 + (ey[i] - gy[j])**2)
                            if distb <= grad*2:
                                gx[j]=0
                                gy[j]=-7
                            break
                        j=j+1
                if etype[i]=="GrenadeBug":#Explodes and gets u and enemies
                    if bbool[i]==1:
                        ex[i] +=espeed[2]
                    elif bbool[i]==0:
                        ex[i] -=espeed[2]
                    if ex[i]>9:
                        ex[i] -=espeed[2]
                        ey[i] +=bway[i]
                        bbool[i]=0
                    elif ex[i]<-9:
                        ex[i] +=espeed[2]
                        ey[i] +=bway[i]
                        bbool[i]=1
                    if ey[i]>6:
                        bway[i]=-1
                        ey[i] +=bway[i]
                        ex[i] -=espeed[2]
                    elif ey[i]<-6:
                        bway[i]=1
                        ey[i] +=bway[i]
                        ex[i] -=espeed[2]
                if etype[i]=="RocketBug":#Fast Unpredictable
                    if ex[i] >= CX:
                        ex_change[i] -=espeed[3]
                    if ex[i] <= -CX:
                        ex_change[i] +=espeed[3]
                        
                    if ey[i] >= CY:
                        ey_change[i] -=espeed[3]
                    if ey[i] <= -CY:
                        ey_change[i] +=espeed[3]
                    
                    ex[i] += ex_change[i]
                    ey[i] += ey_change[i]
                #Check collision with Player
                dist = math.sqrt((sx - ex[i])**2 + (sy - ey[i])**2)
                if dist <= erad and round(((pygame.time.get_ticks()-start_ticks)/1000)-redo,3) > 1:
                    GameOver=1
                #Projectile hit enemy?
                distw = math.sqrt((px - ex[i])**2 + (py - ey[i])**2)
                #Check if explode any enemies
                distE = math.sqrt((ex[i] - xx[xhold])**2 + (ey[i] - xy[xhold])**2)
                if distw <= erad and pz==sz or distE <= xrad:
                    if distE <= xrad:
                        score+=2
                    ehits[i]-=1
                    if ex[0]!=0 and ex[1]!=0 and ex[2]!=0 and ex[3]!=0 and ex[4]!=0 and ex[5]!=0:
                        distance=0
                        pz=-9
                    if ehits[i] <= 0 and etype[i]=="GrenadeBug":#Activate explosion
                        xbool=1
                        xx[i]=ex[i]
                        xy[i]=ey[i]
                        xhold=i
                    if ehits[i] <= 0:
                        #Drop point
                        gx[i]=ex[i]
                        gy[i]=ey[i]
                        
                        ex_change[i]=0.01
                        ey_change[i]=0.01
                        #Random spawn point for enemy. 
                        choice=random.randint(1, 4)
                        if choice==1:
                            ex[i] = random.randint(-8, 8)
                            ey[i] = 6
                        if choice==2:
                            ex[i] = 9
                            ey[i] = random.randint(-5, 5)
                        if choice==3:
                            ex[i] = random.randint(-8, 8)
                            ey[i] = -6
                        if choice==4:
                            ex[i] = -9
                            ey[i] = random.randint(-5, 5)
                        #What type of enemy 0Mos 1Beet 2Bomb 3Bug
                        randBug=random.randint(0, 9)
                        if randBug>=4 or i==0:
                            randBug=0
                        etype[i]=bugs[randBug]
                        ehits[i]=bughits[randBug]
                glTranslatef(ex[i], ey[i], ez)
                glRotatef(90, 0.0, 0.0, 1.0)
                glRotatef(90, 1.0, 0.0, 0.0)
                glRotatef(-90, 0.0, 1.0, 0.0)
                glScalef(esize, esize, esize)
                enemy(etype[i])
                glPopMatrix()
                i=i+1
            
            #Grenade Bug explosion if EnemyDefeated=GernadeBug
            if xbool==1:
                glPushMatrix()
                glColor3f(1,0,0)
                glTranslatef(xx[xhold],xy[xhold],sz)
                xrad+=xadd
                glScalef(xrad,xrad,0.2)
                xadd+=0.01
                
                #Check collision with Player
                distE = math.sqrt((sx - xx[xhold])**2 + (sy - xy[xhold])**2)
                if distE <= xrad:
                    GameOver=1 
                    
                #Check if GernadeBug explode any enemies
                if xrad < 2.8:
                    Sphere()
                else:
                    xx[xhold]=14
                    xy[xhold]=14
                    glTranslatef(xx[xhold],xy[xhold],sz)
                    xrad=0.8
                    xadd=0
                    Sphere()
                    xbool=0
                glPopMatrix()
            
            #Points to collect
            i = 0
            while i <= maxE:
                glPushMatrix()
                glColor3f(1,0,0)
                distg = math.sqrt((sx - gx[i])**2 + (sy - gy[i])**2)
                if distg <= grad:
                    score+=1
                    gx[i]=0
                    gy[i]=-7
                    if(score > 0):
                        collect_sound.play()
                glTranslatef(gx[i], gy[i], sz)
                glRotatef(0, 0.0, 0.0, 1.0)
                gsize=0.6
                glScalef(gsize, gsize, gsize)
                Tri()
                glPopMatrix()
                i=i+1
            #Score display 
            drawText(320, 550, "Score: "+str(score), 45)
            drawText(5, 570, "High Score: "+str(Highscore), 25)
            
            #Controls
            drawText(0, 0, "WASD=Move, Arrows=Shoot, ENTER=Pause, R=Restart ESC=Exit", 30)
            
            #Wave Number
            drawText(500,565,"Wave: "+str(wave), 30)
            
            #Wave Timer
            clock.tick(60)
            time_elapsed += clock.get_time()
            
            #Check if enemy speed should increase with wave number. 
            if(time_elapsed/elapDivide)-redo < 60.000:
                drawText(630,565,"Time: "+str(round((time_elapsed/elapDivide)-(redo),3)),30)
            else:
                redo=redo+60.000
                Upspeed=0.02
                espeed[0]+=Upspeed
                espeed[1]+=Upspeed
                espeed[2]+=Upspeed
                espeed[3]+=0.01
                pspeed+=Upspeed
                speed+=Upspeed
                wave+=1
            #End of Freeze
            
        #Checks if Game Over has occured or not.
        if GameOver==0:
            scoreSet=score
        if GameOver==1:
            scoreSet=score
            drawText(150, 300, "Game Over Score="+str(scoreSet), 60)
            drawText(280, 200, "R to Retry", 60)
            time_elapsed = 0
            if(Highscore < score):
                Highscore = score
            freeze = True
        pygame.display.flip()
        pygame.time.wait(10)
        
        #This helps set the game up properly(projectile placement)
        if(setUp == True):
            pz=-9
            setUp = False

while True:
    try:
        game_loop()
    except pygame.error:
        break