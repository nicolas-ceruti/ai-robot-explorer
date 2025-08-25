
# Intelligent Explorer Robot

## About the Project

This project, developed as part of an Artificial Intelligence course, simulates the behavior of an autonomous robot in a grid-based environment. The main objective is to demonstrate and solidify the understanding of different intelligent agent typologies.

The agent's complexity evolves progressively through four stages, starting with a simple, memoryless reactive agent and advancing to a sophisticated utility-based agent that optimizes routes based on terrain costs.

## File Structure

The project is organized as follows to ensure modularity and clarity:

```
INTELLIGENT_ROBOT_PROJECT/
├── robo_explorer/
│   ├── __init__.py         # Makes the directory a Python package
│   ├── agents.py           # Contains the classes for all agents (Robots)
│   ├── environment.py      # Contains the class that manages the environment (grid, obstacles, etc.)
│   └── visualization.py    # Contains the class for dynamic visualization
├── main.py                 # Main script to run the simulations
└── requirements.txt        # Project dependency list
```

## Technologies Used

  * **Python 3.x**
  * **Matplotlib:** For the graphical visualization of the grid and the agent's behavior.
  * **NumPy:** As a dependency for Matplotlib for array manipulation.

## Environment Setup

Follow the steps below to set up and run the project on your local machine.

### Prerequisites

  * Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/).

### Installation

1.  **Clone the repository** (or simply download and unzip the files into a folder named `INTELLIGENT_ROBOT_PROJECT`).

2.  **Create the `requirements.txt` file** in the project's root directory (`INTELLIGENT_ROBOT_PROJECT/`) with the following content:

    ```
    matplotlib
    ```

3.  **Open a terminal** in the project's root folder.

4.  **Create a virtual environment** to isolate the project's dependencies:

    ```bash
    python -m venv venv
    ```

5.  **Activate the virtual environment:**

      * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
      * **On macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

6.  **Install the required libraries** from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

All simulations are controlled by the `main.py` file. To choose which stage of the simulation you want to visualize, edit the final block of the file.

1.  **Open the `main.py` file** in a code editor.

2.  **Navigate to the end of the file**, to the `if __name__ == "__main__":` block.

3.  **Uncomment the function for the stage you wish to run** and comment out the others. For example, to run Stage 2:

    ```python
    if __name__ == "__main__":
        # Choose which stage you want to visualize with an animation
        # execute_stage1()
        execute_stage2()
        # execute_stage3()
        # execute_stage4()
    ```

4.  **Run the script** from your terminal (with the virtual environment activated):

    ```bash
    python main.py
    ```

    A Matplotlib window will appear, showing the step-by-step simulation of the chosen stage.

## Description of Stages (Agents)

### Stage 1: Simple Reactive Agent

  * **Objective:** To find the 4 walls that delimit the grid.
  * **Logic:** The robot chooses a direction and moves in a straight line until it collides with a boundary. Upon collision, it registers the wall it found and chooses a new direction to continue its exploration. The environment has no internal obstacles.
<img width="785" height="703" alt="image" src="https://github.com/user-attachments/assets/dee5d26f-3ec2-4a1c-ab4d-a2113df21887" />


### Stage 2: Model-Based Reactive Agent

  * **Objective:** To explore as much of a map with obstacles as possible.
  * **Logic:** The agent uses a memory (`mapa_visitados`) to know where it has already been. It always prioritizes moving to adjacent cells that have not yet been visited. If all neighbors have already been visited, it moves to a random adjacent cell to try and "unblock" its path.
<img width="747" height="676" alt="image" src="https://github.com/user-attachments/assets/82ab9c96-c0c2-4a62-b963-abe370ed212f" />


### Stage 3: Goal-Based Agent

  * **Objective:** To find the shortest path (in number of steps) between a random start point and a random end point.
  * **Logic:** The agent receives the complete map with obstacles beforehand. It uses the **A\* (A-Star)** algorithm to calculate the optimal route before moving. The animation shows the robot executing the pre-planned path.
<img width="678" height="671" alt="image" src="https://github.com/user-attachments/assets/9149b2da-c33a-4029-b10d-f46e0d195bf3" />

### Stage 4: Utility-Based Agent

  * **Objective:** To find the path of **least total cost** between a start and end point, on a map with different types of terrain.
  * **Logic:** Similar to Stage 3, the agent uses the A\* algorithm, but the cost function is modified. Each step is not worth "1", but rather the cost value of the target terrain cell (e.g., 1 for normal, 2 for sandy, 3 for rocky). This may cause the robot to choose a path that is longer in steps to avoid expensive terrain.
<img width="710" height="674" alt="image" src="https://github.com/user-attachments/assets/edaadf21-da6c-45f1-9d21-3233667be83e" />
