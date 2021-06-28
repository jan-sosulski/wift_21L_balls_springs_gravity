import pygame, sys, pymunk
import pymunk.pygame_util
import math
import random

class Ball:
    def __init__(self, space, x, y, collision_type):
        self.body = pymunk.Body(1,100,body_type=pymunk.Body.DYNAMIC)
        self.body.position = (x, y)
        self.r = 10
        self.shape = pymunk.Circle(self.body, self.r)
        self.shape.elasticity = 1
        self.shape.density = 1/50
        self.shape.collision_type = collision_type
        space.add(self.body, self.shape)


    def set_mass(self, mass):
        self.body.mass = mass

    def get_mass(self):
        return self.body.mass

    def get_position(self):
        return self.body.position

    def get_r(self):
        return self.r

def create_spring(space, body1, body2):
    spring_rest_length = 150
    spring_stiffness = 50
    spring_damping = 0

    spring = pymunk.DampedSpring(body1, body2, (0, 0), (0, 0), spring_rest_length, spring_stiffness, spring_damping)
    space.add(spring)

def create_walls(space, screen_width, screen_height):
    wall = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)

    shape1 = pymunk.Segment(wall, pymunk.Vec2d(0, 0), pymunk.Vec2d(screen_width, 0), 1) #north wall
    shape2 = pymunk.Segment(wall, pymunk.Vec2d(screen_width, 0), pymunk.Vec2d(screen_width, screen_height), 1) #east wall
    shape3 = pymunk.Segment(wall, pymunk.Vec2d(0, screen_height), pymunk.Vec2d(screen_width, screen_height), 1) #south wall
    shape4 = pymunk.Segment(wall, pymunk.Vec2d(0, 0), pymunk.Vec2d(0, screen_height), 1) #west wall

    space.add(wall, shape1, shape2, shape3, shape4)

def make_simple_gravity(balls):
    for ball_x in balls:
        gravity_vectors = []

        pos_x = ball_x.get_position()

        mass_x = ball_x.get_mass()

        for other_ball in balls:
            pos_other = other_ball.get_position()
            vector = ((pos_other[0]-pos_x[0]), (pos_other[1]-pos_x[1]))
            r = math.sqrt((vector[0]**2) + (vector[1]**2))

            mass_other = other_ball.get_mass()

            if r >= 10:
                gravity_vector = (mass_x*mass_other*(1/r**3) * vector[0], mass_x*mass_other*(1/r**3) * vector[1])
                gravity_vectors.append(gravity_vector)

        for gravity in gravity_vectors:
            ball_x.shape.body.apply_impulse_at_local_point((gravity[0]*1000, gravity[1]*1000), (0,0))

def create_all_springs(space, balls, springs_des):
    for i in springs_des:
        if i[0] != i[1] and i[0] != 0 and i[1] != 0:
            create_spring(space, balls[i[0]-1].body, balls[i[1]-1].body)

def create_all_balls(space, max, screen_width, screen_height):
    balls = []
    for i in range(0, max):
        i = Ball(space, random.randint(0, screen_width), random.randint(0, screen_height), 1)
        balls.append(i)
    return balls

#returned list of spring description, max number of ball
def convert_data(argv):
    springs_finall_description = []
    for i in range(1, len(argv)):
        spring_des = []
        for x in argv[i]:
            if x.isnumeric():
                spring_des.append(int(x))
        springs_finall_description.append(spring_des)

    for i in springs_finall_description:
        max = 1
        if i[0] > max:
            max = i[0]
        if i[1] > max:
            max = i[1]

    return springs_finall_description, max

#main function
def start_game(data):
    pygame.init()

    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    center = screen.get_rect().center
    pygame.display.set_caption("simulation mass springs gravity")

    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, 0)

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    create_walls(space, screen_width, screen_height)

    balls = create_all_balls(space, data[1], screen_width, screen_height)

    create_all_springs(space, balls, data[0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        space.debug_draw(draw_options)

        make_simple_gravity(balls)

        space.step(1/200)

        pygame.display.update()
        clock.tick(120)

#[1,2] [3,0] <- 1, 2 springs and 3 without spring
if __name__ == '__main__':
    try:
        if len(sys.argv) >= 2:
            springs_description = sys.argv

            data = convert_data(sys.argv)

            start_game(data)
        else:
            print("Invalid program call arguments!")

    except Exception as err:
        print(err)

    finally:
        print("The simulation ran correctly!")
