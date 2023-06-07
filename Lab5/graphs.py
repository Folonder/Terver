import matplotlib
import matplotlib.pyplot as plt

# Set the backend to Qt5Agg
matplotlib.use('Qt5Agg')

# Plotting the first graph
plt.subplot(3, 1, 1)
plt.plot([1, 2, 3], [4, 5, 6])
plt.title('Graph 1')

# Plotting the second graph
plt.subplot(3, 1, 2)
plt.plot([3, 2, 1], [6, 5, 4])
plt.title('Graph 2')

# Plotting the third graph
plt.subplot(3, 1, 3)
plt.plot([1, 3, 5], [2, 4, 6])
plt.title('Graph 3')

# Adjusting spacing between subplots
plt.subplots_adjust(hspace=0.5)

# Displaying the plots
plt.show()