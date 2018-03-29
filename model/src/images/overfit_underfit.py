import matplotlib.pyplot as plt
import numpy as np


def fit(deg):
    z = np.polyfit(sample_x, sample_y, deg)
    p = np.poly1d(z)
    return p(real_x)


def print_subplot(i, fitted, title):
    axes[0, i].axis('off')
    a = axes[1, i]
    a.set_ylim(-0.5, 1.5)
    a.plot(real_x, real_y)
    a.scatter(sample_x, sample_y)
    a.plot(real_x, fitted)
    a.set_title(title)
    a.get_xaxis().set_visible(False)
    a.get_yaxis().set_visible(False)


np.random.seed(1354)

start = 0
end = np.pi
original_size = 50
sample_size = 10
random_amount = 0.1

real_x = np.linspace(start, end, original_size)
real_y = np.sin(real_x)

sample_x = np.random.uniform(start, end, sample_size)
sample_x.sort()
sample_y = np.sin(sample_x) + random_amount * np.random.standard_normal(sample_size)

underfit = fit(1)
just_fine = fit(2)
overfit = fit(7)

fig, axes = plt.subplots(
    2,
    3,
    gridspec_kw={'width_ratios': [1, 1, 1], 'height_ratios': [0.01, 1]},
    figsize=(16, 5))
print_subplot(0, underfit, "Alulilleszkedés")
print_subplot(1, just_fine, "Megfelelő illeszkedés")
print_subplot(2, overfit, "Túlilleszkedés")

fig.tight_layout()
plt.show()
