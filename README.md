# Project Name: Board Game AI
**Author: Ntwari Regan 2021/BSE/134/PS**

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
```

### Step 2: Set Up a Virtual Environment
Create a virtual environment to ensure isolated and conflict-free package management:
```bash
python -m venv venv
```

Activate the virtual environment:
On Windows , use:
```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies
Once the virtual environment is activated, install the required Python packages listed in **requirements.txt**:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
Start the Flask application by executing:
```bash
cd minimax_library
cd api
python api/app.py
```
### Important Configuration Note
> **Warning:** Before proceeding with running or testing the application, ensure that the file paths in your scripts are correct. This is essential to avoid runtime errors.
> When you are testing the Flask application directly on your machine (without Docker or Podman), ensure your file paths reflect the actual location on your local filesystem. Coonfigure this variable in your **test_api.py** file:

```python
data = {"filename": "/home/rika/Desktop/board1.txt"}
```

###  Step 5: Test the Flask Application 
To verify that your application is running correctly, use the **test_api.py script.** This script should be executed in a new terminal window  while the Flask app is running in the previous one. 
Open a new terminal window.
Navigate to the project directory, **/checkers_game_library/minimax_library/api** (if not already there).
Run the test script to execute predefined API tests:
```bash
python test_api.py
```

###  Step 6: Configure Docker for Deployment
After verifying that your Flask application is working correctly with the test script test_api.py, you can proceed to set up Docker for your application. The **Dockerfile** allows you to package your application and all of its dependencies into a container, ensuring consistency across different environments.
Here’s a basic example:
```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .
```
###  Step 6.2: Build the Docker Image
Run the following command in your terminal to build the Docker image:
```bash
docker build -t minimax .
```
This command will package your application into an image tagged with minimax.
> **Warning:** Before proceeding with running or testing the docker, ensure that the file paths in your scripts are correct. This is essential to avoid runtime errors.
> When you are testing with Docker or Podman, ensure your file paths reflect the actual location on your local filesystem. Coonfigure this variable in your **test_api.py** file:

```python
data = {"filename": "/host_files/board1.txt"}
```

###  Step 6.3: Run the Docker Container
Start the Docker container using the following command:
> **Warning:** Before starting the Docker container, ensure that your local Flask application is not running. This is crucial to avoid port conflicts, as both processes use the same port (5000).
```bash
podman run -p 5000:5000 -v /home/rika/Desktop:/host_files minimax
```
This command maps port 5000 of the container to port 5000 on your host machine, allowing external access.

###  Step 6.4: Verify Container Deployment
To ensure the Docker container is working properly, open a web browser to access your application:
Visit
```bash
http://127.0.0.1:5000/
```
Run a test similar to **test_api.py** against the Dockerized application to confirm all API endpoints are functioning as expected.
```bash
python test_api.py
```

Here's an example of what the script might print if everything is working as expected:
```bash
Status Code: 200
Response JSON: {
  "best_move": {
    "from": "A2",
    "to": "B3"
  },
  "board": [
    ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
    ["   ", " o ", "   ", "   ", "   ", "   ", "   ", "   "],
    ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
    ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
    ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
    ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
    ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
    ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "]
  ]
}
```
###  Check Logs and Outputs
```bash
docker logs <container_id>
```
Replace <container_id> with the actual container ID, which can be found using docker ps.

###  Stop the Docker Container (Optional)
Once you've tested the application, you may stop the container by running:
```bash
docker stop <container_name_or_id>
```
