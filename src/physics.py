import math
import pygame
from constants import *


class Vector:
    """Represents a two-dimensional vector with x and y as coordinates."""

    def __init__(self, x=0, y=0):
        """Return a new instance of Vector."""
        self.x = x
        self.y = y

    def add(self, other):
        """Return a vector added to another vector."""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        return Vector(self.x + other, self.y + other)

    def multiply(self, other):
        """Return a vector multiplied to another vector."""
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)

        return Vector(self.x * other, self.y * other)

    def divide(self, other):
        """Return a vector divided by another vector."""
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)

        return Vector(self.x / other, self.y / other)

    def dot(self, other):
        """Calculate the product of two vector coordinates."""
        return self.x * other.x + self.y * other.y

    def length(self):
        """Calculate the length of this vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        """Return the normalized vector of this vector."""
        length = self.length()
        if length != 0:
            return self.divide(length)

        return Vector()


class Car:
    """Represents a car."""

    def __init__(self, x, y, color, controls):
        """Return a new instance of Car."""
        self.position = Vector(x, y)
        self.velocity = Vector()
        self.acceleration = Vector()
        self.rotation = 0
        self.color = color
        self.controls = controls
        self.width = 40
        self.height = 100
        self.max_speed = 8
        self.drag = 0.98
        self.angular_velocity = 0
        self.angular_drag = 0.9

    def update(self):
        """Control the car movement."""
        # Handle input
        keys = pygame.key.get_pressed()

        # Forward/Backward
        if keys[self.controls['up']]:
            self.acceleration = Vector(
                math.sin(math.radians(self.rotation)) * 0.2,
                -math.cos(math.radians(self.rotation)) * 0.2
            )
        elif keys[self.controls['down']]:
            self.acceleration = Vector(
                -math.sin(math.radians(self.rotation)) * 0.1,
                math.cos(math.radians(self.rotation)) * 0.1
            )
        else:
            self.acceleration = Vector()

        # Turning
        if keys[self.controls['left']]:
            self.angular_velocity -= 0.2
        if keys[self.controls['right']]:
            self.angular_velocity += 0.2

        # Update physics
        self.velocity = self.velocity.add(self.acceleration)
        self.velocity = self.velocity.multiply(self.drag)

        # Limit speed
        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity = self.velocity.multiply(self.max_speed / speed)

        self.position = self.position.add(self.velocity)

        # Update rotation
        self.angular_velocity *= self.angular_drag
        self.rotation += self.angular_velocity

        # Screen boundaries
        self.position.x = max(0, min(self.position.x, SCREEN_WIDTH))
        self.position.y = max(0, min(self.position.y, SCREEN_HEIGHT))

    def draw(self, screen):
        """Draw the car."""
        # Create points for the car polygon
        points = [
            (self.position.x - self.width / 2, self.position.y - self.height / 2),
            (self.position.x + self.width / 2, self.position.y - self.height / 2),
            (self.position.x + self.width / 2, self.position.y + self.height / 2),
            (self.position.x - self.width / 2, self.position.y + self.height / 2)
        ]

        # Rotate points
        center = (self.position.x, self.position.y)
        rotated_points = []
        for point in points:
            x = point[0] - center[0]
            y = point[1] - center[1]
            rotated_x = x * math.cos(math.radians(self.rotation)) - y * math.sin(math.radians(self.rotation))
            rotated_y = x * math.sin(math.radians(self.rotation)) + y * math.cos(math.radians(self.rotation))
            rotated_points.append((rotated_x + center[0], rotated_y + center[1]))

        pygame.draw.polygon(screen, self.color, rotated_points)
