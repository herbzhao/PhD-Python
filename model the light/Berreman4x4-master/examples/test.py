import matplotlib.pyplot as plt

x = [0,1,2,3,4]
y = [1,2,34,5,7]
fig, axes = plt.subplots(6, 1, subplot_kw=dict(polar=True))
axes[0].plot(x, y)
axes[1].scatter(x, y)

plt.show()