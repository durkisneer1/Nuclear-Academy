import pygame as pg
from pygame.locals import *

pg.init()
clock = pg.time.Clock()
WIDTH = 800
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Nuclear Academy')
pg.display.set_icon(pg.image.load('Data\icon.png'))

c_react = pg.image.load("Data\c_model.png").convert_alpha()
rod_model = pg.image.load("Data\Rods.png").convert_alpha()
press_model = pg.image.load('Data\press.png').convert_alpha()
core_model = pg.image.load('Data\chain.png').convert_alpha()
steam_model = pg.image.load('Data\steam.png').convert_alpha()
tp_idle = pg.image.load('Data\Toxic_idle.png').convert_alpha()
tp_hover = pg.image.load('Data\Toxic_hover.png').convert_alpha()
toxic_full = pg.transform.scale(pg.image.load('Data\Toxic_full.png').convert_alpha(), (500,500))
wp_idle = pg.image.load('Data\waste_idle.png').convert_alpha()
wp_hover = pg.image.load('Data\waste_hover.png').convert_alpha()
waste_full = pg.transform.scale(pg.image.load('Data\waste_full.png').convert_alpha(), (500,500))
cp_idle = pg.image.load('Data\converter_idle.png').convert_alpha()
cp_hover = pg.image.load('Data\converter_hover.png').convert_alpha()
conv_full = pg.transform.scale(pg.image.load('Data\conv_full.gif').convert(), (600,296))
cursor_img = pg.image.load('Data\cursor.png').convert_alpha()

green = (74,193,68)
darkgray = (100,100,100)

m_font = pg.font.Font('Data\Kenney Mini.ttf',82)
p_font = pg.font.Font('Data\Kenney Pixel.ttf',48)
t_font = pg.font.Font('Data\Daydream.ttf', 92)
st_font = pg.font.Font('Data\Daydream.ttf',56)
s_font = pg.font.Font('Data\Daydream.ttf',48)

pg.mouse.set_visible(False)
cursor_rect = cursor_img.get_rect()

class Button:
    def __init__(self, text, size, pos, font):
        self.rect = pg.Rect(pos, size)
        self.rect.center = self.rect.topleft
        self.text_surf = font.render(text, True, 'white')
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.color = darkgray    
    def draw(self):
        self.hover()
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, 'white', self.rect, 2)
        screen.blit(self.text_surf, self.text_rect)        
    def hover(self):
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.color = 'gray'
        else:
            self.color = darkgray

class Graphic:
    def __init__(self, tpos, tsize, bpos, img, ipos, model, pos, title):
        t_box = pg.Rect(tpos, tsize)
        t_box.center = t_box.topleft
        box = pg.Rect(bpos, (600,600))
        box.center = box.topleft
        esc_box = pg.Rect(0, HEIGHT, 330,35)
        esc_box.bottomleft = esc_box.topleft
        refresh(model, pos, title)
        pg.draw.rect(screen,'gray',box)
        pg.draw.rect(screen,'white',t_box)
        pg.draw.rect(screen,'white',esc_box)
        screen.blit(img,ipos)
        pg.draw.rect(screen,'black',box, 3)
        pg.draw.rect(screen,'black',t_box, 3)
        pg.draw.rect(screen,'black',esc_box, 3)
        esc = p_font.render("Press 'ESC' to Return", True, 'black')
        escRect = esc.get_rect()
        escRect.bottomleft = (10, HEIGHT)
        screen.blit(esc, escRect)

class Interactable:
    def __init__(self,x,y,idle, hover):
        self.idle_img = idle
        self.hover_img = hover
        self.image = idle
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.hover_img
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if not self.rect.collidepoint(pos):
            self.image = self.idle_img
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
tp = Interactable(WIDTH/2+30, 140, tp_idle, tp_hover)
wp = Interactable(10, 470, wp_idle, wp_hover)
cp = Interactable(225,500,cp_idle,cp_hover)

class Read:
    def __init__(self, G_pos, G_size, Model, M_pos, Text, T_pos, model, pos, title):
        running = True
        while running:
            Graphic(G_pos,G_size, (WIDTH/2,HEIGHT/2),Model,M_pos, model, pos, title)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            blit_text(screen, Text, T_pos, p_font, 'black')
            cursor_rect.topleft = pg.mouse.get_pos()
            screen.blit(cursor_img, cursor_rect)
            pg.display.update()

def blit_text(surface, text, pos, font, color):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

def refresh(model, pos, title):
    slide = title
    screen.blit(model, pos)
    blit_text(screen, slide, (5, 5), s_font, 'black')

r_text = "\
Dozens of control rods, large\n\
cylinders made of neutron-absorbing\n\
materials, suppress, or even halt, the\n\
rate of reaction for a cooler\n\
temperature or for safety measures."
p_text = "\
Serving as the\n\
boiler of the\n\
coolant system,\n\
the pressurizer is\n\
partially filled\n\
with vapor, creating\n\
a high density\n\
environment for the\n\
water in the coolant\n\
in order to prevent\n\
boiling within the\n\
core. It achieves\n\
this feat by\n\
acquiring a higher\n\
temperature than\n\
the core itself."
c_text = "\
A Uranium-235 atom absorbs a neutron\n\
and fissions into Barium-141 and\n\
Krypton-92. Because the lighter atoms\n\
don't need much energy to hold the\n\
nucleus together, energy is released\n\
as heat. This sparks a chain reaction."
s_text = "\
To cool down the\n\
coolant, an inlet\n\
lets in water from\n\
the cooling tower\n\
into the upper\n\
apparatus. This\n\
allows for the\n\
steam generation\n\
of the water and\n\
the cooling of the\n\
coolant. After the\n\
steam goes through\n\
a turbine to produce\n\
electricity, it is\n\
then sent back to\n\
the cooling tower."

h_text = "*Interactable"
w_text = "\
Waste produced in the past\n\
70 years could only fill\n\
10,000 cubic yards, around\n\
96% of it being recycled\n\
into fuel again and of the\n\
leftover 4%, 90% is not\n\
hazardous. This is because\n\
fuel is replenished only\n\
every 5 years."
cb_text = "\
While some may see this as\n\
a lot and therefor use it\n\
as an argument as to why\n\
nuclear energy production\n\
is harmful to our planet,\n\
need it be taken into\n\
consideration that coal\n\
plants accomplish this\n\
hourly."

t1_txt = "Very Low\nLevel Waste:\n58%"
t2_txt = "Low Level\nWaste:\n34%"
t3_txt = "Intermediate\nLevel Waste:\n9%"
t4_txt = "High Level Waste: 0.03%"
t_cite = "> Ripper, 2017"
w1_txt = "Natural\nGas:\n23.2%"
w2_txt = "Oil: 3.0%"
w3_txt = "Coal: 38.0%"
w4_txt = "Renewable:\n          9.3%"
w5_txt = "Nuclear:\n10.1%"
w6_txt = "Hydropower:\n15.8%"
w_cite = "> BP Statistical Review of World\n    Energy, 2019"

a_txt = "While the provided facts pose little to no assistance in what we, as citizens, \
can do to save\nour country's, or world's, future, there is one strong point that may motivate \
consumers to invest in nuclear: Gas prices. With fossil fuels inevitably becoming scarce in the near future, \
there's been research in the recent years conducting electrochemical energy conversion using hydrogen \
and oxygen, meaning zero carbon emission, unlike combustion which uses gasoline."

f_txt = "\
Hydrogen molecules leave positively\n\
charged protons in the anode.\n\
Electrons travel through the circuit\n\
and protons through the membrane to\n\
the cathode where they form water.\n\
This flow of electrons or electricity\n\
is the primary product of the fuel cell\n\
with pure water as the only byproduct."
f_cite = "> Intelligent Energy, 2020"

def menu():
    running = True
    while running:
        screen.fill(green)
        blit_text(screen, '> Created by Derrick Martinez', (7, HEIGHT-40), p_font, 'red')
        i_box = pg.Rect(WIDTH/2,HEIGHT/3-20,740,320)
        i_box.center = i_box.topleft
        pg.draw.rect(screen,'black',i_box)
        pg.draw.rect(screen,'white',i_box, 3)
        title = t_font.render('Nuclear', True ,'white')
        subtitle = st_font.render('Academy', True,'white')
        screen.blit(title, title.get_rect(center = (WIDTH/2,HEIGHT/4)))
        screen.blit(subtitle, subtitle.get_rect(center= (WIDTH/2,HEIGHT*(2/5))))
        mouse = pg.mouse.get_pos()
        start_button = Button('PLAY', (300,100), (WIDTH/2, HEIGHT-(HEIGHT/4)), m_font)
        start_button.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(mouse):
                    c_model()
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        cursor_rect.topleft = pg.mouse.get_pos()
        screen.blit(cursor_img, cursor_rect)
        pg.display.update()

def c_model():
    running = True
    while running:
        refresh(c_react, (0,0), "Nuclear Coolant System")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if rod.rect.collidepoint(mouse):
                    Read((WIDTH/2,HEIGHT/2+205),(600,190),rod_model,(100,150),r_text,(WIDTH/2-290, HEIGHT*(2/3)-20), c_react, (0,0), "Nuclear Coolant System")
                if press.rect.collidepoint(mouse):
                    Read((WIDTH/2+138,HEIGHT/2),(323,600),press_model,(100,100),p_text,(WIDTH/2-12, HEIGHT/8+5), c_react, (0,0), "Nuclear Coolant System")
                if fuel.rect.collidepoint(mouse):
                    Read((WIDTH/2,HEIGHT/2-190),(600,220),core_model,(100, 375), c_text,(WIDTH/2-290,HEIGHT/8), c_react, (0,0), "Nuclear Coolant System")
                if steam.rect.collidepoint(mouse):
                    Read((WIDTH/2-138,HEIGHT/2),(323,600),steam_model,(420,100),s_text,(WIDTH/2-290,HEIGHT/8+5), c_react, (0,0), "Nuclear Coolant System")
                if next.rect.collidepoint(mouse):
                    w_models()
        mouse = pg.mouse.get_pos()
        rod = Button('Control Rods', (225,50), (WIDTH/4-5,HEIGHT/3-25), p_font)
        rod.draw()
        press = Button('Pressurizer', (225,50), (WIDTH/2-35,HEIGHT/4-15), p_font)
        press.draw()
        fuel = Button('Core', (100,50), (WIDTH/4,HEIGHT*(3/4)-15), p_font)
        fuel.draw()
        steam = Button('Steam Generator', (300,50), (WIDTH*(3/4),HEIGHT/2+50), p_font)
        steam.draw()
        next = Button('> next...', (140,50), (WIDTH-70,HEIGHT-25), p_font)
        next.draw()      
        inst = p_font.render("Click a Button For More Info!", True, 'black')
        instRect = inst.get_rect()
        instRect.bottomleft = (10, HEIGHT)
        screen.blit(inst, instRect)
        cursor_rect.topleft = pg.mouse.get_pos()
        screen.blit(cursor_img, cursor_rect)
        pg.display.update()

def w_models():
    running = True
    while running:
        screen.fill(green)
        blit_text(screen, "Nuclear Waste Fun Facts", (5, 5), s_font, 'black')
        blit_text(screen, w_text, (15,HEIGHT/2-260), p_font, 'black')
        blit_text(screen, cb_text, (WIDTH/2-25,HEIGHT-330), p_font, 'black')
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if next.rect.collidepoint(mouse):
                    action()
        t_box = pg.Rect(WIDTH/2+95, 90, 230, 40)
        pg.draw.rect(screen,'white',t_box)
        pg.draw.rect(screen,'black',t_box, 3)
        blit_text(screen, h_text, (WIDTH/2+100,90), p_font, 'black')
        if tp.draw():
            toxic_read()
        if wp.draw():
            waste_read()
        next = Button('> next...', (140,50), (WIDTH-70,25), p_font)
        next.draw()
        cursor_rect.topleft = pg.mouse.get_pos()
        screen.blit(cursor_img, cursor_rect)
        pg.display.update()

def toxic_read():
    running = True
    while running:
        screen.fill(green)
        blit_text(screen, w_text, (15,HEIGHT/2-260), p_font, 'black')
        blit_text(screen, cb_text, (WIDTH/2-25,HEIGHT-330), p_font, 'black')
        screen.blit(tp_idle,(WIDTH/2+30, 140))
        t_box = pg.Rect(WIDTH/2+95, 90, 230, 40)
        pg.draw.rect(screen,'white',t_box)
        pg.draw.rect(screen,'black',t_box, 3)
        blit_text(screen, h_text, (WIDTH/2+100,90), p_font, 'black')
        Graphic((0,0),(0,0),(WIDTH/2,HEIGHT/2),toxic_full,(145,150), wp_idle, (10, 470), "Nuclear Waste Fun Facts")
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        blit_text(screen, t1_txt, (190,375), p_font, 'black')
        blit_text(screen, t2_txt, (450,330), p_font, 'black')
        blit_text(screen, t3_txt, (415,180), p_font, 'black')
        blit_text(screen, t4_txt, (250,115), p_font, 'black')
        blit_text(screen, t_cite, (110,655), p_font, 'black')
        cursor_rect.topleft = pg.mouse.get_pos()
        screen.blit(cursor_img, cursor_rect)
        pg.display.update()

def waste_read():
    running = True
    while running:
        screen.fill(green)
        blit_text(screen, w_text, (15,HEIGHT/2-260), p_font, 'black')
        blit_text(screen, cb_text, (WIDTH/2-25,HEIGHT-330), p_font, 'black')
        screen.blit(tp_idle,(WIDTH/2+30, 140))
        t_box = pg.Rect(WIDTH/2+95, 90, 230, 40)
        pg.draw.rect(screen,'white',t_box)
        pg.draw.rect(screen,'black',t_box, 3)
        blit_text(screen, h_text, (WIDTH/2+100,90), p_font, 'black')
        Graphic((0,0),(0,0),(WIDTH/2,HEIGHT/2),waste_full,(145,125), wp_idle, (10, 470), "Nuclear Waste Fun Facts")
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        blit_text(screen, w1_txt, (234,220), p_font, 'black')
        blit_text(screen, w2_txt, (165,355), p_font, 'black')
        blit_text(screen, w3_txt, (295,470), p_font, 'black')
        blit_text(screen, w4_txt, (460,390), p_font, 'black')
        blit_text(screen, w5_txt, (490,315), p_font, 'black')
        blit_text(screen, w6_txt, (405,220), p_font, 'black')
        blit_text(screen, w_cite, (110,620), p_font, 'black')
        cursor_rect.topleft = pg.mouse.get_pos()
        screen.blit(cursor_img, cursor_rect)
        pg.display.update()

def action():
    running = True
    while running:
        screen.fill(green)
        blit_text(screen, "Why Invest In Nuclear?", (5, 5), s_font, 'black')
        txt = pg.Rect(WIDTH/2, HEIGHT/2-80, 790,370)
        txt.center = txt.topleft
        pg.draw.rect(screen,'white',txt)
        pg.draw.rect(screen,'black',txt, 3)
        blit_text(screen, a_txt, (15,HEIGHT/2-260), p_font, 'black')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        if cp.draw():
            conv_read()
        cursor_rect.topleft = pg.mouse.get_pos()
        screen.blit(cursor_img, cursor_rect)
        pg.display.update()

def conv_read():
    running = True
    while running:
        screen.fill(green)
        txt = pg.Rect(WIDTH/2, HEIGHT/2-80, 790,370)
        txt.center = txt.topleft
        pg.draw.rect(screen,'white',txt)
        pg.draw.rect(screen,'black',txt, 3)
        blit_text(screen, a_txt, (15,HEIGHT/2-260), p_font, 'black')
        Graphic((WIDTH/2,HEIGHT-252),(600,304),(WIDTH/2,HEIGHT/2), conv_full,(100,100), cp_idle, (225,500), "Why Invest In Nuclear?")
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        blit_text(screen, f_txt, (WIDTH/2-290, HEIGHT/2), p_font, 'black')
        blit_text(screen, f_cite, (WIDTH-200,HEIGHT-75), p_font, 'black')
        cursor_rect.topleft = pg.mouse.get_pos()
        screen.blit(cursor_img, cursor_rect)
        pg.display.update()

if __name__ == "__main__":
    menu()