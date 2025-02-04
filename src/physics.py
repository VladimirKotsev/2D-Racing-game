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
        self.rotation = CAR_ROTATION
        self.color = color
        self.controls = controls
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.max_speed = CAR_MAX_SPEED
        self.drag = CAR_DRAG
        self.angular_velocity = CAR_ANGULAR_VELOCITY
        self.angular_drag = CAR_ANGULAR_DRAG

    def update(self):
        """Control the car movement."""
        # Handle input
        keys = pygame.key.get_pressed()

        # Forward/Backward
        if keys[self.controls['up']]:
            self.acceleration = Vector(
                math.sin(math.radians(self.rotation)) * CAR_FORWARD_VELOCITY,
                -math.cos(math.radians(self.rotation)) * CAR_FORWARD_VELOCITY
            )
        elif keys[self.controls['down']]:
            self.acceleration = Vector(
                -math.sin(math.radians(self.rotation)) * CAR_BACKWARD_VELOCITY,
                math.cos(math.radians(self.rotation)) * CAR_BACKWARD_VELOCITY
            )
        else:
            self.acceleration = Vector()

        # Turning
        if keys[self.controls['left']]:
            self.angular_velocity -= CAR_FORWARD_VELOCITY
        if keys[self.controls['right']]:
            self.angular_velocity += CAR_FORWARD_VELOCITY

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
