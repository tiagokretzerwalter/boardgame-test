# Board game simulator

Welcome to the Board game simulator! This project was created as a way to allow me to test a board game that I am developing with friends. 
The project implements a real-time multiplayer card game using Python with Flask-SocketIO on the backend and jQuery on the frontend. Players can draw cards, shuffle decks, and interact with the game board in a collaborative and competitive environment. Everything that the board game would require you to do in real life, you can do within this webapp.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)

## Features

- Real-time multiplayer functionality
- Multiple decks of cards
- Player-specific hands and boards
- Shuffling and drawing cards
- Sending cards between players
- Resetting the game state

## Installation

### Prerequisites
- Python 3.x
- Flask
- Flask-SocketIO
- python-dotenv

### Steps

1. Clone the repository.
2. Navigate to the project directory
3. Set up a virtual environment:
    python3 -m venv venv
    source venv/bin/activate
    On Windows use `venv\Scripts\activate`
4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
5. Create a .env file with "SECRET_KEY=yoursecretkey" and "FLASK_DEBUG=True"
6. Run the application:

    ```sh
    flask run
    ```


## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Use the buttons on the web interface to draw cards, shuffle decks, and interact with other players.


## Folder Structure

```plaintext
board-game-app/
├── static/
│   ├── css/
│   │   └── base.css
│   └── js/
│       ├── index.js
│       └── player.js
├── templates/
│   └── index.html
├── data/
│   ├── type_cards.csv
│   └── type2_cards.csv
├── app.py
├── requirements.txt
└── README.md

The app Procfile is used for deployment.
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:

    ```sh
    git checkout -b feature-branch
    ```

3. Make your changes and commit them:

    ```sh
    git commit -m "Description of your changes"
    ```

4. Push to the branch:

    ```sh
    git push origin feature-branch
    ```

5. Create a pull request.
