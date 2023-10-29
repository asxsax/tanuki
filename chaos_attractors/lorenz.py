# †
"""
Lorenz attractor animated using matplotlib,
simple solve using scipy ODE solver. Nothing
insane.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

# Initial values
axis = [1,1,1]
dt = np.linspace(0, 40, 10000)
sigma, rho, beta = 10, 28, 8/3

# System
def lorenz(axis, dt):
    x, y, z = axis
    dx = sigma * (y-x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return[dx, dy, dz]

# Solve differential equations
diff_eq = odeint(lorenz, axis , dt)

# Figure 
fig = plt.figure(facecolor='black')
ax = fig.add_subplot(projection='3d', facecolor='black')
sc = ax.scatter([], [], [], 'o', c='white', s=0.05)

# Axis limits
ax.set_xlim([min(diff_eq[:, 0]), max(diff_eq[:, 0])])
ax.set_ylim([min(diff_eq[:, 1]), max(diff_eq[:, 1])])
ax.set_zlim([min(diff_eq[:, 2]), max(diff_eq[:, 2])])

# Title and grid
ax.set_title('Chaos attractor', color='white')
ax.grid(False)

# Dark pane
ax.xaxis.set_pane_color((0, 0, 0, 1))
ax.yaxis.set_pane_color((0, 0, 0, 1))
ax.zaxis.set_pane_color((0, 0, 0, 1))

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Animate
def update(frame):
    sc._offsets3d = (diff_eq[:frame*10, 0], diff_eq[:frame*10, 1],
                     diff_eq[:frame*10, 2])
    return sc,

ani = FuncAnimation(fig, update, interval=1, frames=range(1,
                    len(diff_eq)), blit=False, repeat=False)

# Show figure
plt.show()
