import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from tqdm import tqdm

class sprayDroneSimulation:
    def __init__(self, farm_size, simulation_result_dir=None, savingMode=False, planeSize=25):
        self.simulation_result_dir = simulation_result_dir
        self.savingMode = savingMode
        
        self.LOWEST = 0
        self.PLANE = 1
        self.HARVEST = 9
        self.HIGHEST = 10
        
        self.frameStore = []
        self.size = farm_size
        self.planeSize = planeSize
        
        self.inital_random_points = []
        self.initial_frame = np.ones(shape=(self.size, self.size)) * self.HARVEST
        self.__temp = np.ones(shape=(self.size, self.size)) * self.HARVEST
        
        if self.planeSize < 12:
            print("minimun size of the plane in 12")
        
    
    def __RandomWalk(self, arr, xpos, ypos):
        grid = arr.copy()        
        if random.random() < 0.5:
            if random.random() < 0.5:
                xpos = max(0, min(self.size-1, xpos+2))
            else:
                xpos = max(0, min(self.size-1, xpos-2))        
        else:
            if random.random() < 0.5:
                ypos = max(0, min(self.size-1, ypos+2))
            else:
                ypos = max(0, min(self.size-1, ypos-2))
        
        grid[ypos-1:ypos+1, xpos-1:xpos+1] -= 0.5
        
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
        for i in tqdm(range(steps - self.planeSize)):
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
                    for _ in range(20):
                        self.__temp, x, y = self.__RandomWalk(self.__temp, x, y)
            self.frameStore.append(f)
    
    def Animation(self, name=None):
        fig, ax = plt.subplots()
        ax.axis('off')
        
        def update(frame_idx):
            im.set_array(self.frameStore[frame_idx])
            return [im]
        
        initial_frame = self.frameStore[0]
        im = ax.imshow(self.initial_frame, vmin=0, vmax=self.HARVEST+1)
        ani = FuncAnimation(fig, update, frames=len(self.frameStore), interval=50)
        
        if self.savingMode:
            ani.save(f"{self.simulation_result_dir}/{name}")
            
        plt.axis('off')
        plt.show()

modsim = sprayDroneSimulation(farm_size=200, simulation_result_dir="res", planeSize=12)
modsim.runSimulation(num_plane=8, vel=1, state=lambda i : i % 20 > 0)
modsim.Animation(name="testlagi.gif")
# print(len(modsim.inital_random_points))