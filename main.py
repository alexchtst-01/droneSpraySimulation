import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

class sprayDroneSimulation:
    def __init__(self, farm_size, simulation_result_dir=None, savingMode=False):
        self.simulation_result_dir = simulation_result_dir
        self.save = savingMode
        
        self.LOWEST = 0
        self.PLANE = 1
        self.HARVEST = 2
        self.HIGHEST = 10
        
        self.frameStore = []
        self.size = farm_size
        
        self.initial_frame = np.zeros(shape=(self.size, self.size))
        
    
    def createInitialFarm(self, size):
        grid = np.ones(shape=(size+1, size+1)) * self.HARVEST
        return grid
    
    def __RandomWalk(self, initX, initY, steps):
        for _ in range(step):
            # gerakan horizontal
            if random.random() < 0.5:
                # ke kanan
                if random.random() < 0.5:
                    initX = (initX + 1) % self.size
                # kekiri
                else:
                    initX = (initX - 1) % self.size
            
            # gerakan vertikal
            else: 
                # keatas
                if random.random() < 0.5:
                    initY = (initY - 1) % self.size
                # kebawah
                else:
                    initY = (initY + 1) % self.size

            grid[initX, initY] = (grid[initX, initY] + 1) % 20
    
    def __movePlane(self, arr, xpos, ypos, size=25):
        s = size // 2
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
    
    def runSimulation(self, num_plane):
        for i in range(100):
            yplane = (self.size - 30) - 2*i
            xcoodinates = []
            for n in range(num_plane):
                xcoodinates.append(int(self.size * (n+1) / (num_plane + 1)))
            
            f = self.__movePlane(self.initial_frame, xcoodinates[0], yplane)
            for j in range(1, num_plane):
                f = self.__movePlane(f, xcoodinates[j], yplane)
            
            self.frameStore.append(f)
    
    def saveAnimation(self, name):
        fig, ax = plt.subplots()
        ax.axis('off')
        
        def update(frame_idx):
            im.set_array(self.frameStore[frame_idx])
            return [im]
        
        initial_frame = self.frameStore[0]
        im = ax.imshow(self.initial_frame, vmin=0, vmax=self.HARVEST+1)
        ani = FuncAnimation(fig, update, frames=len(self.frameStore), interval=50)
        
        plt.axis('off')
        plt.show()

modsim = sprayDroneSimulation(farm_size=256)
modsim.runSimulation(num_plane=4)
modsim.saveAnimation(name="hai.gif")