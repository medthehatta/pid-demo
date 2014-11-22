setpoint = 0
initial  = -5

K_p = 0
K_i = 0
K_d = 0

running_time = 16
damping      = 0.6
dt           = 1e-4
crappiness   = 0







####################
# simulation stuff #
####################

# imports
import numpy as np
import matplotlib.pyplot as plt

# system equation
def update(p, damping=1, drift=0, f=0, dt=1e-2):
    (x0, v0) = p
    x1 = v0*dt + x0
    v1 = (f - damping*v0)*dt + v0 + drift
    return (x1, v1)

# initialize the simulation
X     = np.arange(0,running_time,dt)
(x,v) = (initial,0)
vals  = []
integ = 0  # for use with the integral term
last  = 0  # for use with the derivative term

# run the simulation
for pt in X:
    err = (setpoint - x)

    prop  =  K_p*err
    integ += K_i*dt*err
    deriv =  K_d/dt*(err - last)

    f = prop + integ + deriv + crappiness

    (x,v) = update(
        (x,v), 
        damping=damping, 
        f=f, 
        dt=dt,
    )

    vals.append(x)
    last = err

# plot to file
fig_filename = '/tmp/plot.png'

fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111)
ax.plot(X, [setpoint]*len(vals), 'r-', linewidth=2)
ax.plot(X, vals, 'k-')

plt.title('Response of a PID-controlled System')
plt.ylabel('Position')
plt.xlabel('Time')
plt.ylim(min(vals),max(*[1.1*setpoint]+vals))
plt.grid(True)

fig.savefig(fig_filename)

# Update open graph on Med's computer.
# (Probably won't work anywhere else)
import os
os.system('xdotool search --name feh key r')
os.system('xdotool search --name feh key r')

