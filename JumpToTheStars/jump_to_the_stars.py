import pygame
from pygame.locals import *
import sys
import random

WIDTH = 700
HEIGHT = 800
# Setare elemente de grafica
pygame.init()

# Culori
PINK = (255, 115, 255)
BLUE = (100, 190, 255)
GRAY = (55, 55, 55)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURQ = (35, 140, 155)

# Incarcare imagini pentru grafica, setare fereastra program, setare font
window = pygame.display.set_mode((WIDTH, HEIGHT))
astronaut = pygame.image.load("images/astr.png")
static_step = pygame.image.load("images/static_step.png")
moving_step = pygame.image.load("images/moving_step.png")
background = pygame.image.load("images/galaxy.png")
rocket_plus = pygame.image.load("images/rocket_plus.png")
rocket_extra = pygame.image.load("images/rocket_extra.png")
planet = pygame.image.load("images/planet2.png")
menu_bg = pygame.image.load("images/menu.png")
about_bg = pygame.image.load("images/about_bg.png")

font = pygame.font.SysFont("freesansbold.ttf", 60)
FONT = pygame.font.Font("freesansbold.ttf", 50)
FONT_TEXT_BUTON = pygame.font.Font("freesansbold.ttf", 30)

# Butoane
t1 = FONT.render("START", True, WHITE)
t2 = FONT.render("ABOUT", True, WHITE)
t3 = FONT.render("QUIT", True, WHITE)
t4 = FONT.render("BACK", True, WHITE)
t5 = FONT.render("REPLAY", True, WHITE)

# Pozitia butoanelor(left, top, width, height)
start = pygame.Rect(400, 250, 200, 50)
option = pygame.Rect(400, 330, 200, 50)
quit = pygame.Rect(400, 410, 200, 50)
back = pygame.Rect(200, 300, 300, 80)
replay = pygame.Rect(200, 200, 300, 80)

text_START = "START"
text_ABOUT = "ABOUT"
text_QUIT = "QUIT"
text_BACK = "BACK"
text_REPLAY = "REPLAY"

# Liste de structuri pentru butoane folosite pentru a seta butoanele in interfata
buttons = [[t1, start, GRAY, text_START],
           [t2, option, PINK, text_ABOUT],
           [t3, quit, BLUE, text_QUIT]]

about_buttons = [[t4, back, GRAY, text_BACK]]
replay_buttons = [[t5, replay, TURQ, text_REPLAY]]

steps = []
astronaut_position = [WIDTH/2 - 50, HEIGHT-300]
jumping = False
speed = 4
go_to_next = False
jumping_speed = 2


def print_score(score):
    """
        afisare scor pe ecran
    """
    score1 = font.render("Score: " + str(score), True, (0, 0, 0))
    window.blit(score1, (15, 15))


def set_game_background():
    """
        setare background si elemente de grafica
    """
    pygame.display.set_caption('Jump To The Stars')
    window.fill((100, 160, 200))
    window.blit(background, [0, 0])
    window.blit(planet, [100, 10])
    window.blit(astronaut, astronaut_position)


def about_section():
    """
        Aceasta functie are rolul de a genera fereastra pentru sectiunea About
    """
    while (True):
        # Elemente de grafica pentru fereastra About
        pygame.display.set_caption('Jump To The Stars')
        window.fill(WHITE)
        window.blit(about_bg, [0, 0])
        pygame.draw.rect(window, TURQ, back)

        # Text in fereastra About
        text_surf_about = FONT.render("Version: 1.2.0.7", True, (100, 100, 100))
        text_rect_about = text_surf_about.get_rect(center=(WIDTH / 2, HEIGHT - 100))
        window.blit(text_surf_about, text_rect_about)

        # Text buton BACK
        text_surf_back, text_rect_back = text_obj("BACK", FONT_TEXT_BUTON)
        text_rect_back.center = ((200 + (300 / 2)), (300 + (80 / 2)))
        window.blit(text_surf_back, text_rect_back)
        pygame.display.update()

        # Verificare buton Close si buton Back
        for elem in pygame.event.get():
            if elem.type == pygame.QUIT:
                sys.exit()
            if elem.type == pygame.MOUSEBUTTONDOWN:
                if elem.button == 1:
                    back_BUTTON = about_buttons[0][1]
                # Daca butonul Back este actionat, trimite in fereastra Menu
                if back_BUTTON.collidepoint(elem.pos):
                    menu()


def quit_game():
    """
        Aceasta functie are rolul de a inchide programul
    """
    for elem in pygame.event.get():
        if elem.type == pygame.QUIT:
            sys.exit()


def text_obj(text, font):
    """
        Aceasta functie are rolul de a randa textul dat ca parametru
    """
    text_surface = font.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()


def play_game(score, jumping, go_to_next, game_over):
    global jumping_speed
    # Generare platforme
    for i in range(12):
        step = [random.randint(20, WIDTH-100), i * 75]
        steps.append(step)
    # Pozitia primei platforme
    steps[11][0] = WIDTH/2 - 50

    while True:
        # Setare background si elemente de grafica
        set_game_background()
        if astronaut_position[1] >= HEIGHT:
            game_over = True

        # Game Over
        if game_over:
            # Animatie Game Over, avatarul cade
            if steps[0][1] >= -HEIGHT:
                for step in steps:
                    step[1] -= speed
            # Stare mesaj de Game Over
            pygame.draw.rect(window, TURQ, replay)
            text_surf_replay, text_rect_replay = text_obj("GAME OVER", FONT_TEXT_BUTON)
            text_rect_replay.center = ((100 + (500 / 2)), (200 + (80 / 2)))
            window.blit(text_surf_replay, text_rect_replay)

        # Afisare platforme statice
        for step in steps:
            if step[1] >= HEIGHT + 50:
                step[1] = 0
            window.blit(static_step, step)

        quit_game()
        pygame.event.get()
        key = pygame.key.get_pressed()

        if jumping_speed <= 2:
            jumping_speed = 2

        # Miscare pe axa orizontala in functie de tasta care este apasata(key left sau key right)
        if key[K_LEFT]:
            astronaut_position[0] -= speed
        if key[K_RIGHT]:
            astronaut_position[0] += speed
        pygame.display.update()

        if game_over:
            quit_game()
            # Animatia avatarului de a se ridica pana la jumatatea ecranului
            if astronaut_position[1] >= HEIGHT / 2:
                astronaut_position[1] -= 1
            else:
                pass
            continue

        # Miscarea avatarului pe axa verticala
        if jumping == False:
            if astronaut_position[1] >= HEIGHT:
                jumping = True
                jumping_speed = 10
            else:
                jumping_speed += 0.1
                astronaut_position[1] += jumping_speed
        else:
            if astronaut_position[1] <= HEIGHT / 2:
                jumping = False
                jumping_speed = 2
            else:
                jumping_speed -= 0.1
                astronaut_position[1] -= jumping_speed

        cnt = -1
        # Verificare coliziune intre avatar si platforme
        for step in steps:
            cnt += 1
            rect = pygame.Rect(step[0], step[1], static_step.get_width() - 10, static_step.get_height())
            player = pygame.Rect(astronaut_position[0], astronaut_position[1], astronaut.get_width() - 10,
                                 astronaut.get_height())
            if rect.colliderect(player) and speed and astronaut_position[1] < (step[1]):
                # Verifica daca este deasupra unei pltforme si o salveaza
                if astronaut_position[1] <= step[1] - 70:
                    collision_step = cnt
                    jumping = True
                    go_to_next = True

        # Treci la urmatoarea platforma
        if go_to_next:
            # Se coboara fiecare platforma pana cand platforma pe care a sarit ultima data ajunge la pozitia setata
            if steps[collision_step][1] <= HEIGHT - 150:
                score += 1
                for step in steps:
                    step[1] += speed
            else:
                go_to_next = False

        # Trecerea avatarului din partea stanga a ecranului in dreapta si viceversa
        if astronaut_position[0] < 0:
            astronaut_position[0] = WIDTH - 50
        if astronaut_position[0] > 700:
            astronaut_position[0] = 20
        pygame.display.update()

run_game = False
def menu():
    ok = False
    run_game = False
    while (ok != 1):
        # Elemente grafica pentru fereastra Meniu
        pygame.display.set_caption('Jump To The Stars')
        window.fill((255, 255, 255))
        window.blit(menu_bg, [0, 0])
        pygame.draw.rect(window, GRAY, start)
        pygame.draw.rect(window, PINK, option)
        pygame.draw.rect(window, BLUE, quit)

        # Text buton start
        text_surf_start, text_rect_start = text_obj("START", FONT_TEXT_BUTON)
        text_rect_start.center = ((400+(200/2)), (250+(50/2)))
        window.blit(text_surf_start, text_rect_start)

        # Text buton About
        text_surf_about, text_rect_about = text_obj("ABOUT", FONT_TEXT_BUTON)
        text_rect_about.center = ((400 + (200 / 2)), (330 + (50 / 2)))
        window.blit(text_surf_about, text_rect_about)

        # Text buton QUIT
        text_surf_quit, text_rect_quit = text_obj("QUIT", FONT_TEXT_BUTON)
        text_rect_quit.center = ((400 + (200 / 2)), (410 + (50 / 2)))
        window.blit(text_surf_quit, text_rect_quit)

        # Text fereastra Menu
        text_surf = FONT.render("Jump to the Stars", True, (100, 100, 100))
        text_surf1 = FONT.render("Game Menu", True, (200, 200, 200))
        text_rect = text_surf.get_rect(center=(WIDTH / 2, 90))
        text_rect1 = text_surf1.get_rect(center=(WIDTH/2, 150))
        window.blit(text_surf, text_rect)
        window.blit(text_surf1, text_rect1)
        pygame.display.update()

        # Verificare comanda butoane
        for elem in pygame.event.get():
            if elem.type == pygame.QUIT:
                sys.exit()

            if elem.type == pygame.MOUSEBUTTONDOWN:
                if elem.button == 1:
                    start_BUTTON = buttons[0][1]
                    about_BUTTON = buttons[1][1]
                    quit_BUTTON = buttons[2][1]
                    # Verificare comanda START si incepe jocul daca acest buton a afost apasat
                    if start_BUTTON.collidepoint(elem.pos):
                        ok = True
                        run_game = True
                        play_game(0, False, False, False)
                    # Verificare comanda ABOUT si trimitere catre aceasta fereastra
                    elif about_BUTTON.collidepoint(elem.pos):
                        about_section()
                    # Verificare comanda inchidere program
                    elif quit_BUTTON.collidepoint(elem.pos):
                        sys.exit()
                    else:
                        print("Invalid command.")
                    window.fill((100, 160, 200))

menu()
sys.exit()
