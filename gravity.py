import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import jit


G = 6.67408e-11 * 100_000_000 
N_BODIES = 20


class Body:
    def __init__(self, mass, pos, vel, acc=0, colour="r."):
        self.mass = mass
        self.pos = np.array(pos)  # vector
        self.vel = np.array(vel)  # vector
        self.acc = np.array(acc)  # vector
        self.colour = colour

    def __str__(self):
        return f"Body: Mass {self.mass}, Position {self.pos}, Velocity {self.vel}, Acceleration {self.acc}"

    def update_position(self, t):
        self.pos = self.pos + self.vel*t + 0.5*self.acc*t**2

    def update_vel(self, t):
        self.vel = self.vel + (t * self.acc)

class Simulation:
    def __init__(self, bodies):
        self.bodies = bodies  # list of Body objects

    def step(self, timestep=.1):
        coords = None
        for body_one in self.bodies:
                forces = np.zeros_like(body_one.pos)
                for body_two in self.bodies:
                    if body_one is body_two:
                        continue
                    forces = np.add(forces, F_g(body_one, body_two))
                body_one.acc =  forces / body_one.mass
                body_one.update_position(timestep)
                body_one.update_vel(timestep)
                coords = np.vstack((coords, body_one.pos)) if coords is not None else body_one.pos
        return coords

def F_g(one, two):
    return ((G * one.mass * two.mass) / (r(one.pos, two.pos) ** 2)) * r_unit(one.pos, two.pos)

def r(r1, r2):
    return np.linalg.norm(r1 - r2)

def r_unit(r1, r2):
    return (r2 - r1) / np.linalg.norm(r2-r1)

def main():
    dimensions = 3
    bodies = [Body(1000000, [0,0,0], [0,0,0])]  # initialize with a "sun"
    
    # modifiers to change the range of randomly generated planets
    mass_mod = 100
    p_mod = 100
    v_mod = 25
    masses = [100]  # sun
    for _ in range(N_BODIES):
        #  mass, pos, vel
        m = np.random.random() * mass_mod
        masses.append(m)
        p = (np.random.random(dimensions) * p_mod) - p_mod/2
        v = (np.random.random(dimensions) * v_mod) - v_mod/2
        b = Body(m, p, v)
        bodies.append(b)

    s = Simulation(bodies)

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xticks([]), ax.set_yticks([]), ax.set_zticks([])
    ax.set_xlim3d(-100, 100); ax.set_ylim3d(-100, 100); ax.set_zlim3d(-100, 100)
    i = s.step()
    graph = ax.scatter(i[..., 0], i[..., 1], i[..., 2], '.', s=masses)

    def update(frame_number):
        i = s.step()
        graph._offsets3d = (i[..., 0], i[..., 1], i[..., 2])
        return graph,

    animation = FuncAnimation(fig, update, interval=1, blit=False)
    plt.show()

if __name__ == "__main__":
    main()