def movePlayers(keys):
    if keys[pygame.K_w]:
        player_pos1.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos1.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos1.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos1.x += 300 * dt

    if keys[pygame.K_UP]:
        player_pos2.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        player_pos2.y += 300 * dt
    if keys[pygame.K_LEFT]:
        player_pos2.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
        player_pos2.x += 300 * dt

# Function to draw the map for each player and zoom in
def draw_camera(screen, background, player_pos, zoom_level, offset_x, offset_y, screen_area):
    # Calculate the camera area around the player
    camera_width, camera_height = screen_area.width // zoom_level, screen_area.height // zoom_level

    # Define the top-left corner of the camera (keeping player in center)
    camera_x = player_pos.x - camera_width // 2
    camera_y = player_pos.y - camera_height // 2

    # Ensure the camera doesn't go outside the boundaries of the map
    camera_x = max(0, min(camera_x, background.get_width() - camera_width))
    camera_y = max(0, min(camera_y, background.get_height() - camera_height))

    # Adjust camera width and height if they exceed the map boundaries
    camera_width = min(camera_width, background.get_width() - camera_x)
    camera_height = min(camera_height, background.get_height() - camera_y)

    # Get the part of the map seen by the camera
    camera_view = background.subsurface(pygame.Rect(camera_x, camera_y, camera_width, camera_height))

    # Scale it up to fill the screen area (zoom effect)
    scaled_view = pygame.transform.scale(camera_view, (screen_area.width, screen_area.height))

    # Blit the zoomed map to the respective part of the screen
    screen.blit(scaled_view, (offset_x, offset_y))