import numpy as np
import random
import time
from env import GuardiansGambitEnv

# Hyperparameters for Q-learning
ALPHA = 0.3        # Learning rate
GAMMA = 0.9         # Discount factor
EPSILON = 1.0       # Exploration rate (for epsilon-greedy strategy)
EPISODES = 1       # Number of episodes for training
Q_TABLE_FILE = "guard_q_table.npy"  # File to save/load Q-table
DECAY_RATE = 0.999995  # Decay rate for epsilon
def save_q_table(file_path, q_table):
    """Save the Q-table to a file."""
    np.save(file_path, q_table)
    print(f"Q-table saved to '{file_path}'.")
    # log_q_table_size(len(q_table), "save")

def load_q_table(file_path):
    """Load the Q-table from a file."""
    try:
        q_table = np.load(file_path, allow_pickle=True).item()
        print(f"Q-table loaded from '{file_path}'.")
        # log_q_table_size(len(q_table), "save")
        return q_table
    except FileNotFoundError:
        print(f"No existing Q-table found. Starting from scratch.")
        return {}

def train_guard():
    """Train the Guard using Q-learning while the Guard moves randomly and the Thief acts according to its Q-table."""
    global EPSILON  # Declare EPSILON as global to modify it within this function

    env = GuardiansGambitEnv()

    # Load the existing Q-table for the Guard or initialize it if it doesn't exist
    Q_table = load_q_table(Q_TABLE_FILE)
    num_update_count = {}

    # Load the Thief's Q-table
    thief_q_table = load_q_table("thief_q_table.npy")
    
    for episode in range(EPISODES):
        # Reset the environment for each episode
        obs, reward, done, info = env.reset()  # Reset and get the initial state
        done = False

        # Convert the initial state to a discrete representation
        state = discretize_state(obs)

        if state not in Q_table:
            Q_table[state] = np.zeros(env.action_space.n)
            for action in range(env.action_space.n):
                num_update_count[(state, action)] = 0

        step_count = 0  # To limit the number of steps in an episode
        total_reward = 0  # Initialize total reward for this episode

        while not done:
            step_count += 1
            # Choose an action for the Guard using epsilon-greedy strategy
            if np.random.uniform(0, 1) < EPSILON:
                action = np.random.choice(env.action_space.n)  # Explore
            else:
                action = np.argmax(Q_table[state])  # Exploit

            # Get the current state for the Thief and decide its action based on its Q-table
            thief_state = discretize_state(obs)  # Assuming `obs` is Thief's state representation
            if thief_state in thief_q_table:
                thief_action = np.argmax(thief_q_table[thief_state])  # Exploit
            else:
                thief_action = np.random.choice(env.action_space.n)  # Explore

            # Take the chosen action for the Guard and Thief
            obs, reward, done, info = env.guard_step(action, thief_action)

            # Convert the next state to a discrete representation
            next_state = discretize_state(obs)

            if next_state not in Q_table:
                Q_table[next_state] = np.zeros(env.action_space.n)
                for a in range(env.action_space.n):
                    num_update_count[(next_state, a)] = 0

            # Initialize num_update_count if the state-action pair is not present
            if (state, action) not in num_update_count:
                num_update_count[(state, action)] = 0  # Initialize if not present

            # Dynamic learning rate
            eta = 1 / (1 + num_update_count[(state, action)])

            # Q-value update using the Q-learning update rule
            max_next_q = np.max(Q_table[next_state])
            Q_table[state][action] = (
                (1 - eta) * Q_table[state][action] + eta * (reward + GAMMA * max_next_q)
            )

            num_update_count[(state, action)] += 1

            # Move to the next state
            state = next_state
            env.render()  # Optional: render the environment to visualize the training
            time.sleep(0.1)  # Optional: pause for better visualization
            print(f"Episode {episode + 1}/{EPISODES}, Step {step_count} - State: {state}, Action: {action}, Reward: {reward}, Done: {done}")

        EPSILON = max(EPSILON * DECAY_RATE, 0.01)

        print(f"Episode {episode + 1}/{EPISODES} - Total Reward: {reward}")

        if (episode + 1) % 100 == 0:
            save_q_table(Q_TABLE_FILE, Q_table)
            print("Saved Qtable after 100 episodes")

    # Save the final trained Q-table
    save_q_table(Q_TABLE_FILE, Q_table)
    print(f"Training complete! Q-table saved to '{Q_TABLE_FILE}'.")

def discretize_state(state):
    """
    Convert a continuous state into a discrete state for use in the Q-table.
    """
    thief_x, thief_y, guard_x, guard_y, cashbag_status = state
    thief_x = int(thief_x // 10)
    thief_y = int(thief_y // 10)
    guard_x = int(guard_x // 10)
    guard_y = int(guard_y // 10)
    return thief_x * 10000 + thief_y * 1000 + guard_x * 100 + guard_y * 10 + cashbag_status


if __name__ == "__main__":
    train_guard()
