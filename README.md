# Guardians Gambit
This project implements a reinforcement learning-based multi-agent game that represents a heist scenario where a thief attempts to steal a cash bag from one of the rooms in the bank without being detected by the security camera or the security guard. While the security guard searches for the thief around the environment. Both agents use reinforcement learning algorithms and learn smart strategies as they get trained in the environment. As the two agents interact with the environment, they receive pre-defined rewards and penalties tied to each of their objectives. The progressive training enhances their decision-making and adaptability, showcasing the practical application of RL in dynamic, competitive scenarios.

Rewards and Penalties for the agents: Time penalty, Thief and cashbag, Terminal area, Camera range, Guard - Thief proximity

To play the main game:

1. Run main.py to play the user playable version of the game

2. Thief movements - Arrow keys

3. Guard movements - W A S D keys

4. Play the game by following step 1 and get familiar with the environment.

5. env.py is where the environment to train the agents has been set up.

6. To train both the agents efficiently, we trained the thief first having the guard move randomly.

7. To train the thief, run train_thief.py

8. Once the thief is acting smart and gaining more positive rewards compared to getting penalized, we train the guard.

9. The guard is trained with the thief moving according to the thief's Q table.

10. To train the guard, run train_guard.py.

11. This way the Q table of the thief is not being updated and the Q table of the guard is being updated.

12. Now to train both the agents simultaneously, run train_agents.py, and both the agents will be trained simultaneously and their Q table updated simultaneously as well.