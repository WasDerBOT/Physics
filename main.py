import sys
import math
import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
G = 1
K = 5
FPS = 60
dt = 1 / FPS

def collect_garbage():
    global Objects
    for object in Objects:
        if object.position.magnitude() > 1000:
            Objects.remove(object)

class Vector:
    def __init__(self, *components):
        self.components = list(components)

    def __len__(self):
        return len(self.components)

    def __getitem__(self, index):
        return self.components[index]

    def __setitem__(self, index, value):
        self.components[index] = value

    def __repr__(self):
        return f"Vector({', '.join(map(str, self.components))})"

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors must be of the same dimension for addition.")
        return Vector(*[a + b for a, b in zip(self.components, other.components)])

    def __sub__(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors must be of the same dimension for subtraction.")
        return Vector(*[a - b for a, b in zip(self.components, other.components)])

    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be a number.")
        return Vector(*[a * scalar for a in self.components])

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def dot(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors must be of the same dimension for dot product.")
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        return math.sqrt(sum(a**2 for a in self.components))

    def normalized(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector.")
        return Vector(*[a / mag for a in self.components])

    def to_tuple(self):
        return tuple(self.components)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        return all(a == b for a, b in zip(self.components, other.components))

    def __ne__(self, other):
        return not self.__eq__(other)

    def cut(self, limit):
        self.normalized()
        self *= limit


class Particle:
    def __init__(self, x, y, charge, mass, radius):
        self.position = Vector(x, y)
        self.charge = charge
        self.mass = mass
        self.radius = radius
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

    def interact_with(self, other):
        if other.position == self.position:
            return
        gravity_force = (other.position - self.position).normalized() * (G * self.mass * other.mass / ((other.position - self.position).magnitude() / (self.radius + other.radius)) ** 2)
        electro_weak_force = (other.position - self.position).normalized() * (K * self.charge * other.charge / ((other.position - self.position).magnitude() / (self.radius + other.radius)) ** 2)
        electro_strong_force = (other.position - self.position).normalized() * -1 * (
                    K * self.mass * other.mass / ((other.position - self.position).magnitude() / (self.radius + other.radius)) ** 3)

        a = electro_strong_force + gravity_force + electro_weak_force

        a *= 1 / self.mass

        self.acceleration = a
        self.velocity += a * dt
        if self.velocity.magnitude() > 10:
            self.velocity = self.velocity.normalized() * 50
        self.position += self.velocity * dt

    def draw(self):
        pygame.draw.circle(screen, BLUE, self.position.to_tuple(), self.radius)

Objects = []


running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_position = pygame.mouse.get_pos()
            Objects.append(Particle(click_position[0], click_position[1], 0, 100, 30))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pass
    if keys[pygame.K_RIGHT]:
        pass
    if keys[pygame.K_UP]:
        pass
    if keys[pygame.K_DOWN]:
        pass

    screen.fill(BLACK)
    collect_garbage()
    for obj in Objects:
        for other in Objects:
            if obj.position.to_tuple() != other.position.to_tuple():
                obj.interact_with(other)

    for obj in Objects:
        obj.draw()
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
sys.exit()
