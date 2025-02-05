import math
import os
import pygame
from constants import *


class Vector:
    """Represents a two-dimensional vector with x and y as coordinates."""

    def __init__(self, x=0, y=0):
        """Return a new instance of Vector."""
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

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

        self.layers =[]
        car_image_path = CAR_IMAGES_PATH + ('red_car' if color == RED else 'blue_car')
        for img_file in sorted(os.listdir(car_image_path)):
            img = pygame.image.load(os.path.join(car_image_path, img_file))
            self.layers.append(img)

    def update(self, track_bounds):
        """Update car position and movement."""
        keys = pygame.key.get_pressed()

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

        is_moving = self.velocity.length() > 0.7
        if keys[self.controls['left']]:
            if  is_moving:
                self.angular_velocity -= CAR_FORWARD_VELOCITY
        if keys[self.controls['right']]:
            if is_moving:
                self.angular_velocity += CAR_FORWARD_VELOCITY

        speed = self.velocity.length()
        self.velocity = self.velocity.multiply(self.drag)
        self.velocity = self.velocity.add(self.acceleration)

        if speed > self.max_speed:
            self.velocity = self.velocity.multiply(self.max_speed / speed)

        old_position = Vector(self.position.x, self.position.y)
        self.position = self.position.add(self.velocity)

        if not (track_bounds[0] <= self.position.x <= track_bounds[2] and
                track_bounds[1] <= self.position.y <= track_bounds[3]):
            self.position = old_position
            self.velocity = Vector()

        self.angular_velocity *= self.angular_drag
        self.rotation += self.angular_velocity

    def draw(self, screen, camera_offset, viewport_rect):
        """Render the car."""
        points = [
            (self.position.x - self.width / 2, self.position.y - self.height / 2),
            (self.position.x + self.width / 2, self.position.y - self.height / 2),
            (self.position.x + self.width / 2, self.position.y + self.height / 2),
            (self.position.x - self.width / 2, self.position.y + self.height / 2)
        ]

        center = (self.position.x, self.position.y)
        rotated_points = []
        for point in points:
            x = point[0] - center[0]
            y = point[1] - center[1]
            rotated_x = x * math.cos(math.radians(self.rotation)) - y * math.sin(math.radians(self.rotation))
            rotated_y = x * math.sin(math.radians(self.rotation)) + y * math.cos(math.radians(self.rotation))

            screen_x = rotated_x + center[0] - camera_offset.x + viewport_rect.x
            screen_y = rotated_y + center[1] - camera_offset.y + viewport_rect.y
            rotated_points.append((screen_x, screen_y))

        if (viewport_rect.collidepoint(rotated_points[0]) and viewport_rect.collidepoint(rotated_points[1])
                and viewport_rect.collidepoint(rotated_points[2]) and viewport_rect.collidepoint(rotated_points[3])):
            pygame.draw.polygon(screen, self.color, rotated_points)


class Camera:
    """Represents a POV for a player."""

    def __init__(self, x, y):
        """Return new instance of Camera."""
        self.position = Vector(x, y)
        self.target_position = Vector(x, y)
        self.smoothness = CAMERA_SMOOTHNESS

    def update(self, target_x, target_y):
        """Update state of camera"""
        self.target_position = Vector(target_x, target_y)
        current_x = self.target_position.x - self.position.x
        current_y = self.target_position.y - self.position.y
        self.position.x += current_x * self.smoothness
        self.position.y += current_y * self.smoothness

# To be continued...
class Track:
    """Represents a track class."""

    def __init__(self):
        """Return a new instance of Track."""
        self.width = TRACK_WIDTH
        self.height = TRACK_HEIGHT
        self.outer_bounds = (0, 0, self.width, self.height)
        #self.checkpoints = []
        self.checkpoints = [
            (300, 300),
            (2700, 300),
            (2700, 1700),
            (300, 1700)
        ]

    def draw(self, screen, camera_offset, viewport_rect):
        # """Render track."""
        # surface = pygame.Surface((viewport_rect.width, viewport_rect.height))
        # surface.fill(GREEN)
        # # A map will be rendered later on!!!
        #
        # screen.blit(surface, viewport_rect)

        # Create a surface for this viewport
        viewport_surface = pygame.Surface((viewport_rect.width, viewport_rect.height))
        viewport_surface.fill(GREEN)  # Draw grass background

        # Draw track on viewport surface
        track_points = [(x - camera_offset.x, y - camera_offset.y)
                        for x, y in self.checkpoints]
        track_points.append(track_points[0])  # Close the loop
        pygame.draw.lines(viewport_surface, GRAY, False, track_points, 100)

        # Draw checkpoints on viewport surface
        for point in track_points[:-1]:
            pygame.draw.circle(viewport_surface, WHITE, (int(point[0]), int(point[1])), 10)

        # Blit the viewport surface onto the main screen at the correct position
        screen.blit(viewport_surface, viewport_rect)
