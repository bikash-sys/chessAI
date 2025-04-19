# chessAI

# Chess AI Game

This is a Python-based chess game that incorporates an AI opponent using the `python-chess` library. The game allows players to play chess against a computer with a fully functional graphical user interface (GUI) powered by Tkinter.

### Features
- **Graphical User Interface (GUI)**: Built using Tkinter for a smooth chess-playing experience.
- **AI Opponent**: The AI is powered by the `python-chess` library, utilizing Stockfish for move calculations.
- **Piece Movement**: Pieces can be moved by clicking on the chessboard.
- **Highlighting Moves**: Valid moves for selected pieces are highlighted for better visualization.
- **End Game Notifications**: Upon winning or losing, the game displays appropriate messages and feedback.

### Installation

Follow these steps to run the game on your local machine or in a cloud-based environment like **GitHub Codespaces**.

#### 1. Clone the Repository

```bash
git clone https://github.com/bikash-sys/chessAI.git
cd chess-ai-game
```

#### 2. Set Up Python Environment

Create a virtual environment and activate it.

```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

#### 3. Install Dependencies

Install all necessary Python libraries:

```bash
pip install chess tkinter
```

#### 4. Run the Game

Once the environment is set up and the dependencies are installed, you can run the game:

```bash
python chessai.py
```

This will launch the game with a GUI interface for playing chess against the AI.

### Gameplay Instructions

- **Move a piece**: Click on a piece to select it, and then click on the destination square to move it.
- **AI Move**: After each of your moves, the AI will automatically make its move.
- **Game Over**: If you win or lose, a message will be displayed, and the game will end.
- **Valid Moves Highlight**: When selecting a piece, its valid moves will be highlighted on the board.

### Customizations and Future Improvements

This project is an ongoing development, and we plan to add more features like:

- **Difficulty Levels**: Implementing adjustable difficulty levels for the AI.
- **Online Multiplayer**: Adding an option for online multiplayer matches.
- **Advanced AI Strategies**: Improving the AI's decision-making process for harder challenges.

### Contribution

Feel free to contribute to this project by submitting pull requests, opening issues, or suggesting new features!

- **Fork** the repository.
- **Clone** your fork.
- Make changes and **commit** your improvements.
- **Push** your changes to your fork.
- **Submit** a pull request to the main repository.



