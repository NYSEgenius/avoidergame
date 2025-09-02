import sys, pygame, math


# Finished game author: Turner Cox

def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one contacts the other.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap


def begin_level_1():
    """
    Display the first level
    """
    map = pygame.image.load("cs1400_a11_map1.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    map_rect = map.get_rect()

    # create the window based on the map size
    screen = pygame.display.set_mode(map_size)
    map = map.convert_alpha()
    map.set_colorkey((255, 255, 255))
    map_mask = pygame.mask.from_surface(map)

    # Create the player data
    player = pygame.image.load("cs1400_a11_smileyball.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (25, 25))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    key = pygame.image.load("cs1400_a11_key.png").convert_alpha()
    key = pygame.transform.smoothscale(key, (25, 25))
    key_rect = key.get_rect()
    key_rect.center = (50, 520)
    key_mask = pygame.mask.from_surface(key)

    gate = pygame.image.load("cs1400_a11_gate.png").convert_alpha()
    gate = pygame.transform.smoothscale(gate, (70, 70))
    gate_rect = gate.get_rect()
    gate_rect.center = (450, 250)
    gate_mask = pygame.mask.from_surface(gate)

    starting_point = pygame.image.load("cs1400_a11_start.png").convert_alpha()
    starting_point = pygame.transform.smoothscale(starting_point, (75, 75))
    starting_point_rect = starting_point.get_rect()
    starting_point_rect.center = (40, 240)
    starting_point_mask = pygame.mask.from_surface(starting_point)

    elevator = pygame.image.load("cs1400_a11_elevator.png").convert_alpha()
    elevator = pygame.transform.smoothscale(elevator, (75, 75))
    elevator_rect = elevator.get_rect()
    elevator_rect.center = (750, 500)
    elevator_mask = pygame.mask.from_surface(elevator)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    myfont = pygame.font.SysFont('monospace', 24)
    myfont_big = pygame.font.SysFont('monospace', 100)

    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # This state variable shows whether the key is found yet or not
    found_key = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene

    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            # Check if player clicks start
            elif event.type == pygame.MOUSEBUTTONDOWN and pixel_collision(player_mask, player_rect, starting_point_mask,
                                                                          starting_point_rect) and not started:
                started = True

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player_rect.center = pos

        # Draw the background
        screen.fill((250, 250, 250))
        screen.blit(map, map_rect)

        # Draw the starting point
        if not started:
            screen.blit(starting_point, starting_point_rect)

        # Only draw the key and door if the key is not collected
        if not found_key:
            screen.blit(key, key_rect)
            screen.blit(gate, gate_rect)

        # Draw finish line
        screen.blit(elevator, elevator_rect)

        # Draw the player character
        screen.blit(player, player_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = myfont.render("Escape Hell", True, (0, 255, 0))
        screen.blit(label, (50, 80))
        label = myfont.render("Use the key to unlock the gate, get to the elevator", True, (0, 255, 0))
        screen.blit(label, (50, 110))

        # See if we touch the maze walls
        if pixel_collision(player_mask, player_rect, map_mask, map_rect) and started:
            is_alive = False

        # Check if player has touched gate
        if pixel_collision(player_mask, player_rect, gate_mask, gate_rect) and not found_key and started:
            is_alive = False

        # Check if we contact the key
        if not found_key and pixel_collision(player_mask, player_rect, key_mask, key_rect) and started:
            found_key = True

        # Check if player has hit finish line
        if pixel_collision(player_mask, player_rect, elevator_mask, elevator_rect) and started:
            # go to level 2
            begin_level_2()

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    # display GAME OVER once player has died
    game_over_screen = myfont_big.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game_over_screen, (200, 300))
    click_to_exit = myfont.render("click anywhere to exit", True, (0, 0, 0))
    screen.blit(click_to_exit, (200, 400))
    pygame.display.update()

    # wait for the player to click to exit the program
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_click = False


def begin_level_2():
    """
    Display the second level
    """
    map = pygame.image.load("cs1400_a11_map2.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    map_rect = map.get_rect()

    # create the window based on the map size
    screen = pygame.display.set_mode(map_size)
    map = map.convert_alpha()
    map.set_colorkey((255, 255, 255))
    map_mask = pygame.mask.from_surface(map)

    # Create the player data
    player = pygame.image.load("cs1400_a11_smileyball.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (25, 25))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # create a legion of 7 demons
    demons_list = []
    for count in range(7):
        demon = pygame.image.load("cs1400_a11_demon.png").convert_alpha()
        demon = pygame.transform.smoothscale(demon, (70, 70))
        demon_rect = demon.get_rect()
        # space out the demons
        demon_rect.center = (-300 + count * 100, 10 + count * 100)
        demon_mask = pygame.mask.from_surface(demon)

        demon_traits = (demon, demon_rect, demon_mask)
        demons_list.append(demon_traits)

    # this variable initializes the loop that makes the demons move
    # we use the fact that the sin function oscillates between -1 and 1
    # to cause the demons to move back and forth
    demon_count = 0

    starting_point = pygame.image.load("cs1400_a11_start.png").convert_alpha()
    starting_point = pygame.transform.smoothscale(starting_point, (75, 75))
    starting_point_rect = starting_point.get_rect()
    starting_point_rect.center = (40, 40)
    starting_point_mask = pygame.mask.from_surface(starting_point)

    elevator = pygame.image.load("cs1400_a11_elevator.png").convert_alpha()
    elevator = pygame.transform.smoothscale(elevator, (75, 75))
    elevator_rect = elevator.get_rect()
    elevator_rect.center = (400, 300)
    elevator_mask = pygame.mask.from_surface(elevator)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    myfont = pygame.font.SysFont('monospace', 24)
    myfont_big = pygame.font.SysFont('monospace', 100)
    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene

    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            # Check if player clicks start
            elif event.type == pygame.MOUSEBUTTONDOWN and pixel_collision(player_mask, player_rect, starting_point_mask,
                                                                          starting_point_rect) and not started:
                started = True

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player_rect.center = pos

        # Draw the background
        screen.fill((250, 250, 250))
        screen.blit(map, map_rect)

        # Draw the starting point
        if not started:
            screen.blit(starting_point, starting_point_rect)

        # spawn in the demons
        for demon_traits in demons_list:
            screen.blit(demon_traits[0], demon_traits[1])

        # Draw finish line
        screen.blit(elevator, elevator_rect)

        # Draw the player character
        screen.blit(player, player_rect)

        # See if we touch the maze walls
        if pixel_collision(player_mask, player_rect, map_mask, map_rect) and started:
            is_alive = False

        # Check if player has touched demon
        for demon_traits in demons_list:
            if pixel_collision(player_mask, player_rect, demon_traits[2], demon_traits[1]) and started:
                is_alive = False

        # Make the demons move
        for demon_traits in demons_list:
            if math.sin(demon_count) >= 0:
                demon_traits[1].center = (demon_traits[1].center[0] + 5, demon_traits[1].center[1])
                demon_count += math.pi / 1200
            else:
                demon_traits[1].center = (demon_traits[1].center[0] - 5, demon_traits[1].center[1])
                demon_count += math.pi / 1200

        # check if player has hit finish line
        if pixel_collision(player_mask, player_rect, elevator_mask, elevator_rect) and started:
            # go to level 3
            begin_level_3()

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    # display GAME OVER once player has died
    game_over_screen = myfont_big.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game_over_screen, (200, 300))
    click_to_exit = myfont.render("click anywhere to exit", True, (0, 0, 0))
    screen.blit(click_to_exit, (200, 400))
    pygame.display.update()

    # wait for the player to click to exit the program
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_click = False

def begin_level_3():
    """
    Display the third level
    """
    map = pygame.image.load("cs1400_a11_map3.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    map_rect = map.get_rect()

    # create the window based on the map size
    screen = pygame.display.set_mode(map_size)
    map = map.convert_alpha()
    map.set_colorkey((255, 255, 255))
    map_mask = pygame.mask.from_surface(map)

    # Create the player data
    player = pygame.image.load("cs1400_a11_smileyball.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (25, 25))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    starting_point = pygame.image.load("cs1400_a11_start.png").convert_alpha()
    starting_point = pygame.transform.smoothscale(starting_point, (75, 75))
    starting_point_rect = starting_point.get_rect()
    starting_point_rect.center = (80, 80)
    starting_point_mask = pygame.mask.from_surface(starting_point)

    winscreen = pygame.image.load("cs1400_a11_winscreen.jpeg").convert_alpha()
    winscreen = pygame.transform.smoothscale(winscreen, (800, 600))
    winscreen_rect = winscreen.get_rect()
    winscreen_rect.center = (400, 300)
    winscreen_mask = pygame.mask.from_surface(winscreen)

    elevator = pygame.image.load("cs1400_a11_elevator.png").convert_alpha()
    elevator = pygame.transform.smoothscale(elevator, (75, 75))
    elevator_rect = elevator.get_rect()
    elevator_rect.center = (700, 500)
    elevator_mask = pygame.mask.from_surface(elevator)

    demon = pygame.image.load("cs1400_a11_demon.png").convert_alpha()
    demon = pygame.transform.smoothscale(demon, (70, 70))
    demon_rect = demon.get_rect()
    demon_rect.center = (20, 550)
    demon_mask = pygame.mask.from_surface(demon)

    key1 = pygame.image.load("cs1400_a11_key.png").convert_alpha()
    key1 = pygame.transform.smoothscale(key1, (25, 25))
    key1_rect = key1.get_rect()
    key1_rect.center = (420, 540)
    key1_mask = pygame.mask.from_surface(key1)

    key2 = pygame.image.load("cs1400_a11_key.png").convert_alpha()
    key2 = pygame.transform.smoothscale(key2, (25, 25))
    key2_rect = key2.get_rect()
    key2_rect.center = (420, 350)
    key2_mask = pygame.mask.from_surface(key2)

    key3 = pygame.image.load("cs1400_a11_key.png").convert_alpha()
    key3 = pygame.transform.smoothscale(key3, (25, 25))
    key3_rect = key3.get_rect()
    key3_rect.center = (500, 20)
    key3_mask = pygame.mask.from_surface(key3)

    gate = pygame.image.load("cs1400_a11_gate.png").convert_alpha()
    gate = pygame.transform.smoothscale(gate, (70, 70))
    gate_rect = gate.get_rect()
    gate_rect.center = (600, 500)
    gate_mask = pygame.mask.from_surface(gate)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    myfont = pygame.font.SysFont('monospace', 24)
    myfont_big = pygame.font.SysFont('monospace', 100)
    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # This state variable shows whether each key is found yet or not
    found_key1 = False

    # This state variable shows whether each key is found yet or not
    found_key2 = False

    # This state variable shows whether each key is found yet or not
    found_key3 = False

    # This variable initializes the key counter
    key_counter = 0

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene

    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            # Check if player clicks start
            elif event.type == pygame.MOUSEBUTTONDOWN and pixel_collision(player_mask, player_rect, starting_point_mask,
                                                                          starting_point_rect) and not started:
                started = True

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player_rect.center = pos

        # Draw the background
        screen.fill((250, 250, 250))
        screen.blit(map, map_rect)

        # Draw the starting point
        if not started:
            screen.blit(starting_point, starting_point_rect)

        # spawn in a demon
        screen.blit(demon, demon_rect)

        # Only draw the gate if the keys are not collected
        if not key_counter == 3:
            screen.blit(gate, gate_rect)

        # Only draw the keys if they are not collected
        if not found_key1:
            screen.blit(key1, key1_rect)

        if not found_key2:
            screen.blit(key2, key2_rect)

        if not found_key3:
            screen.blit(key3, key3_rect)

        # Draw finish line
        screen.blit(elevator, elevator_rect)

        # Draw the player character
        screen.blit(player, player_rect)

        label = myfont.render("Collect the keys", True, (0, 255, 0))
        screen.blit(label, (10, 10))
        label = myfont.render("RUN FOR YOUR LIFE", True, (0, 255, 0))
        screen.blit(label, (10, 130))

        # See if we touch the maze walls
        if pixel_collision(player_mask, player_rect, map_mask, map_rect) and started:
            is_alive = False

        # Check if player has touched demon
        if pixel_collision(player_mask, player_rect, demon_mask, demon_rect) and started:
            is_alive = False

        # Make the demon chase the player
        if started:
            if demon_rect.center[0] < player_rect.center[0]:
                demon_rect.center = (demon_rect.center[0] + 1, demon_rect.center[1])
            elif demon_rect.center[0] > player_rect.center[0]:
                demon_rect.center = (demon_rect.center[0] - 1, demon_rect.center[1])
            if demon_rect.center[1] < player_rect.center[1]:
                demon_rect.center = (demon_rect.center[0], demon_rect.center[1] + 1)
            elif demon_rect.center[1] > player_rect.center[1]:
                demon_rect.center = (demon_rect.center[0], demon_rect.center[1] - 1)

        # Check if player has touched gate
        if pixel_collision(player_mask, player_rect, gate_mask, gate_rect) and not key_counter == 3 and started:
            is_alive = False

        # Check if we contact the key1
        if not found_key1 and pixel_collision(player_mask, player_rect, key1_mask, key1_rect) and started:
            key_counter += 1
            found_key1 = True

        # Check if we contact the key2
        if not found_key2 and pixel_collision(player_mask, player_rect, key2_mask, key2_rect) and started:
            key_counter += 1
            found_key2 = True

        # Check if we contact the key3
        if not found_key3 and pixel_collision(player_mask, player_rect, key3_mask, key3_rect) and started:
            key_counter += 1
            found_key3 = True

        # check if player has hit finish line
        if pixel_collision(player_mask, player_rect, elevator_mask, elevator_rect) and started:
            # display win screen
            screen.blit(winscreen, winscreen_rect)
        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    # display GAME OVER once player has died
    game_over_screen = myfont_big.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game_over_screen, (200, 300))
    click_to_exit = myfont.render("click anywhere to exit", True, (0, 0, 0))
    screen.blit(click_to_exit, (200, 400))
    pygame.display.update()

    # wait for the player to click to exit the program
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_click = False

def main():
    # Initialize pygame
    pygame.init()

    # begin level 1, which starts the whole game, as the other level are called within this function
    begin_level_1()


# Start the program
main()
