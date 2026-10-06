alien = Actor('alien')
alien.pos = 10, 10

def draw():
    screen.clear()
    alien.draw()

def update():
    alien.x += 1
    if alien.left > WIDTH:
        alien.right = pgzero