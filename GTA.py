from ursina import *
import random

app = Ursina()
window.color = color.rgb32(70,70,75)
camera.orthographic = True
camera.fov = 14

def na_rua(x,y):
    return abs(x % 6 - 3) < 1 or abs(y % 6 - 3) < 1

for x in range(-5,6):
    for y in range(-5,6):
        cor = color.hsv(random.uniform(0,360), 0.3, 0.8)
        Entity(model='quad', x=x*6, y=y*6, color=cor, scale=4)

jogador = Entity(model='circle', color=color.orange, scale=0.9, x=3,y=3, z=-1)

def mover(e, dx, dy):
    if na_rua(e.x + dx, e.y):
        e.x += dx
    if na_rua(e.x, e.y + dy):
        e.y += dy

carros = []
for _ in range(16):
    cor  = color.hsv(random.uniform(0,360), 0.8, 0.9)
    giro = random.choice([0,90,180,270])
    c = Entity(model='quad', scale=(1.4,0.8), z=-0.5, color=cor, rotation_z=giro)
    Entity(parent=c, model='quad',color=color.black66,x=0.2, scale=(0.15,0.8))
    rua = random.randint(-5,4) * 6 + 3
    p = random.uniform(-30,30)
    c.position = (rua, p) if giro % 180 == 0 else (rua, p)
    c.position += c.down * 0.5
    carros.append(c)

policia = Entity(model='quad', color = color.white, scale=(1.4,0.8), x=9, y=3, z=-0.6)

sirene = Entity(parent=policia, model = 'quad',z=-0.1, scale=(0.3, 0.9))

aviso = Text('', scale=4, origin=(0,0), y=0.3, color=color.red)

relogio = 0

def update():
    global relogio
    vel = 5 * time.dt
    mover(jogador, held_keys['d'] * vel - held_keys['a'] * vel, held_keys['w'] * vel - held_keys['s'] * vel)
    camera.x, camera.y = jogador.x, jogador.y
    for c in carros:
        c.position += c.right * 7 * time.dt
        c.x = (c.x + 33) % 60 - 33
        c.y = (c.y + 33) % 60 - 33
    relogio += time.dt
    piscar = int(relogio * 6) % 2
    sirene.color = color.red if piscar else color.blue
    rumo = jogador.position - policia.position
    rumo = rumo.normalized() * 4.9 * time.dt
    mover(policia, rumo.x, rumo.y)
    if distance_2d(policia, jogador) < 0.1:
        aviso.text = 'PRESO!'
        application.pause()

app.run()