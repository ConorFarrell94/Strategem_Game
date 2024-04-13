import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Strategem Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define the strategem combos
strategem_data = """
Machine Gun
Down, Left, Down, Up, Right

Anti-Material Rifle
Down, Left, Right, Up, Down

Stalwart
Down, Left, Down, Up, Up, Left

Expendable Anti-Tank
Down, Down, Left, Up, Right

Recoilless Rifle
Down, Left, Right, Right, Left

Flamethrower
Down, Left, Up, Down, Up

Autocannon
Down, Left, Down, Up, Up, Right

Railgun
Down, Right, Left, Down, Up, Left, Right

Spear
Down, Down, Up, Down, Down

Orbital Gatling Barrage
Right, Down, Left, Up, Up

Orbital Airburst Strike
Right, Right, Right

Orbital 120MM HE Barrage
Right, Down, Left, Right, Down

Orbital 380MM HE Barrage
Right, Down, Up, Up, Left, Down, Down

Orbital Walking Barrage
Right, Right, Down, Left, Right, Down

Orbital Lasers
Right, Down, Up, Right, Down

Orbital Railcannon Strike
Right, Up, Down, Down, Right

Eagle Strafing Run
Up, Right, Right

Eagle Airstrike
Up, Right, Down, Right

Eagle Cluster Bomb
Up, Right, Down, Down, Right

Eagle Napalm Airstrike
Up, Right, Down, Up

Jump Pack
Down, Up, Up, Down, Up

Eagle Smoke Strike
Up, Right, Up, Down

Eagle 110MM Rocket Pods
Up, Right, Up, Left

Eagle 500KG Bomb
Up, Right, Down, Down, Down

Orbital Precision Strike
Right, Right, Up

Orbital Gas Strike
Right, Right, Down, Right

Orbital EMS Strike
Right, Right, Left, Down

Orbital Smoke Strike
Right, Right, Down, Up

HMG Emplacement
Down, Up, Left, Right, Right, Left

Shield Generation Relay
Down, Up, Left, Down, Right, Right

Tesla Tower
Down, Up, Right, Up, Left, Right

Anti-Personnel Minefield
Down, Left, Up, Right

Supply Pack
Down, Left, Down, Up, Up, Down

Grenade Launcher
Down, Left, Up, Left, Down

Laser Cannon
Down, Left, Down, Up, Left

Incendiary Mines
Down, Left, Left, Down

Guard Dog Rover
Down, Up, Left, Up, Right, Right

Ballistic Shield Backpack
Down, Left, Up, Up, Right

Arc thrower
Down, Right, Up, Left, Down

Shield Generator Pack
Down, Up, Left, Right, Left, Right

Machine Gun Sentry
Down, Up, Right, Right, Up

Gatling Sentry
Down, Up, Right, Left

Mortar Sentry
Down, Up, Right, Right, Down

Guard Dog
Down, Up, Left, Up, Right, Down

Autocannon Sentry
Down, Up, Right, Up, Left, Up

Rocket Sentry
Down, Up, Right, Right, Left

EMS Mortar Sentry
Down, Down, Up, Up, Left
"""

# Parse combo data
combo_list = strategem_data.strip().split("\n\n")
combos = {}
for strategem_data in combo_list:
    lines = strategem_data.strip().split("\n")
    name = lines[0]
    combination = [key.strip() for key in lines[1].split(",")]
    combos[name] = combination

# Timing variables
time_limit = 15  # seconds per round
start_time = 0
time_remaining = time_limit

# Scoring variables
score = 0
highscore = 0

# Load a font
font_path = "Arial.ttf"
font = pygame.font.Font(font_path, 36)

# Define arrow symbols using Unicode characters
ARROW_SYMBOLS = {"Up": "↑", "Down": "↓", "Left": "←", "Right": "→"}


# Function to generate a new combo with arrow symbols
def generate_combo():
    while True:
        combo_name = random.choice(list(combos.keys()))
        combo = combos[combo_name]
        if combo:
            combo_with_arrows = [key for key in combo]
            return combo_name, combo_with_arrows


# Function to display text on the screen
def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Game state variables
game_started = False
combo_started = False
running = True
game_over = False
incorrect_key_time = 0
incorrect_key = False
incorrect_key_duration = 0.5  # in seconds

# Main game loop
combo_name, combo = "", []
original_combos = {}  # Dictionary to store original combos
while running:
    # Clear the screen
    screen.fill(WHITE)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started:
                # Start the game if Enter is pressed
                if event.key == pygame.K_RETURN:
                    game_started = True
                    combo_started = True
                    # Start the timer and generate the first combo
                    start_time = time.time()
                    combo_name, combo = generate_combo()
                    original_combos[combo_name] = list(combo)  # Store original combo
                    print("Game started!")

            elif game_over:
                # Restart the game if y is pressed
                if event.key == pygame.K_y:
                    game_over = False
                    game_started = False
                    score = 0
                    start_time = 0
                    time_remaining = time_limit
                    print("Game restarted!")
                    # Close the game if n is pressed

                elif event.key == pygame.K_n:
                    running = False
                    # if highscore is greater than 0, save it to a file
                    if highscore > 0:
                        with open("highscore.txt", "a") as file:
                            file.write(
                                f"Highscore: {highscore} | Date: {time.asctime()}\n"
                            )
                            file.close()

            else:
                # Check if the pressed key matches the next key in the combo
                if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    key = ""
                    if event.key == pygame.K_w:
                        key = "Up"
                    elif event.key == pygame.K_s:
                        key = "Down"
                    elif event.key == pygame.K_a:
                        key = "Left"
                    elif event.key == pygame.K_d:
                        key = "Right"

                    if len(combo) > 0 and key == combo[0]:
                        combo.pop(0)  # Remove the matched key
                        # add 1 second to the timer
                        if len(combo) == 0:  # If all keys matched
                            score += 1
                            combo_name, combo = generate_combo()
                            # Store original combo
                            original_combos[combo_name] = list(combo)
                            # start_time = time.time()  # Reset the timer
                            # add to the timer
                            start_time += 2

                            combo_started = True
                            print("Correct! Next combo:")
                            print(combo_name)
                            print(combo)
                    else:  # Incorrect key
                        if combo_started:
                            print("Incorrect key! Combo reset.")
                            # Reset combo to original state
                            combo = list(original_combos[combo_name])
                            # Remove from the timer
                            start_time -= 3
                            incorrect_key = True
                            incorrect_key_time = (
                                time.time()
                            )  # Start the timer for incorrect key message

    # Display the "Incorrect key" message for 0.5 seconds
    if incorrect_key and time.time() - incorrect_key_time < incorrect_key_duration:
        draw_text("Incorrect key!", 200, 400, RED)
    else:
        incorrect_key = False  # Reset incorrect key flag

    # Check if the game has started
    if not game_started:
        draw_text("Press Enter to start the game", 200, 200)
    elif game_over:
        # Display final score and prompt to restart the game
        draw_text("Game Over!", 300, 200, RED)
        draw_text("Final Score: " + str(score), 300, 250, RED)
        if score > highscore:
            highscore = score  # Update highscore only if current score is higher
        # Display highscore
        draw_text("Highest: " + str(highscore), 10, 90)
        draw_text("Restart? (y/n)", 280, 300, RED)

    else:
        # Check the time
        current_time = time.time()
        time_remaining = max(0, time_limit - (current_time - start_time))

        if time_remaining == 0:
            # Time's up, end the game
            game_over = True
            print("Time's up! Game over.")

        # Display the score and time remaining
        draw_text("Score: " + str(score), 10, 10)
        draw_text("Time: " + str(round(time_remaining)), 10, 50)

        # Display the name of the current combo
        draw_text("Combo: " + combo_name, 10, 130)

        # Display the remaining keys for the current combo using arrow symbols
        draw_text(
            "Remaining Keys: " + " ".join([ARROW_SYMBOLS[key] for key in combo]),
            10,
            170,
        )

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
