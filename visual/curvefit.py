import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
from visualization import strList2list
pi = np.pi

# 模拟生成一组实验数据
f = open("exp1.time_depths.txt", "r")
x = np.array(strList2list(f.readline(), 1, -2))
y_mm = np.array(strList2list(f.readline(), 1, -2))
y = np.array(strList2list(f.readline(), 1, -2))
noise = np.random.uniform(0, 0.1, len(x))
y += noise
fig, ax = plt.subplots()
ax.plot(x, y, 'b--', label="Alpha-Beta")


# 拟合指数曲线
def target_func(x, a0, a1, a2):
    return a0 * pow(a1,x) + a2


p0 = [1, 1.1, 0]
print(p0)
para, cov = optimize.curve_fit(target_func, x, y, p0=p0)
print(para)

x_fit = [i for i in np.linspace(1, 8, 1000)]
y_fit = [target_func(a, *para) for a in x_fit]
xxxx = str("f(x)="+"{:.3}".format(para[0]))+"*"+str("{:.3}".format(para[1]))+"^x"+str("{:+.3}".format(para[2]))
ax.plot(x_fit, y_fit, 'g', label=xxxx)
plt.title("Fitting Alpha-Beta Algorithm", fontsize="15")
plt.xlabel('Depths', fontsize="15")
plt.ylabel('Average Time/Step', fontsize="15")
plt.xticks(fontsize="14")
plt.yticks(fontsize="14")
plt.legend(fontsize="15")
plt.show()
