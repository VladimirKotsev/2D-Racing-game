import math
import os
import pygame
import time
import random
from constants import *


class Vector:
    """Represents a two-dimensional vector with x and y as coordinates."""

    def __init__(self, x=0, y=0):
        """Return a new instance of Vector."""
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        """Return a vector added to another vector."""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        """Return a vector subtracted by another vector."""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

        return Vector(self.x - other, self.y - other)

    def __mul__(self, other):
        """Return a vector multiplied to another vector."""
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)

        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        """Return a vector divided by another vector."""
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)

        return Vector(self.x / other, self.y / other)

    def dot(self, other):
        """Calculate the dot product of two vectors."""
        return self.x * other.x + self.y * other.y

    def length(self):
        """Calculate the length of this vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        """Return the normalized vector of this vector."""
        length = self.length()
        if length != 0:
            return self / length
        return Vector()


class Car:
    """Represents a car."""

    def __init__(self, x, y, angular_velocity, color, controls):
        """Return a new instance of Car."""
        self.start_position = Vector(x, y)
        self.start_angular_velocity = angular_velocity
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
        self.angular_velocity = angular_velocity
        self.angular_drag = CAR_ANGULAR_DRAG
        self.collision_cooldown = 0
        self.off_track = False
        self.has_started = False
        self.has_finished = False
        self.time_start = 0
        self.finish_time = 0

        self.layers = []
        car_image_path = CAR_IMAGES_PATH + ('red_car' if color == RED else 'blue_car')
        for img_file in sorted(os.listdir(car_image_path)):
            img = pygame.image.load(os.path.join(car_image_path, img_file))
            enlargen_img = pygame.transform.scale_by(img, (CAR_SPRITESTACK_ENLARGE, CAR_SPRITESTACK_ENLARGE))
            self.layers.append(enlargen_img)

    def rematch(self):
        self.off_track = False
        self.has_started = False
        self.has_finished = False
        self.position = self.start_position
        self.velocity = Vector()
        self.angular_velocity = self.start_angular_velocity
        self.rotation = CAR_ROTATION
        self.time_start = 0

    def get_corners(self):
        """Get the rotated corners of the car."""
        half_width = self.width / 2
        half_height = self.height / 2

        sin_rot = math.sin(math.radians(self.rotation))
        cos_rot = math.cos(math.radians(self.rotation))

        corners = [
            (-half_width, -half_height),
            (half_width, -half_height),
            (half_width, half_height),
            (-half_width, half_height)
        ]

        rotated_corners = []
        for x, y in corners:
            rotated_x = x * cos_rot - y * sin_rot
            rotated_y = x * sin_rot + y * cos_rot

            world_x = rotated_x + self.position.x
            world_y = rotated_y + self.position.y

            rotated_corners.append((world_x, world_y))

        return rotated_corners

    def check_collision(self, other_car):
        """Check and handle collision with another car."""
        if self.collision_cooldown > 0 or other_car.collision_cooldown > 0:
            return False

        self_corners = self.get_corners()
        other_corners = other_car.get_corners()

        def get_projection_range(corners, axis):
            dots = [axis.dot(Vector(x, y)) for x, y in corners]
            return min(dots), max(dots)

        def get_axes(corners):
            axes = []
            for i in range(len(corners)):
                p1 = Vector(corners[i][0], corners[i][1])
                p2 = Vector(corners[(i + 1) % len(corners)][0], corners[(i + 1) % len(corners)][1])
                edge = p2 - p1
                normal = Vector(-edge.y, edge.x).normalize()
                axes.append(normal)
            return axes

        axes = get_axes(self_corners) + get_axes(other_corners)

        collision = True
        min_overlap = float('inf')
        collision_normal = None

        for axis in axes:
            range1 = get_projection_range(self_corners, axis)
            range2 = get_projection_range(other_corners, axis)

            if range1[1] < range2[0] or range2[1] < range1[0]:
                collision = False
                break

            overlap = min(range1[1], range2[1]) - max(range1[0], range2[0])
            if overlap < min_overlap:
                min_overlap = overlap
                collision_normal = axis

        if collision and collision_normal:
            diff = self.position - other_car.position
            if diff.dot(collision_normal) < 0:
                collision_normal = Vector(-collision_normal.x, -collision_normal.y)

            separation = collision_normal * (min_overlap / 2 + 1)
            self.position = self.position + separation
            other_car.position = other_car.position - separation

            relative_velocity = self.velocity - other_car.velocity
            bounce_force = collision_normal * (CAR_COLLISION_BOUNCE * relative_velocity.length())

            self.velocity = bounce_force
            other_car.velocity = bounce_force * -1

            self.collision_cooldown = 10
            other_car.collision_cooldown = 10

            return True

        return False

    def update(self, track_bounds, track):
        """Update car position and movement."""
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        keys = pygame.key.get_pressed()

        car_pos = (int(self.position.x), int(self.position.y))
        self.off_track = not track.is_on_track(car_pos)
        track.is_on_race_line(self)
        is_cheating = track.is_cheating(car_pos)

        # Reduce speed if offtrack
        speed_multiplier = CAR_OFFTRACK_SLOWING_INDEX if self.off_track else 1.0
        speed_multiplier = CAR_OFFTRACK_CHEATING if is_cheating else 1.0

        if keys[self.controls['up']]:
            self.acceleration = Vector(
                math.sin(math.radians(self.rotation)) * CAR_FORWARD_VELOCITY * speed_multiplier,
                -math.cos(math.radians(self.rotation)) * CAR_FORWARD_VELOCITY * speed_multiplier
            )
        elif keys[self.controls['down']]:
            self.acceleration = Vector(
                -math.sin(math.radians(self.rotation)) * CAR_BACKWARD_VELOCITY * speed_multiplier,
                math.cos(math.radians(self.rotation)) * CAR_BACKWARD_VELOCITY * speed_multiplier
            )
        else:
            self.acceleration = Vector()

        is_moving = self.velocity.length() > CAR_TURN_LIMITER
        if keys[self.controls['left']]:
            if is_moving:
                self.angular_velocity -= CAR_FORWARD_VELOCITY * speed_multiplier
        if keys[self.controls['right']]:
            if is_moving:
                self.angular_velocity += CAR_FORWARD_VELOCITY * speed_multiplier

        speed = self.velocity.length()
        self.velocity = self.velocity * (self.drag * (0.95 if self.off_track else 1.0))
        self.velocity = self.velocity + self.acceleration

        if speed > self.max_speed * speed_multiplier:
            self.velocity = self.velocity * (self.max_speed * speed_multiplier / speed)

        old_position = Vector(self.position.x, self.position.y)
        self.position = self.position + self.velocity

        if not (track_bounds[0] <= self.position.x <= track_bounds[2] and
                track_bounds[1] <= self.position.y <= track_bounds[3]):
            self.position = old_position
            self.velocity = Vector()

        self.angular_velocity *= self.angular_drag
        self.rotation += self.angular_velocity

    def render_stack(self, screen, camera_offset, viewport_rect):
        screen_position = (
            self.position.x - camera_offset.x + viewport_rect.x,
            self.position.y - camera_offset.y + viewport_rect.y
        )

        if (0 <= screen_position[0] <= viewport_rect.width and
                0 <= screen_position[1] <= viewport_rect.height):

            for i, layer in enumerate(self.layers):
                rotated_layer = pygame.transform.rotate(layer, -self.rotation)

                layer_pos = (
                    screen_position[0] - rotated_layer.get_width() // 2,
                    screen_position[1] - rotated_layer.get_height() // 2 - i * CAR_LAYER_SPREAD
                )

                screen.blit(rotated_layer, layer_pos)

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
            self.render_stack(screen, camera_offset, viewport_rect)


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


class Track:
    """Represents a track class."""

    def __init__(self):
        """Return a new instance of Track."""
        self.width = TRACK_WIDTH
        self.height = TRACK_HEIGHT
        self.outer_bounds = (0, 0, self.width, self.height)

        track_num = random.randint(0, 2)
        #track_num = 2

        self.track_image = pygame.image.load(TRACK_PATH + f'track_{track_num}.png')
        self.track_image = pygame.transform.scale(self.track_image, (self.width, self.height))
        self.track_image = self.track_image.convert()

        self.p1_start = TRACKS[track_num][1] # tuple coordinates
        self.p2_start = TRACKS[track_num][2] # tuple coordinates
        self.angular_velocity = TRACKS[track_num][3]

    def is_cheating(self, position):
        """Check if a position is out of track and player is trying to cheat."""
        x, y = position

        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        try:
            color = self.track_image.get_at((int(x), int(y)))
            # Track color is around RGB(8, 109, 10)
            return (abs(color[0] - 8) < 9 and
                    abs(color[1] - 109) < 9 and
                    abs(color[2] - 10) < 9)
        except IndexError:
            return False

    def is_on_track(self, position):
        """Check if a position is on the track."""
        x, y = position

        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        try:
            color = self.track_image.get_at((int(x), int(y)))
            # Track color is around RGB(79, 92, 73)
            return ((abs(color[0] - 79) < 15 and
                    abs(color[1] - 92) < 15 and
                    abs(color[2] - 73) < 15) or
                    (abs(color[0] - 255) < 15 and
                    abs(color[1] - 255) < 15 and
                    abs(color[2] - 255) < 15))
        except IndexError:
            return False

    def is_on_race_line(self, car):
        """Check if a position is on the race line."""
        x, y = (int(car.position.x), int(car.position.y))

        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        try:
            color = self.track_image.get_at((int(x), int(y)))
            # Race line color is RGB(255, 255, 255)
            if (abs(color[0] - 255) < 15 and
                    abs(color[1] - 255) < 15 and
                    abs(color[2] - 255) < 15):
                if not car.has_started:
                    car.has_started = True
                    car.time_start = time.time()  # Start the timer
                    return False
                elif (car.has_started and
                      int(time.time() - car.time_start) >= CAR_MINIMUM_AFTER_START and
                      car.finish_time == 0):
                    car.has_finished = True
                    car.finish_time = int(time.time() - car.time_start)
                    return True
                else:
                    return False
        except IndexError:
            return False

    def draw(self, screen, camera_offset, viewport_rect):
        """Draw the track on the screen."""
        view_x = int(camera_offset.x)
        view_y = int(camera_offset.y)

        viewport_surface = pygame.Surface((viewport_rect.width, viewport_rect.height))

        source_rect = pygame.Rect(
            max(0, view_x),
            max(0, view_y),
            min(self.width - view_x, viewport_rect.width),
            min(self.height - view_y, viewport_rect.height)
        )

        dest_x = max(0, -view_x)
        dest_y = max(0, -view_y)

        viewport_surface.blit(self.track_image, (dest_x, dest_y), source_rect)

        screen.blit(viewport_surface, viewport_rect)


class Player:
    """Represents a game player."""

    def __init__(self, nickname, car, player_pov):
        """Create a new instance of Player."""
        self.nickname = nickname
        self.car = car
        self.camera = Camera(car.position.x, car.position.y)
        self.player_pov = player_pov

    def __str__(self):
        """Return player's nickname."""
        return str(self.nickname)

    @property
    def nickname(self):
        """Getter for nickname."""
        return self._nickname

    @nickname.setter
    def nickname(self, new_nickname):
        """Setter for nickname."""
        self._nickname = new_nickname

    def get_time(self):
        """Return player's finish time."""
        return self.car.finish_time

    def has_finished(self):
        """Return if player is winner."""
        return self.car.has_finished

    def update(self, track):
        """Update player's car and camera."""
        self.car.update(track.outer_bounds, track)
        self.camera.update(self.car.position.x - SPLIT_WIDTH / 2, self.car.position.y - SCREEN_HEIGHT / 2)

    def draw(self, screen, other_car):
        """Draw to player cars to screen."""
        self.car.draw(screen, self.camera.position, self.player_pov)
        other_car.draw(screen, self.camera.position, self.player_pov)

    def check_collision(self, other_player):
        """Check for collision between two players."""
        self.car.check_collision(other_player.car)

    def rematch(self):
        """Rematch players."""
        self.car.rematch()
