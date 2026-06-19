import os
import re
import random

def main():
    # 1. Capture the user's move from the issue title environment variable
    issue_title = os.getenv("ISSUE_TITLE", "").lower()
    choices = ["rock", "paper", "scissors"]
    
    player_move = None
    for choice in choices:
        if choice in issue_title:
            player_move = choice
            break

    if not player_move:
        print("Game outcome: Could not detect valid move from title.")
        return

    # 2. Bot selects a random move
    bot_move = random.choice(choices)
    
    # 3. Determine the match winner
    if player_move == bot_move:
        outcome = "tie"
    elif (player_move == "rock" and bot_move == "scissors") or \
         (player_move == "paper" and bot_move == "rock") or \
         (player_move == "scissors" and bot_move == "paper"):
        outcome = "player"
    else:
        outcome = "bot"

    # 4. Read the current README contents and parse the scoreboard numbers
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    p_wins = int(re.search(r"Player Wins\*\*:\s*(\d+)", readme).group(1))
    b_wins = int(re.search(r"Bot Wins\*\*:\s*(\d+)", readme).group(1))
    ties = int(re.search(r"Ties\*\*:\s*(\d+)", readme).group(1))

    # 5. Increment values based on match rules
    if outcome == "player":
        p_wins += 1
        msg = f"🎉 You won! Your {player_move} smashed the bot's {bot_move}."
    elif outcome == "bot":
        b_wins += 1
        msg = f"😢 You lost! The bot's {bot_move} defeated your {player_move}."
    else:
        ties += 1
        msg = f"🤝 It's a tie! Both chose {player_move}."

    # 6. Rebuild the updated README scoreboard string block
    updated_scoreboard = f"""<!-- RPS-SCOREBOARD-START -->
- 🏆 **Player Wins**: {p_wins}
- 🤖 **Bot Wins**: {b_wins}
- 🤝 **Ties**: {ties}
<!-- RPS-SCOREBOARD-END -->"""

    pattern = r"<!-- RPS-SCOREBOARD-START -->.*?<!-- RPS-SCOREBOARD-END -->"
    new_readme = re.sub(pattern, updated_scoreboard, readme, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

    # 7. Pass comment message to the subsequent steps inside GitHub Actions
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f"outcome_message={msg}", file=fh)

if __name__ == "__main__":
    main()
