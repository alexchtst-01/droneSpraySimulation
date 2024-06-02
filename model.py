import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from tqdm import tqdm

class sprayAircraft:
    def __init__(self, farm_size, simulation_result_dir=None, savingMode=False, planeSize=25, distance=0, planeHeight=10):
        self.simulation_result_dir = simulation_result_dir
        self.savingMode = savingMode
        
        self.LOWEST = 0
        self.PLANE = 1
        self.HARVEST = 9
        self.HIGHEST = 10
        
        self.frameStore = []
        self.farmGrids = []
        self.size = farm_size
        self.planeSize = planeSize
        self.planeHeight = planeHeight
        
        self.initial_frame = np.ones(shape=(self.size, self.size)) * self.HARVEST
        self.__temp = np.ones(shape=(self.size, self.size)) * self.HARVEST
        self.farm = np.ones(shape=(self.size, self.size)) * self.HARVEST
        self.dist = distance
        
        if self.planeSize < 12:
            print("minimun size of the plane in 12")
        
    
    def __RandomWalk(self, arr, xpos, ypos):
        grid = arr.copy()
        if random.random() < 0.5:
            if random.random() < 0.5:
                xpos = max(0, min(self.size-1, xpos+1))
            else:
                xpos = max(0, min(self.size-1, xpos-1))
        else:
            if random.random() < 0.5:
                ypos = max(0, min(self.size-1, ypos+1))
            else:
                ypos = max(0, min(self.size-1, ypos-1))
        
        grid[ypos-1:ypos+1, xpos-1:xpos+1] -= 0.05
        
        return grid, xpos, ypos
    
    def __movePlane(self, arr, xpos, ypos):
        s = self.planeSize // 2
        temp = arr.copy()
        # badan pesawat
        temp[ypos-s:ypos+s-2, xpos-int(s*0.2):xpos+int(s*0.2)] = self.PLANE
        # sayap pesawat
        temp[ypos-3:ypos-1, xpos-s:xpos+s] = self.PLANE
        temp[ypos-2:ypos, xpos-s-1:xpos+s+1] = self.PLANE
        temp[ypos-1:ypos+1, xpos-s-1:xpos+s+1] = self.PLANE
        # ekor pesawat
        temp[ypos+s-2:ypos+s-1, xpos-s//3:xpos+s//3] = self.PLANE
        temp[ypos+s-1:ypos+s, xpos-s//2:xpos+s//2] = self.PLANE

        return temp
    
    def runSimulation(self, num_plane, state, vel=3, steps=200):
        for i in tqdm(range(steps - self.planeSize - 1)):
            yplane = max((self.size - self.planeSize) - i*vel, self.planeSize)
            xcoodinates = []
            for n in range(num_plane):
                xcoodinates.append(int(self.size * (n+1) / (num_plane + 1)))
            
            f = self.__movePlane(self.__temp, xcoodinates[0], yplane)
            for j in range(1, num_plane):
                f = self.__movePlane(f, xcoodinates[j], yplane)
            
            for x in xcoodinates:
                if state(i):
                    y = yplane
                    for _ in range(self.planeHeight):
                        self.__temp, x, y = self.__RandomWalk(self.__temp, x+self.planeSize//3+self.dist, y)
                        self.__temp, x, y = self.__RandomWalk(self.__temp, x, y)
                        self.__temp, x, y = self.__RandomWalk(self.__temp, x-self.planeSize//3-self.dist, y)
                        
                        self.farm, x, y = self.__RandomWalk(self.farm, x+self.planeSize//3+self.dist, y)
                        self.farm, x, y = self.__RandomWalk(self.farm, x, y)
                        self.farm, x, y = self.__RandomWalk(self.farm, x-self.planeSize//3-self.dist, y)
                    
            self.farmGrids.append(self.farm)
            
            self.frameStore.append(f)
    
    def fertilizerPercentage(self):
        l = []
        for item in self.farmGrids:
            l.append(self.inspectFarmCondition(item))
        return l
    
    def inspectFarmCondition(self, arr):
        mat = arr < self.HARVEST
        mat = mat * 1
        return np.count_nonzero(mat) / (self.size**2)
    
    def Animation(self, name=None):
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        ax[0].set_title("Simulation")
        ax[1].set_title("Percentage of Fertilizer on the Farm")
        
        ax[0].axis('off')
        ax[1].set_xlabel("Time")
        ax[1].set_ylabel("Coverage")
        ax[1].set_ylim(0, 1)
        ax[1].set_xlim(0, len(self.fertilizerPercentage()))
        
        t = np.arange(len(self.fertilizerPercentage()))
        line = ax[1].plot([], [])
        
        im = ax[0].imshow(self.initial_frame, vmin=0, vmax=self.HARVEST+1)
        line, = ax[1].plot([], [])
        
        def update(idx):
            im.set_array(self.frameStore[idx])
            line.set_data(t[:idx], self.fertilizerPercentage()[:idx])
            return [im], line
        
        ani = FuncAnimation(fig, update, frames=len(self.frameStore), interval=50)
        
        if self.savingMode:
            ani.save(f"{self.simulation_result_dir}/{name}")
            
        plt.show()