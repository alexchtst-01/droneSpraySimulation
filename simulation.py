from model import sprayAircraft
import matplotlib.pyplot as plt
import numpy as np
#Simulate all cases

#Case 1 for planeHeight = 30 and num_plane = 8
first_sim_values = []
first_sim = sprayAircraft(farm_size=200, simulation_result_dir="res", planeSize=12, planeHeight=30)
first_sim.runSimulation(num_plane=8, vel=1, state=lambda i : i % 20 > 0)
first_sim.Animation(name="planeHeight = 30 and num_plane = 8")
first_sim_coverage = first_sim.fertilizerPercentage()
first_sim_values.append([1, first_sim_coverage[-1]])
print(f"Coverage : {first_sim_coverage[-1]*100}%")

for i in range(9): #Iterate for 9 times, because we already have 1 data
    first_sim = sprayAircraft(farm_size=200, simulation_result_dir="res", planeSize=12, planeHeight=30)
    first_sim.runSimulation(num_plane=8, vel=1, state=lambda i : i % 20 > 0)
    first_sim_values.append([i+2, first_sim.fertilizerPercentage()[-1]])

#Plot the result
first_sim_values = np.array(first_sim_values)
plt.scatter(first_sim_values[:,0], first_sim_values[:,1])

#Case 2 for planeHeight = 15 and num_plane = 8
second_sim_values = []
second_sim = sprayAircraft(farm_size=200, simulation_result_dir="res", planeSize=12, planeHeight=30)
second_sim.runSimulation(num_plane=8, vel=1, state=lambda i : i % 20 > 0)
second_sim.Animation(name="planeHeight = 15 and num_plane = 8")
second_sim_coverage = second_sim.fertilizerPercentage()
second_sim_values.append([1, second_sim_coverage[-1]])
print(f"Coverage : {second_sim_coverage[-1]*100}%")

for i in range(9): #Iterate for 9 times, because we already have 1 data
    second_sim = sprayAircraft(farm_size=200, simulation_result_dir="res", planeSize=12, planeHeight=15)
    second_sim.runSimulation(num_plane=8, vel=1, state=lambda i : i % 20 > 0)
    second_sim_values.append([i+2, second_sim.fertilizerPercentage()[-1]])

#Plot the result
second_sim_values = np.array(second_sim_values)
plt.scatter(second_sim_values[:,0], second_sim_values[:,1])

#Case 3 for planeHeight = 15 and num_plane = 4
third_sim_values = []
third_sim = sprayAircraft(farm_size=200, simulation_result_dir="res", planeSize=12, planeHeight=15)
third_sim.runSimulation(num_plane=4, vel=1, state=lambda i : i % 20 > 0)
third_sim.Animation(name="planeHeight = 15 and num_plane = 4")
third_sim_coverage = third_sim.fertilizerPercentage()
third_sim_values.append([1, third_sim_coverage[-1]])
print(f"Coverage : {third_sim_coverage[-1]*100}%")

for i in range(9): #Iterate for 9 times, because we already have 1 data
    third_sim = sprayAircraft(farm_size=200, simulation_result_dir="res", planeSize=12, planeHeight=15)
    third_sim.runSimulation(num_plane=4, vel=1, state=lambda i : i % 20 > 0)
    third_sim_values.append([i+2, third_sim.fertilizerPercentage()[-1]])

#Plot the result
third_sim_values = np.array(third_sim_values)
plt.scatter(third_sim_values[:,0], third_sim_values[:,1])

#Case 4 for planeHeight = 30 and num_plane = 4
fourth_sim_values = []
fourth_sim = sprayAircraft(farm_size=200, simulation_result_dir="res", planeSize=12, planeHeight=30)
fourth_sim.runSimulation(num_plane=4, vel=1, state=lambda i : i % 20 > 0)
fourth_sim.Animation(name="planeHeight = 30 and num_plane = 4")
fourth_sim_coverage = fourth_sim.fertilizerPercentage()
fourth_sim_values.append([1, fourth_sim_coverage[-1]])
print(f"Coverage : {fourth_sim_coverage[-1]*100}%")

for i in range(9): #Iterate for 9 times, because we already have 1 data
    fourth_sim = sprayAircraft(farm_size=200, simulation_result_dir="res", planeSize=12, planeHeight=30)
    fourth_sim.runSimulation(num_plane=4, vel=1, state=lambda i : i % 20 > 0)
    fourth_sim_values.append([i+2, fourth_sim.fertilizerPercentage()[-1]])
    
#Plot the result
fourth_sim_values = np.array(fourth_sim_values)
plt.scatter(fourth_sim_values[:,0], fourth_sim_values[:,1])