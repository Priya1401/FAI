# Guardians Gambit
This project implements a reinforcement learning-based multi-agent game that represents a heist scenario where a thief attempts to steal a cash bag from one of the rooms in the bank without being detected by the security camera or the security guard. While the security guard searches for the thief around the environment. Both agents use reinforcement learning algorithms and learn smart strategies as they get trained in the environment. As the two agents interact with the environment, they receive pre-defined rewards and penalties tied to each of their objectives. The progressive training enhances their decision-making and adaptability, showcasing the practical application of RL in dynamic, competitive scenarios.

Rewards and Penalties for the agents: Time penalty, Thief and cashbag, Terminal area, Camera range, Guard - Thief proximity 

The project successfully demonstrates the application of reinforcement learning in a competitive, goal-driven multi agent game. Each of the agents interacted with the environment through actions and learnt to achieve the winning state quicker than the initial phases. The training of each agent in different positions also resulted in a good improvement in the agent’s decision making. While this project showcases the potential of reinforcement learning in creating intelligent agents capable of learning and navigating through a complex map, there have also been significant challenges while training and testing the agents. Each
episode in the initial training ran longer than usual, since each movement had to be rendered on UI. The tweaking of the environment sometimes resulted in restarting the training with new Q-tables. There were challenges with the agent trying to detect collisions since the map contains multiple obstacles. While there is always a scope for improving the behavior of the agent by training them for more iterations and fine tuning the parameters, the results observed at this stage have shown a good improvement in the behavior of the agents.

To play the main game:

1. Run main.py to start the game

2. Guard movements - W A S D keys

3. Thief movements - Arrow keys
