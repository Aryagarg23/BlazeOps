import numpy as np
import random
import matplotlib.pyplot as plt
import time

def rothermel_fire_spread(wind_speed, fuel_moisture, slope):
    # Simplified version of Rothermel's fire spread formula
    return max(0.1, 0.001 * wind_speed * (1 - fuel_moisture) * (1 + 0.2 * slope))

class FireRescueEnv:
    def __init__(self, grid_size=(10, 10), num_firefighters=3, num_civilians=5, fire_spread_prob=0.3, wind_speed=5, fuel_moisture=0.2, slope=0):
        self.grid_size = grid_size
        self.num_firefighters = num_firefighters
        self.num_civilians = num_civilians
        self.fire_spread_prob = fire_spread_prob
        self.wind_speed = wind_speed
        self.fuel_moisture = fuel_moisture
        self.slope = slope
        self.reset()
    
    def reset(self):
        # Initialize empty grid
        self.grid = np.zeros(self.grid_size, dtype=int)
        
        # Place fire (marked as 2)
        self.fire_positions = set()
        for _ in range(random.randint(1, 3)):
            x, y = random.randint(0, self.grid_size[0]-1), random.randint(0, self.grid_size[1]-1)
            self.grid[x, y] = 2
            self.fire_positions.add((x, y))
        
        # Place civilians (marked as 3)
        self.civilian_positions = set()
        while len(self.civilian_positions) < self.num_civilians:
            x, y = random.randint(0, self.grid_size[0]-1), random.randint(0, self.grid_size[1]-1)
            if self.grid[x, y] == 0:
                self.grid[x, y] = 3
                self.civilian_positions.add((x, y))
        
        # Place firefighters (marked as 1)
        self.firefighter_positions = []
        while len(self.firefighter_positions) < self.num_firefighters:
            x, y = random.randint(0, self.grid_size[0]-1), random.randint(0, self.grid_size[1]-1)
            if self.grid[x, y] == 0:
                self.grid[x, y] = 1
                self.firefighter_positions.append((x, y))
        
        return self.grid
    
    def step(self, actions):
        new_firefighter_positions = []
        for i, (x, y) in enumerate(self.firefighter_positions):
            action = actions[i]
            new_x, new_y = x, y
            
            if action == 'UP' and x > 0:
                new_x -= 1
            elif action == 'DOWN' and x < self.grid_size[0] - 1:
                new_x += 1
            elif action == 'LEFT' and y > 0:
                new_y -= 1
            elif action == 'RIGHT' and y < self.grid_size[1] - 1:
                new_y += 1
            elif action == 'EXTINGUISH' and (x, y) in self.fire_positions:
                self.fire_positions.remove((x, y))
                self.grid[x, y] = 0
            elif action == 'RESCUE' and (x, y) in self.civilian_positions:
                self.civilian_positions.remove((x, y))
                self.grid[x, y] = 0
                
            new_firefighter_positions.append((new_x, new_y))
        
        self.firefighter_positions = new_firefighter_positions
        self._spread_fire()
        return self.grid
    
    def _spread_fire(self):
        new_fire_positions = set()
        spread_rate = rothermel_fire_spread(self.wind_speed, self.fuel_moisture, self.slope)
        for x, y in self.fire_positions:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size[0] and 0 <= ny < self.grid_size[1]:
                    if self.grid[nx, ny] != 2 and random.random() < spread_rate:  # Fire spreads to any non-fire tile
                        new_fire_positions.add((nx, ny))
        self.fire_positions.update(new_fire_positions)
        for x, y in new_fire_positions:
            self.grid[x, y] = 2
    
    def render(self):
        plt.ion()
        for _ in range(50):  # Simulate 50 steps
            self._spread_fire()
            color_map = {0: 'white', 1: 'blue', 2: 'red', 3: 'green'}
            colored_grid = np.zeros((*self.grid.shape, 3))
            
            for x in range(self.grid.shape[0]):
                for y in range(self.grid.shape[1]):
                    if self.grid[x, y] == 1:
                        colored_grid[x, y] = [0, 0, 1]  # Blue for firefighters
                    elif self.grid[x, y] == 2:
                        colored_grid[x, y] = [1, 0, 0]  # Red for fire
                    elif self.grid[x, y] == 3:
                        colored_grid[x, y] = [0, 1, 0]  # Green for civilians
                    else:
                        colored_grid[x, y] = [1, 1, 1]  # White for empty spaces
            
            plt.imshow(colored_grid)
            plt.xticks([])
            plt.yticks([])
            plt.pause(0.5)
            plt.clf()
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    env = FireRescueEnv()
    env.render()
