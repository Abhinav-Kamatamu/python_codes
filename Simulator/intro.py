import pygame,time
pygame.init()
win = pygame.display.set_mode((600,600))



def init():
    global win
    win.fill((0, 0, 0))
    redraw()
    pygame.display.update()
    time.sleep(3)
    fade = pygame.Surface((600,600))
    fade.fill((255,255,255))
    for alpha in range(0,100):
        fade.set_alpha(alpha)
        win.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)
        pygame.display.update()



def redraw():
    win.fill((0, 0, 0))
    _type_ = pygame.font.Font('freesansbold.ttf', 100)
    text = _type_.render('Simulation', True, (255,0,0))
    textrect = text.get_rect()
    textrect.topleft = (30,230)
    win.blit(text, textrect)

init()