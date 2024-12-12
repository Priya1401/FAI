import numpy as np
import time
from env import GuardiansGambitEnv

# Hyperparameters
ALPHA = 0.3        # Learning rate
GAMMA = 0.9        # Discount factor
EPSILON = 1.0      # Exploration rate (for epsilon-greedy strategy)
EPISODES = 5000     # Number of episodes for training
DECAY_RATE = 0.999995  # Decay rate for epsilon
THIEF_Q_TABLE_FILE = "thief_q_table.npy"
GUARD_Q_TABLE_FILE = "guard_q_table.npy"

def save_q_table(file_path, q_table):
    """Save the Q-table to a file."""
    np.save(file_path, q_table)
    print(f"Q-table saved to '{file_path}'.")

def load_q_table(file_path):
    """Load the Q-table from a file."""
    try:
        q_table = np.load(file_path, allow_pickle=True).item()
        print(f"Q-table loaded from '{file_path}'.")
        return q_table
    except FileNotFoundError:
        print(f"No existing Q-table found. Starting from scratch.")
        return {}

def discretize_state(state):
    thief_x, thief_y, guard_x, guard_y, cashbag_status = state
    thief_x = int(thief_x // 10)
    thief_y = int(thief_y // 10)
    guard_x = int(guard_x // 10)
    guard_y = int(guard_y // 10)
    return thief_x * 10000 + thief_y * 1000 + guard_x * 100 + guard_y * 10 + cashbag_status

def train_agents():
    global EPSILON
    env = GuardiansGambitEnv()

    # Load or initialize Q-tables
    thief_q_table = load_q_table(THIEF_Q_TABLE_FILE)
    guard_q_table = load_q_table(GUARD_Q_TABLE_FILE)

    num_update_count_thief = {}
    num_update_count_guard = {}

    for episode in range(EPISODES):
        obs, _, done, _ = env.reset()
        done = False
        state = discretize_state(obs)

        if state not in thief_q_table:
            thief_q_table[state] = np.zeros(env.action_space.n)
            for action in range(env.action_space.n):
                num_update_count_thief[(state, action)] = 0

        if state not in guard_q_table:
            guard_q_table[state] = np.zeros(env.action_space.n)
            for action in range(env.action_space.n):
                num_update_count_guard[(state, action)] = 0

        step_count = 0

        while not done:
            step_count += 1

            # Thief chooses an action
            if np.random.uniform(0, 1) < EPSILON:
                thief_action = np.random.choice(env.action_space.n)
            else:
                thief_action = np.argmax(thief_q_table[state])

            # Guard chooses an action
            if np.random.uniform(0, 1) < EPSILON:
                guard_action = np.random.choice(env.action_space.n)
            else:
                guard_action = np.argmax(guard_q_table[state])

            print(thief_action, guard_action)

            # Execute both actions in the environment
            obs, thief_reward, guard_reward, done, _ = env.step(thief_action, guard_action)

            print("Thief Reward:", thief_reward, "Guard Reward:",guard_reward)

            next_state = discretize_state(obs)

            if next_state not in thief_q_table:
                thief_q_table[next_state] = np.zeros(env.action_space.n)
                for action in range(env.action_space.n):
                    num_update_count_thief[(next_state, action)] = 0

            if next_state not in guard_q_table:
                guard_q_table[next_state] = np.zeros(env.action_space.n)
                for action in range(env.action_space.n):
                    num_update_count_guard[(next_state, action)] = 0

            if (state, thief_action) not in num_update_count_thief:
                num_update_count_thief[(state, thief_action)] = 0

            if (state, guard_action) not in num_update_count_guard:
                num_update_count_guard[(state, guard_action)] = 0

                    # Update Q-values for thief
            eta_thief = 1 / (1 + num_update_count_thief[(state, thief_action)])
            max_next_q_thief = np.max(thief_q_table[next_state])
            thief_q_table[state][thief_action] = (
                (1 - eta_thief) * thief_q_table[state][thief_action] + eta_thief * (thief_reward + GAMMA * max_next_q_thief)
            )
            num_update_count_thief[(state, thief_action)] += 1

            # Update Q-values for guard
            eta_guard = 1 / (1 + num_update_count_guard[(state, guard_action)])
            max_next_q_guard = np.max(guard_q_table[next_state])
            guard_q_table[state][guard_action] = (
                (1 - eta_guard) * guard_q_table[state][guard_action] + eta_guard * (guard_reward + GAMMA * max_next_q_guard)
            )
            num_update_count_guard[(state, guard_action)] += 1

            # Move to the next state
            state = next_state

            env.render()  # Optional: Render the environment
            time.sleep(0.1)  # Optional: Pause for visualization

        EPSILON = max(EPSILON * DECAY_RATE, 0.01)

        print(f"Episode {episode + 1}/{EPISODES} - Steps: {step_count}")

        # Save Q-tables periodically
        if (episode + 1) % 100 == 0:
            save_q_table(THIEF_Q_TABLE_FILE, thief_q_table)
            save_q_table(GUARD_Q_TABLE_FILE, guard_q_table)

    # Save final Q-tables
    save_q_table(THIEF_Q_TABLE_FILE, thief_q_table)
    save_q_table(GUARD_Q_TABLE_FILE, guard_q_table)
    print("Training complete!")

if __name__ == "__main__":
    train_agents()