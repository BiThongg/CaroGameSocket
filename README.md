# Socket Board Game

Socket Board Game is an online game developed by our team, integrating two popular board games, Tic-Tac-Toe and Caro (Gomoku), into one module. The game is implemented on a web platform with a client-server architecture using the Socket protocol to ensure real-time communication. This architecture supports multiple players at once, offering a connected and interactive gaming experience.

## Technologies Used

- **Flask (Python)**: Framework for implementing the backend server.
- **ReactJS (TypeScript)**: Library for developing the client-side interface.
- **Socket.IO**: A library that provides WebSocket protocol with extended features for real-time communication.
- **Deployment**: Ubuntu Server OS for setting up the environment and deploying the project to the web.
- **Version Control**: Git, GitHub.

## Links

- **GitHub Repository**: [Socket Board Game Repository](#)  
- **Webgame URL**: [Play the Game](#)

---

## Chapter 1: Project Introduction

### Overview
Socket Board Game is a real-time multiplayer game combining Tic-Tac-Toe and Caro into a unified web interface. It uses a client-server model with Flask handling the backend and ReactJS managing the frontend. Socket.IO ensures smooth real-time communication between the server and the client, enabling players to interact seamlessly within the game.

---

## Chapter 2: Architecture

The architecture of Socket Board Game follows a **client-server** model:
- **Client**: Built with ReactJS, responsible for handling the user interface, and communicating with the server via Socket.IO for real-time data exchange.
- **Server**: Flask is used to process game logic and manage player session connections.

---

## Chapter 3: Algorithm Flow and OOP Design

### Algorithm Flowchart
*Include your flowchart image or diagram here if necessary.*

### OOP Design
*Link to the detailed OOP design document or image.*

---

## Chapter 4: Backend Core

### Connection Handling
To ensure data integrity, each time a player connects or reconnects, the server maps the player’s session ID to maintain a stable connection.

### Authentication Handling
Each player maintains a unique ID on the client side, which is sent in each request. For optimization, the team used decorators to handle access rights.  
Example: The `join_room` function first passes through the `@user_information_filter` class to ensure proper access control.

### Data Storage Architecture
Since personal data storage is not necessary, we use a dictionary to store game-related data temporarily.

### Data Synchronization
Server-side objects are serialized into JSON format to be parsed by the client-side, ensuring smooth data transmission between Python and JavaScript.

---

## Chapter 5: Frontend Core

### React Hooks
React hooks are used effectively to ensure that the game state and data remain consistent across the application.

### Responsive UI
The UI is designed to be responsive, ensuring optimal gameplay experience on both desktop and mobile devices.

### Access Control
The frontend handles access control by restricting which rooms and actions players can interact with based on their roles.

### Module Pattern
The codebase follows a modular pattern, making it easy to add new game modules in the future.

---

## Chapter 6: Bot Module Core

### Alpha-Beta Pruning Algorithm (Minimax)
The bot AI is powered by the **alpha-beta pruning** algorithm, which optimizes the minimax algorithm to determine the best move for the bot.  

Example of Min function:

