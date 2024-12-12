# Guardians Gambit
This project implements a reinforcement learning-based multi-agent game that represents a heist scenario where a thief attempts to steal a cash bag from one of the rooms in the bank without being detected by the security camera or the security guard. While the security guard searches for the thief around the environment. Both agents use reinforcement learning algorithms and learn smart strategies as they get trained in the environment. As the two agents interact with the environment, they receive pre-defined rewards and penalties tied to each of their objectives. The progressive training enhances their decision-making and adaptability, showcasing the practical application of RL in dynamic, competitive scenarios.

Rewards and Penalties for the agents: Time penalty, Thief and cashbag, Terminal area, Camera range, Guard - Thief proximity

To play the main game:

1. Run main.py to play the user playable version of the game

2. Run train_thief.py to train the thief

3. Run train_guard.py to train the guard

4. Run train_agents.py to train both the agents


