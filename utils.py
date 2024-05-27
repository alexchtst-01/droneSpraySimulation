import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def addPlane(arr, xpos, ypos, size=25):
    s = size // 2
    temp = arr.copy()
    # badan pesawat
    temp[ypos-s:ypos+s-2, xpos-int(s*0.2):xpos+int(s*0.2)] = 1
    # sayap pesawat
    temp[ypos-3:ypos-1, xpos-s:xpos+s] = 1
    temp[ypos-2:ypos, xpos-s-1:xpos+s+1] = 1
    temp[ypos-1:ypos+1, xpos-s-1:xpos+s+1] = 1
    # ekor pesawat
    temp[ypos+s-2:ypos+s-1, xpos-s//3:xpos+s//3] = 1
    temp[ypos+s-1:ypos+s, xpos-s//2:xpos+s//2] = 1
    
    return temp

def simulateFrames(frameStore, vmin, vmax):
    fig, ax = plt.subplots()
    
    def update(frame_number):
        im.set_array(frameStore[frame_number])
        return [im]

    initial_frame = frameStore[0]

    im = ax.imshow(initial_frame, vmin=vmin, vmax=vmax)

    ani = animation.FuncAnimation(fig, update, frames=len(frameStore), interval=25, blit=True)

    plt.axis('off')
    plt.show()