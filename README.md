# Project Name: Board Game AI

## Overview
The "Board Game AI" project is a simulation of a strategic two-player board game with an integrated AI opponent. This AI, which employs the Minimax algorithm with alpha-beta pruning, deftly analyzes potential moves to optimize gameplay success. The entire application is hosted via a Flask-based API, allowing for robust interaction and versatile deployment options, including Docker.

### Features
- **AI Move Prediction**: The minimax function evaluates possible moves and determines the optimal path for the AI using recursive depth-first search enhanced by alpha-beta pruning.
- **User Interactivity**: The read_board_from_file function provides flexibility for users to load game states dynamically from external text files, allowing for quick setup changes.
- **Web-based API**: The Flask API endpoint /predict_move handles HTTP POST requests, interpreting the board state files and leveraging AI logic for move predictions.

## Table of Contents
1. [Installation](#installation)
2. [System Requirements](#system-requirements)
3. [Local Setup](#local-setup)
4. [Running the Application](#running-the-application)
5. [API Endpoints](#api-endpoints)
6. [Docker Deployment](#docker-deployment)
7. [File Structure](#file-structure)
8. [Development](#development)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)
11. [License](#license)

## Installation

### System Requirements
To ensure compatibility and performance, verify that your system meets the following specifications:
- **Operating System**: The library is supported on Windows, macOS, and Linux. Ensure that your OS is fully updated to the latest stable release for the best performance and security.
- **Python Version**: Ensure that Python 3.9 or later is installed. You can verify your Python version by running:
-  ```sh
    python --version
    ```
    or
    ```sh
    python3 --version
    ```
  - It's recommended to use the latest patch release of Python 3.9 for any bug fixes or performance improvements.
- **Python Package Manager**:
  - Ensure `pip` is updated to the latest version for smooth dependency installation. Update pip with:
    ```sh
    pip install --upgrade pip
    ```

- **Tools**:
  - **Git**: Used for version control and managing codebase changes. Ensure Git is installed and accessible from the command line, check it with:
    ```sh
    git --version
    ```
  - **Docker** (optional but recommended for deployment):
    - Docker version 20.10.0 or newer is recommended. Verify Docker’s installation by running:
      ```sh
      docker --version
      ```

- **Editor/IDE**:
  - A text editor or IDE with Python support is recommended for development, such as VSCode, PyCharm, or Sublime Text. Ensure it is configured for Python 3.9 development.

- **Network Access**:
  - Ensure that your environment allows network operations such as fetching packages from PyPI and accessing API endpoints during execution and testing.

### Dependencies
This project requires several Python libraries to function correctly:
- Flask
- Requests for testing
- OS for system interfacing

You can find a complete list of dependencies in `requirements.txt`.

## Local Setup

### Step 1: Clone the Repository
Begin by cloning the repository to your local machine using Git:
```bash
git clone https://github.com/rikaari/checkers_game_library/
cd checkers_game_library

### Step 2: Set Up a Virtual Environment
Create a virtual environment to ensure isolated and conflict-free package management:
```bash
python -m venv venv

Activate the virtual environment:
On Windows , use:
```bash
venv\Scripts\activate

On macOS  and Linux , use:
```bash
source venv/bin/activate



