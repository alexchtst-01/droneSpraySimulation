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
        # arah horizontal
        if random.random() < 0.5:
            if random.random() < 0.5:
                # kekanan
                xpos = min(self.size-1, xpos+1)
            else:
                # kekiri
                xpos = min(self.size-1, xpos-1)
        
        # arah vertikal
        else:
            if random.random() < 0.5:
                # kebawah
                ypos = min(self.size-1, ypos+1)
            else:
                # keatas
                ypos = min(self.size-1, ypos-1)
        
        grid[xpos, ypos] -= 5
        
        return grid
    
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
    
    def runSimulation(self, num_plane, state, vel=3, steps=600):
        for i in tqdm(range(steps)):
            yplane = max((self.size - self.planeSize) - i*vel, self.planeSize)
            xcoodinates = []
            for n in range(num_plane):
                xcoodinates.append(int(self.size * (n+1) / (num_plane + 1)))
            
            f = self.__movePlane(self.__temp, xcoodinates[0], yplane)
            for j in range(1, num_plane):
                f = self.__movePlane(f, xcoodinates[j], yplane)
            
            if state(i):
                for j in range(num_plane):
                    x = xcoodinates[j]
                    y = yplane
                    self.__temp= self.__RandomWalk(self.__temp, y, x + self.planeSize//2)
                    self.__temp= self.__RandomWalk(self.__temp, y, x - self.planeSize//2)
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

modsim = sprayDroneSimulation(farm_size=128, simulation_result_dir="res", planeSize=12)
modsim.runSimulation(num_plane=2, vel=1, state=lambda i : i % 20 > 10)
modsim.Animation(name="testlagi.gif")