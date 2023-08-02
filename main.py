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

G = 2
start_simulation = False
animation_playing = False

class Planet:
    def __init__(self, color, x, y, mass = 10, vel_x = 0, vel_y = 0):
        self.color = color
        self.mass = mass
        self.radius = math.sqrt(mass / 3.1831 * math.pi)
        # Position
        self.pos_x = x
        self.pos_y = y
        # Velocity
        self.vel_x = vel_x
        self.vel_y = vel_y
        # Acceleration
        self.acc_x = 0
        self.acc_y = 0

    def main(self, other_planet):
        self.change_position(other_planet)
        self.detect_collision(other_planet)

    def draw_planet(self):
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)

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
        

    def detect_collision(self, other):
        # Collison is detected only when the center of the planett is touched
        collision_in_x = self.pos_x + self.radius >= other.pos_x and self.pos_x - self.radius <= other.pos_x
        collision_in_y = self.pos_y + self.radius >= other.pos_y and self.pos_y - self.radius <= other.pos_y
        if collision_in_x and collision_in_y:
            # Calculate velocity of the new formed planet
            self.form_planet_from_impact(other)
            print("Collision")
            # Destroy planets in collision
            if self in planets:
                planets.remove(self)
            if other in planets:
                planets.remove(other)

# --- IN PROGRESS ---
    def form_planet_from_impact(self, parent2):
    # Create a new planet originating from the two colliding planets
        parent1 = self

        # Calculate the new planet position
        new_planet_x = (parent1.pos_x + parent2.pos_x) / 2
        new_planet_y = (parent1.pos_y + parent2.pos_y) / 2

        # Momentum for x-axis
        p1_x = parent1.mass * parent1.vel_x
        p2_x = parent2.mass * parent2.vel_x

        # Momentum for y-axis
        p1_y = parent1.mass * parent1.vel_y
        p2_y = parent2.mass * parent2.vel_y
        
        # Calculate new planet mass
        new_planet_mass = parent1.mass + parent2.mass

        color = "yellow"
        if abs(parent1.mass - parent2.mass) == 10:
            color = "red"
            print(f"I am {self.mass} and {parent2.mass}")
            print(f"{parent1.mass} + {parent2.mass} = {new_planet_mass}kg")

        # Calculate new planet velocity for x-axis
        new_planet_vel_x = (p1_x + p2_x) / new_planet_mass

        # Calculate new planet velocity for y-axis
        new_planet_vel_y = (p1_y + p2_y) / new_planet_mass

        # Create the new planet
        new_planet = Planet(color, new_planet_x, new_planet_y, new_planet_mass, new_planet_vel_x, new_planet_vel_y)
        planets.append(new_planet)


# def detect_collision(self, other):
#         # Collison is detected only when the center of the planett is touched
#         collision_in_x = self.pos_x + self.radius >= other.pos_x and self.pos_x - self.radius <= other.pos_x
#         collision_in_y = self.pos_y + self.radius >= other.pos_y and self.pos_y - self.radius <= other.pos_y
#         if collision_in_x and collision_in_y:
#             # Calculate velocity of the new formed planet
#             self.form_planet_from_impact(other)
#             print("Collision")
#             # Destroy planets in collision
#             if self in planets:
#                 planets.remove(self)
#             if other in planets:
#                 planets.remove(other)


# Buttons !(need to be updated)!
play_button_surface = pygame.image.load("img/play-button.png").convert_alpha()
play_button_unclick_surface = pygame.image.load("img/play-button-unclick.png").convert_alpha()
play_button_rect = play_button_surface.get_rect(center = (screen_width - 100, 30))
# Start button is the play buttom slighty moved to the right to take Stop button place (because there is no need for Stop button when simulation is not started)
start_button_rect = play_button_surface.get_rect(center = (screen_width - 40, 30))

pause_button_surface = pygame.image.load("img/pause-button.png").convert_alpha()
pause_button_unclick_surface = pygame.image.load("img/pause-button-unclick.png").convert_alpha()
pause_button_rect = pause_button_surface.get_rect(center = (screen_width - 100, 30))

stop_button_surface = pygame.image.load("img/stop-button.png").convert_alpha() 
stop_button_unclick_surface = pygame.image.load("img/stop-button-unclick.png").convert_alpha()
stop_button_rect = stop_button_surface.get_rect(center = (screen_width - 40, 30))

def isButtonHovered(button_rect):
    x,y = pygame.mouse.get_pos()
    if (button_rect.collidepoint((x,y))):
        return True
    else:
        return False

def displayButton(button):
    if button == "start":
        if (isButtonHovered(start_button_rect)):
            screen.blit(play_button_surface, start_button_rect)
        else:
            screen.blit(play_button_unclick_surface, start_button_rect)

    if button == "play":
        if (isButtonHovered(play_button_rect)):
            screen.blit(play_button_surface, play_button_rect)
        else:
            screen.blit(play_button_unclick_surface, play_button_rect)

    elif button == "pause":
        if (isButtonHovered(pause_button_rect)):
            screen.blit(pause_button_surface, pause_button_rect)
        else:
            screen.blit(pause_button_unclick_surface, pause_button_rect)

    elif button == "stop":
        if (isButtonHovered(stop_button_rect)):
            screen.blit(stop_button_surface, stop_button_rect)
        else:
            screen.blit(stop_button_unclick_surface, stop_button_rect)

        



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
                    if stop_button_rect.collidepoint((x,y)):
                        planets = []
                        start_simulation = False
                        animation_playing = False

                    elif pause_button_rect.collidepoint((x,y)):
                        animation_playing = False
                else:
                    if play_button_rect.collidepoint((x,y)) and not animation_playing:
                        animation_playing = True

                    elif stop_button_rect.collidepoint((x,y)):
                        planets = []
                        start_simulation = False
                        animation_playing = False
                    
                    elif not animation_playing:
                        new_planet = Planet("yellow", x, y)
                        planets.append(new_planet)
            else:
                if start_button_rect.collidepoint((x,y)):
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
                        planet.main(other_planet)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # for planet in planets:
        #     for p in planets:
        #         if (planet.detect_collision(p)):
        #             pygame.quit()
        #             sys.exit()
    
    screen.fill("black")

    for planet in planets:
        planet.draw_planet()

    # If simulation started...
    if start_simulation:
        # Show pause button if animation is playing
        if animation_playing:
            displayButton("pause")

        # Show play button if animation is paused
        else:
            displayButton("play")
        # Show stop button to restart        
        displayButton("stop")
    # If simulation not started...
    if not start_simulation:
       # Show only the start button (a play button moved to the right)
       displayButton("start")
    
    pygame.display.update()
    time.tick(50)
