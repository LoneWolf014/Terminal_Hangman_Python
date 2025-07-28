import random
import os
import time
from colorama import init, Fore, Back, Style

# Initialize colorama for Windows compatibility.
# This ensures ANSI escape codes work correctly on different operating systems,
# especially on Windows, to display colors and styles.
init(autoreset=True)

# --- Configuration ---
# List of words for the Hangman game. Words are in uppercase for consistency.
WORD_LIST = [
    "PYTHON", "PROGRAMMING", "COMPUTER", "DEVELOPER", "ALGORITHM",
    "TERMINAL", "SCANLINE", "RETRO", "HANGMAN", "KEYBOARD",
    "MONITOR", "ELECTRONIC", "VINTAGE", "CONSOLE", "PIXEL"
]

# ASCII art for each stage of the hangman.
# Each string represents a different stage of the hangman figure,
# from empty gallows to the full figure.
HANGMAN_STAGES = [
    # 0 incorrect guesses: Initial empty gallows
    """
       -----
       |   |
           |
           |
           |
           |
    ---------
    """,
    # 1 incorrect guess: Head
    """
       -----
       |   |
       O   |
           |
           |
           |
    ---------
    """,
    # 2 incorrect guesses: Body
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    ---------
    """,
    # 3 incorrect guesses: One arm
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    ---------
    """,
    # 4 incorrect guesses: Both arms
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    ---------
    """,
    # 5 incorrect guesses: One leg
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    ---------
    """,
    # 6 incorrect guesses: Both legs (Game Over state)
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ---------
    """
]

# The maximum number of incorrect guesses allowed before the game ends.
# This is derived from the number of hangman stages.
MAX_INCORRECT_GUESSES = len(HANGMAN_STAGES) - 1 # This will be 6

# --- CRT/Terminal Styling Functions ---

def clear_screen():
    """
    Clears the terminal screen.
    Uses 'cls' for Windows and 'clear' for Unix-like systems (Linux, macOS).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def apply_crt_style(text, bright=True):
    """
    Applies CRT-like styling to text: green foreground, black background.
    Optionally makes the text bright for emphasis.
    """
    if bright:
        return Fore.GREEN + Back.BLACK + Style.BRIGHT + text + Style.RESET_ALL
    else:
        # Use a dimmer style for borders or less important elements
        return Fore.GREEN + Back.BLACK + Style.DIM + text + Style.RESET_ALL

def draw_border_and_content(content_lines):
    """
    Draws an ASCII border around the provided content lines,
    ensuring a consistent CRT screen size (80 columns x 24 rows).
    """
    width = 80  # Standard terminal width
    height = 24 # Standard terminal height

    # Prepare content lines by padding them to fit within the border.
    # Subtract 4 for two side borders and two inner spaces.
    padded_content_lines = []
    for line in content_lines:
        padded_content_lines.append(line.ljust(width - 4))

    # Fill any remaining lines with empty space to maintain consistent screen height.
    # Subtract 2 for the top and bottom borders.
    while len(padded_content_lines) < height - 2:
        padded_content_lines.append("".ljust(width - 4))

    # Construct the full display, including top/bottom and side borders.
    full_display = []

    # Top border line
    full_display.append(apply_crt_style("+" + "-" * (width - 2) + "+", bright=False))

    # Content rows with side borders
    for line in padded_content_lines:
        full_display.append(apply_crt_style("| " + line + " |", bright=True)) # Content is bright

    # Bottom border line
    full_display.append(apply_crt_style("+" + "-" * (width - 2) + "+", bright=False))

    return full_display

def crt_refresh_effect(display_lines, delay=0.005):
    """
    Simulates a CRT screen refresh by printing lines one by one.
    This creates the "scanline going top-bottom" visual effect.
    """
    clear_screen()
    for line in display_lines:
        print(line)
        time.sleep(delay) # Small delay for the scanning effect

def display_game(chosen_word, guessed_letters, incorrect_guesses, message="", skip_effect=False):
    """
    Composes and displays the entire game screen.
    Includes the word, hangman status, guessed letters, and any messages.
    Applies the CRT refresh effect unless skipped (e.g., for subsequent input prompts).
    """
    # Create the masked word display (e.g., P _ T H _ N)
    display_word = ""
    for letter in chosen_word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "

    # Get the current ASCII art for the hangman figure based on incorrect guesses.
    hangman_art = HANGMAN_STAGES[incorrect_guesses].split('\n')

    # Prepare all content lines that will go inside the CRT frame.
    content = []
    # Game title, centered with bright style.
    content.append(" " * 15 + Style.BRIGHT + "--- HANGMAN CRT EDITION ---" + Style.RESET_ALL)
    content.append("")
    # Add the hangman ASCII art.
    content.extend(hangman_art)
    content.append("")
    # Display the masked word.
    content.append(f" Word: {display_word.strip()}")
    # Display already guessed letters, sorted for readability.
    # Removes any space if it somehow gets into guessed_letters set.
    content.append(f" Guessed Letters: {', '.join(sorted(list(guessed_letters - {' '})))}")
    # Display remaining incorrect guesses.
    content.append(f" Incorrect Guesses Left: {MAX_INCORRECT_GUESSES - incorrect_guesses}")
    content.append("")
    # Display a status message to the user.
    content.append(f" Status: {message}")
    content.append("")
    # Placeholder for the input prompt, which will be handled separately.
    content.append(" >_ ")

    # Get the full display content with borders and proper padding.
    full_display_content = draw_border_and_content(content)

    # Apply the CRT refresh effect or just print directly.
    if not skip_effect:
        crt_refresh_effect(full_display_content)
    else:
        # If skipping the effect, just clear and print all at once for faster updates
        clear_screen()
        for line in full_display_content:
            print(line)

# --- Game Logic ---

def get_guess(already_guessed):
    """
    Prompts the user for a single letter guess and validates it.
    Returns the valid guess or None if invalid.
    """
    while True:
        # The actual input prompt is shown here.
        guess = input(apply_crt_style("Enter your guess: ", bright=True)).upper()
        if len(guess) != 1 or not 'A' <= guess <= 'Z':
            print(apply_crt_style("Invalid input. Please enter a single letter (A-Z).", bright=True))
            time.sleep(1.5) # Pause to allow user to read the error message
            return None # Indicate an invalid guess
        if guess in already_guessed:
            print(apply_crt_style(f"You already guessed '{guess}'. Try again.", bright=True))
            time.sleep(1.5) # Pause to allow user to read the error message
            return None # Indicate an invalid guess
        return guess

def play_game():
    """
    Main function to run the Hangman game.
    Manages game flow, user input, and game state updates.
    """
    clear_screen()
    print(apply_crt_style("Booting up CRT Hangman...", bright=True))
    time.sleep(1.5) # Initial boot-up delay

    while True: # Loop to allow playing multiple games
        chosen_word = random.choice(WORD_LIST) # Select a random word for the new game
        guessed_letters = set() # Set to store unique guessed letters
        incorrect_guesses = 0   # Counter for incorrect guesses
        game_over = False       # Flag to control the game loop

        while not game_over:
            # Display the current game state before getting a guess.
            # Message is updated based on game flow.
            display_game(chosen_word, guessed_letters, incorrect_guesses, "Guess a letter.")

            # Check for win condition
            # All letters in the chosen word must be present in guessed_letters.
            if all(letter in guessed_letters for letter in chosen_word):
                display_game(chosen_word, guessed_letters, incorrect_guesses, "CONGRATULATIONS! You guessed the word!", skip_effect=True)
                game_over = True
                break

            # Check for loss condition
            # If incorrect guesses reach the maximum allowed.
            if incorrect_guesses >= MAX_INCORRECT_GUESSES:
                display_game(chosen_word, guessed_letters, incorrect_guesses, f"GAME OVER! The word was '{chosen_word}'.", skip_effect=True)
                game_over = True
                break

            # Get a valid guess from the user. Loop until a valid one is received.
            guess = None
            while guess is None:
                # Display the game with a prompt message before input.
                display_game(chosen_word, guessed_letters, incorrect_guesses, "Enter your guess...")
                guess = get_guess(guessed_letters) # Get input from the user

            guessed_letters.add(guess) # Add the valid guess to the set of guessed letters

            # Process the guess: check if it's in the word.
            if guess not in chosen_word:
                incorrect_guesses += 1
                display_game(chosen_word, guessed_letters, incorrect_guesses, f"'{guess}' is not in the word.")
                time.sleep(1) # Pause to allow user to read the message
            else:
                display_game(chosen_word, guessed_letters, incorrect_guesses, f"Good guess! '{guess}' is in the word.")
                time.sleep(1) # Pause to allow user to read the message

        # After a game ends, ask if the user wants to play again.
        play_again = input(apply_crt_style("\nPlay again? (yes/no): ", bright=True)).lower()
        if play_again != 'yes':
            break # Exit the main game loop if not 'yes'

    # Final message before exiting.
    clear_screen()
    print(apply_crt_style("Thanks for playing CRT Hangman!", bright=True))
    time.sleep(1.5)

# Entry point for the script.
if __name__ == "__main__":
    play_game()
