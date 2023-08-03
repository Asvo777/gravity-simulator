import pygame, math, sys

pygame.init()
pygame.display.set_caption("Gravity Simulator")
icon = pygame.image.load("gravity-simulator-icon.png")
pygame.display.set_icon(icon)

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
time = pygame.time.Clock()
x,y = pygame.mouse.get_pos()

G = 3
start_simulation = False
animation_playing = False

class Planet:
    def __init__(self, color, x, y, mass = 10, vel_x = 0, vel_y = 0):
        self.color = color
        self.mass = mass
        self.radius = (mass * 3 / 4 * math.pi)**(1/3)
        # Position
        self.pos_x = x
        self.pos_y = y
        # Velocity
        self.vel_x = vel_x
        self.vel_y = vel_y
        # Acceleration
        self.acc_x = 0
        self.acc_y = 0

    def draw_planet(self):
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)
        print(planets.index(self))

    def calculate_acceleration(self, other):
        # Distance between both planets
        dx = abs(self.pos_x - other.pos_x)
        dy = abs(self.pos_y - other.pos_y)
        distance = math.sqrt(dx**2 + dy**2)
        
        # Cancel gravity if the planets are too near each other
        if distance > self.radius * 5:
            try:
                # Gravitational acceleration formula
                acceleration = G * other.mass / distance**2
                # Find the value of the angle formed by the bottom of the screen and the line connecting the two planets 
                angle = math.asin(dy/distance)
                # Calculate acceleration for each direction
                if self.pos_x < other.pos_x:
                    acc_x = math.cos(angle) * acceleration
                elif self.pos_x > other.pos_x:
                    acc_x = - math.cos(angle) * acceleration
                else:
                    acc_x = 0

                if self.pos_y < other.pos_y:
                    acc_y = math.sin(angle) * acceleration
                elif self.pos_y > other.pos_y:
                    acc_y = - math.sin(angle) * acceleration
                else:
                    acc_y = 0


                return acc_x, acc_y
            except ZeroDivisionError:
                return self.acc_x, self.acc_y
        else:
            return self.acc_x, self.acc_y

    def change_position(self, other):
        self.acc_x, self.acc_y = self.calculate_acceleration(other)

        self.vel_x += self.acc_x
        self.vel_y += self.acc_y

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        
    @staticmethod
    def detect_collision(planet1, planet2):
        # Collison is detected only when the center of a planet is touched
        collision_in_x = planet1.pos_x + planet1.radius >= planet2.pos_x and planet1.pos_x - planet1.radius <= planet2.pos_x
        collision_in_y = planet1.pos_y + planet1.radius >= planet2.pos_y and planet1.pos_y - planet1.radius <= planet2.pos_y
        
        if collision_in_x and collision_in_y:
            return True
        else:
            return False

    @staticmethod
    # Create a new planet originating from the two colliding planets
    def form_planet_from_impact(parent1, parent2):
        
        # Calculate new planet mass
        new_planet_mass = parent1.mass + parent2.mass

        # Calculate the new planet position depending on average positon of the parents and their masses
        new_planet_x = (parent1.pos_x * parent1.mass + parent2.pos_x * parent2.mass) / (2 * (new_planet_mass / 2))
        new_planet_y = (parent1.pos_y * parent1.mass + parent2.pos_y * parent2.mass) / (2 * (new_planet_mass / 2))

        # Momentum for x-axis
        p1_x = parent1.mass * parent1.vel_x
        p2_x = parent2.mass * parent2.vel_x

        # Momentum for y-axis
        p1_y = parent1.mass * parent1.vel_y
        p2_y = parent2.mass * parent2.vel_y
        
        # Calculate new planet velocity for x-axis
        new_planet_vel_x = (p1_x + p2_x) / new_planet_mass

        # Calculate new planet velocity for y-axis
        new_planet_vel_y = (p1_y + p2_y) / new_planet_mass

        # Create the new planet
        print(f"x: {new_planet_x}, y: {new_planet_y}, mass: {new_planet_mass}, vel x: {new_planet_vel_x}, vel y: {new_planet_vel_y}")
        return Planet("yellow", new_planet_x, new_planet_y, new_planet_mass, new_planet_vel_x, new_planet_vel_y)

class Button:
    # Buttons !(need to be updated)!
    def __init__(self):
        self.play_button_surface = pygame.image.load("img/play-button.png").convert_alpha()
        self.play_button_unclick_surface = pygame.image.load("img/play-button-unclick.png").convert_alpha()
        self.play_button_rect = self.play_button_surface.get_rect(center = (screen_width - 100, 30))
        # Start button is the play buttom slighty moved to the right to take Stop button place (because there is no need for Stop button when simulation is not started)
        self.start_button_rect = self.play_button_surface.get_rect(center = (screen_width - 40, 30))

        self.pause_button_surface = pygame.image.load("img/pause-button.png").convert_alpha()
        self.pause_button_unclick_surface = pygame.image.load("img/pause-button-unclick.png").convert_alpha()
        self.pause_button_rect = self.pause_button_surface.get_rect(center = (screen_width - 100, 30))

        self.stop_button_surface = pygame.image.load("img/stop-button.png").convert_alpha() 
        self.stop_button_unclick_surface = pygame.image.load("img/stop-button-unclick.png").convert_alpha()
        self.stop_button_rect = self.stop_button_surface.get_rect(center = (screen_width - 40, 30))

    def isButtonHovered(self, button_rect):
        x,y = pygame.mouse.get_pos()
        if (button_rect.collidepoint((x,y))):
            return True
        else:
            return False

    def displayButton(self, button):
        if button == "start":
            if (self.isButtonHovered(self.start_button_rect)):
                screen.blit(self.play_button_surface, self.start_button_rect)
            else:
                screen.blit(self.play_button_unclick_surface, self.start_button_rect)

        if button == "play":
            if (self.isButtonHovered(self.play_button_rect)):
                screen.blit(self.play_button_surface, self.play_button_rect)
            else:
                screen.blit(self.play_button_unclick_surface, self.play_button_rect)

        elif button == "pause":
            if (self.isButtonHovered(self.pause_button_rect)):
                screen.blit(self.pause_button_surface, self.pause_button_rect)
            else:
                screen.blit(self.pause_button_unclick_surface, self.pause_button_rect)

        elif button == "stop":
            if (self.isButtonHovered(self.stop_button_rect)):
                screen.blit(self.stop_button_surface, self.stop_button_rect)
            else:
                screen.blit(self.stop_button_unclick_surface, self.stop_button_rect)

        


btn = Button()
planets = []
PLANETANIMATE = pygame.USEREVENT
pygame.time.set_timer(PLANETANIMATE, 100)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if start_simulation:
                if animation_playing:
                    if btn.stop_button_rect.collidepoint((x,y)):
                        planets = []
                        start_simulation = False
                        animation_playing = False

                    elif btn.pause_button_rect.collidepoint((x,y)):
                        animation_playing = False
                else:
                    if btn.play_button_rect.collidepoint((x,y)) and not animation_playing:
                        animation_playing = True

                    elif btn.stop_button_rect.collidepoint((x,y)):
                        planets = []
                        start_simulation = False
                        animation_playing = False
                    
                    elif not animation_playing:
                        new_planet = Planet("yellow", x, y)
                        planets.append(new_planet)
            else:
                if btn.start_button_rect.collidepoint((x,y)):
                    start_simulation = True
                    animation_playing = True

                else:
                    new_planet = Planet("yellow", x, y)
                    planets.append(new_planet)

        if event.type == PLANETANIMATE and animation_playing:
            # Calculate acceleration for each planet
            for planet in planets:
                for other_planet in planets:
                    # Not allow calculation with itself 
                    if other_planet != planet:
                        planet.change_position(other_planet)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        for first_planet in planets:
            for second_planet in planets:
                if (Planet.detect_collision(first_planet, second_planet) and first_planet != second_planet):
                    new_planet = Planet.form_planet_from_impact(first_planet, second_planet)
                    if first_planet in planets:
                        planets.remove(first_planet)
                    if second_planet in planets:
                        planets.remove(second_planet)

                    planets.append(new_planet)
                    print(f"Collision: {len(planets)}")

    screen.fill("black")

    for planet in planets:
        planet.draw_planet()

    # If simulation started...
    if start_simulation:
        # Show pause button if animation is playing
        if animation_playing:
            btn.displayButton("pause")

        # Show play button if animation is paused
        else:
            btn.displayButton("play")
        # Show stop button to restart        
        btn.displayButton("stop")
    # If simulation not started...
    if not start_simulation:
       # Show only the start button (a play button moved to the right)
       btn.displayButton("start")
    
    pygame.display.update()
    time.tick(50)
