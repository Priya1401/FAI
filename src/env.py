import gym
import math
from gym import spaces
import numpy as np
import pygame
import pygame.sprite
from main import *
from cashbag import *

class GuardiansGambitEnv(gym.Env):
    def __init__(self):
        super(GuardiansGambitEnv, self).__init__()

        # Initialize the game
        self.game = Game()
        self.game.running = False  # Disable game loop for training

        self.action_space = spaces.Discrete(4)  # Action space: up, down, left, right
        self.observation_space = spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)

        # Reward variables
        self.game.cashbag_collected = False
        self.thief_reward = 0
        self.guard_reward = 0
        self.prev_thief_pos = None  
        self.prev_guard_pos = None

        # Time penalty variables
        self.thief_timer = 0  # Timer for Thief's time in the same area
        self.guard_timer = 0  # Counter for time in the same area
        self.time_penalty_threshold = 5  # Time threshold for applying penalty (in seconds)
        self.last_timer_update = pygame.time.get_ticks()  # Time of the last update

        self.prev_thief_reward = 0.0
        self.prev_guard_reward = 0.0

        self.last_reward_update_time = pygame.time.get_ticks()
        self.reward_updated = False
    
    def reset(self):
        # Reset the game state for a new episode
        self.game = Game()
        self.thief_reward = 0
        self.guard_reward = 0
        self.same_area_timer = 0
        self.last_timer_update = pygame.time.get_ticks()
        self.game.running = False
        self.game.cashbag_collected = False
        self.game.thief.rect.topleft = (80, 400)  # Reset Thief's position
        self.game.guard.rect.topleft = (670, 400)  # Reset Guard's position
        cash_bag_position = (545, 700)  # Reset Cashbag position
        Cashbag(cash_bag_position, (self.game.all_sprites, self.game.cashbag))

        self.prev_thief_pos = self.game.thief.rect.topleft  # Initialize previous Thief position
        self.prev_guard_pos = self.game.guard.rect.topleft  # Initialize previous Guard position
        done = self.check_game_over()
        return self.get_observation(), self.thief_reward, done, {}

    def step(self, thief_action=None, guard_action=None):
        dt = self.game.clock.tick() / 1000.0  # Time delta for updating the game state

        if thief_action is not None:
            self.process_thief_action(thief_action, dt)
        if guard_action is not None:
            self.process_guard_action(guard_action, dt)
        self.game.all_sprites.update(dt)

        # Check if the reward has changed
        current_reward = self.thief_reward + self.guard_reward
        if current_reward != self.prev_thief_reward + self.prev_guard_reward:
            self.last_reward_update_time = pygame.time.get_ticks()
            self.reward_updated = True
            self.prev_thief_reward = self.thief_reward
            self.prev_guard_reward = self.guard_reward
        else:
            self.reward_updated = False

        # Apply the time penalty if no reward update has occurred within 5 seconds
        if not self.reward_updated:
            current_time = pygame.time.get_ticks()
            time_since_last_update = (current_time - self.last_reward_update_time) / 1000.0  # in seconds
            if time_since_last_update >= 15:
                print("Time penalty applied! No reward update for 5 seconds.")
                self.thief_reward -= 0.30
                self.guard_reward -= 0.30
                self.last_reward_update_time = current_time  # Reset the timer

        done = self.check_game_over()
        self.calculate_rewards()

        # Update time penalty
        self.apply_time_penalty()


        # Return the new observation, reward, done, and additional info
        return self.get_observation(), self.thief_reward, self.guard_reward, done, {}


    def apply_time_penalty_dist(self):
        """Apply a time penalty if the Thief and Guard stay in the same area for too long."""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_timer_update) / 1000.0  # Convert to seconds

        # Check if Thief and Guard are in the same area
        thief_pos = self.game.thief.rect.topleft
        guard_pos = self.game.guard.rect.topleft

        
        area_size = 400  
        same_area = (
            abs(thief_pos[0] - guard_pos[0]) <= area_size and
            abs(thief_pos[1] - guard_pos[1]) <= area_size
        )

        if same_area:
            self.same_area_timer += elapsed_time
        else:
            self.same_area_timer = 0  # Reset timer if they leave the area

        # Apply penalty if they remain in the same area for too long
        if self.same_area_timer >= self.time_penalty_threshold:
            print(f"Time penalty applied! Thief and Guard stayed in the same area for {self.same_area_timer:.2f} seconds.")
            self.thief_reward -= 0.5
            self.guard_reward -= 0.5
            self.same_area_timer = 0  # Reset timer after applying penalty

        self.last_timer_update = current_time

    def apply_time_penalty(self):
        """Apply time penalties if the Thief or Guard stay in their respective 300x300 areas for too long."""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_timer_update) / 1000.0  # Convert to seconds

        thief_pos = self.game.thief.rect.topleft
        guard_pos = self.game.guard.rect.topleft

        # Define the 300x300 grid boundaries for the Thief and Guard
        thief_area = (thief_pos[0] - 150, thief_pos[1] - 150, 300, 300)
        guard_area = (guard_pos[0] - 150, guard_pos[1] - 150, 300, 300)

        # Check if the Thief is within its grid for too long
        if (thief_area[0] <= thief_pos[0] <= thief_area[0] + 300 and
            thief_area[1] <= thief_pos[1] <= thief_area[1] + 300):
            self.thief_timer += elapsed_time
        else:
            self.thief_timer = 0  # Reset timer if Thief leaves the area

        # Check if the Guard is within its grid for too long
        if (guard_area[0] <= guard_pos[0] <= guard_area[0] + 300 and
            guard_area[1] <= guard_pos[1] <= guard_area[1] + 300):
            self.guard_timer += elapsed_time
        else:
            self.guard_timer = 0  # Reset timer if Guard leaves the area

        # Apply penalty if they remain in their areas for too long
        if self.thief_timer >= self.time_penalty_threshold:
            print(f"Thief penalty applied! Thief stayed in its area for {self.thief_timer:.2f} seconds.")
            self.thief_reward -= 0.6  # Penalty for staying too long
            self.thief_timer = 0  # Reset timer after applying penalty

        if self.guard_timer >= self.time_penalty_threshold:
            print(f"Guard penalty applied! Guard stayed in its area for {self.guard_timer:.2f} seconds.")
            self.guard_reward -= 0.6  # Penalty for staying too long
            self.guard_timer = 0  # Reset timer after applying penalty

        self.last_timer_update = current_time

    
    def step_guard(self, action):
        dt = self.game.clock.tick() / 1000.0
        self.process_guard_action(action, dt)
        self.process_thief_action(action, dt)

        # self.game.guard.update(dt)
        self.game.all_sprites.update(dt)

        done = self.check_game_over()

        self.calculate_rewards()

        # Return the new observation, reward, done, and info
        return self.get_observation(), self.guard_reward, done, {}

    def process_thief_action(self, action, dt):
        if action == 0:  # Thief moves up
            self.game.thief.direction.x = 0
            self.game.thief.direction.y = -1
        elif action == 1:  # Thief moves down
            self.game.thief.direction.x = 0
            self.game.thief.direction.y = 1
        elif action == 2:  # Thief moves left
            self.game.thief.direction.x = -1
            self.game.thief.direction.y = 0
        elif action == 3:  # Thief moves right
            self.game.thief.direction.x = 1
            self.game.thief.direction.y = 0
        
        # Move the thief with the given direction and time delta
        self.game.thief.move(dt)


        # Process the guard's chosen action
    def process_guard_action(self, action, dt):
        if action == 0:  # Guard moves up
            self.game.guard.direction.x = 0
            self.game.guard.direction.y = -1
        elif action == 1:  # Guard moves down
            self.game.guard.direction.x = 0
            self.game.guard.direction.y = 1
        elif action == 2:  # Guard moves left
            self.game.guard.direction.x = -1
            self.game.guard.direction.y = 0
        elif action == 3:  # Guard moves right
            self.game.guard.direction.x = 1
            self.game.guard.direction.y = 0

        # Move the guard with the given direction and time delta
        self.game.guard.move(dt)

    def check_game_over(self):
        if pygame.sprite.spritecollide(self.game.thief, self.game.guard_sprite, False):
            print("Thief caught by the Guard")
            self.thief_reward -= 100  # Thief is caught by the guard
            self.guard_reward +=100
            return True

        if self.game.is_thief_in_terminal_area() and self.game.cashbag_collected:
            print("Thief reached the terminal area with cashbag")
            self.thief_reward += 100
            self.guard_reward -= 100
            return True

        return False


    def calculate_rewards(self):
        thief_x, thief_y = self.game.thief.rect.topleft
        guard_x, guard_y = self.game.guard.rect.topleft
        cashbag_x, cashbag_y = 545, 700

        # Reward for taking the cashbag
        if not self.game.cashbag_collected and pygame.sprite.spritecollide(self.game.thief, self.game.cashbag, True):
            print("Thief reached cashbag! Cashbag removed.")
            self.thief_reward +=50
            self.game.cashbag_collected = True


        if not self.game.cashbag_collected:
            current_distance_to_cashbag = math.hypot(thief_x - cashbag_x, thief_y - cashbag_y)
            previous_distance_to_cashbag = math.hypot(self.prev_thief_pos[0] - cashbag_x, self.prev_thief_pos[1] - cashbag_y)
            threshold = 100  # Set the threshold value as needed

            # Check if there is an object in between or the distance exceeds the threshold
            if not self.noObjectInBetween(cashbag_x, cashbag_y, self.game.thief.rect.center) or current_distance_to_cashbag > threshold:
                print("No reward: Object in between or distance exceeds threshold.")
                self.thief_reward += 0  # Explicitly adding 0 for clarity
            else:
                if current_distance_to_cashbag < previous_distance_to_cashbag:
                    print("Thief is moving closer to the cashbag.")
                    self.thief_reward += 1
                else:
                    print("Thief is moving away from the cashbag.")
                    self.thief_reward -= 2


        # Check if Thief is at the terminal area
        if self.game.is_thief_in_terminal_area():
            self.thief_reward += 5  # Thief reaches terminal without cashbag

        if self.game.thief.rect.colliderect(self.game.camera_range.rect):
            self.thief_reward -= 10

        movement_reward = self.check_proximity_and_movement(self.prev_thief_pos[0], self.prev_thief_pos[1], guard_x, guard_y)
        self.thief_reward += movement_reward
        self.guard_reward -= movement_reward

        # Update the previous Thief position
        self.prev_thief_pos = (thief_x, thief_y)

    def check_proximity_and_movement(self, prev_x, prev_y, guard_x, guard_y):
        """Calculate reward based on the Thief's movement relative to the Guard."""
        current_distance = math.hypot(self.game.thief.rect.x - guard_x, self.game.thief.rect.y - guard_y)
        previous_distance = math.hypot(prev_x - guard_x, prev_y - guard_y)
        threshold = 200  # Distance threshold

        if current_distance < threshold:
            if self.noObjectInBetween(guard_x, guard_y, self.game.thief.rect.center):
                if current_distance < previous_distance:
                    print("Thief is moving closer to the Guard within the threshold")
                    return -3  # Penalty
                elif current_distance > previous_distance:
                    print("Thief is moving away from the Guard within the threshold")
                    return 3  # Reward
            else:
                print("There is an object in between the Guard and Thief")
                return 0  # No reward/penalty due to an object in between
        else:
            print("Thief is outside the threshold")
            return 0  # No reward/penalty
        return 0



    def get_observation(self):
        thief_pos = self.game.thief.rect.topleft if hasattr(self.game.thief.rect, 'topleft') else (0, 0)
        guard_pos = self.game.guard.rect.topleft if hasattr(self.game.guard.rect, 'topleft') else (0, 0)
        cashbag_status = 1 if self.game.cashbag_collected else 0


        return np.array([thief_pos[0], thief_pos[1], guard_pos[0], guard_pos[1], cashbag_status], dtype=np.float32)


    def render(self):
        self.game.display_surface.fill('black')
        self.game.all_sprites.draw(self.game.display_surface)
        pygame.display.update()

    def close(self):
        pygame.quit()

    def noObjectInBetween(self, guard_x, guard_y, thief_center):
        """Check if there is an obstacle between the Guard and the Thief."""
        thief_x, thief_y = thief_center

        # Create a line vector between the Guard and the Thief
        line = pygame.math.Vector2(thief_x - guard_x, thief_y - guard_y)
        direction = line.normalize()  # Normalize to get a direction vector
        steps = int(line.length())  # Number of steps based on distance

        # Step along the line and check for collisions
        for step in range(steps):
            # Calculate the position to check
            check_x = int(guard_x + direction.x * step)
            check_y = int(guard_y + direction.y * step)

            # Check if the point collides with any of the collision sprites
            for sprite in self.game.collision_sprites:
                if sprite != self.game.cashbag and sprite.rect.collidepoint(check_x, check_y):
                    return False # An obstacle is blocking the line of sight

        return True  # No obstacle found
