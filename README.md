# Python-Checkers-AI
A fork from "Python-Checkers-AI" as a project for GAME THEORY course.

## readme

- （assets 文件夹中是王冠的图片，exps-backup 文件夹中是一些备份数据）
- checkers 文件夹内的文件分别是不同类的实现。
- minimax 文件夹中的 algorithm.py 文件具体实现了minimax算法和alpha-beta优化算法。
- visual 文件夹中的 visualization.py、curvefit.py 分别是对实验数据可视化、拟合曲线的程序。
- graphs 文件夹中是最终可视化的结果图。
- main.py 实现一局游戏的进行，tools.py 对一局游戏的过程进行分析得到需要的信息。
- experiments.py 生成三个实验的实验数据。三个函数分别为：t1,t2,t3。
- .log 文件是实验数据生出过程中的log。
- .txt 文件是最终生成的数据。

## pipeline with comment

| command | comment |
|  ----   | ----    |
| python experiments.py [> expX.log]  | # 手动注释/取消注释，进行指定实验1/2/3 [生成log文件可选] |
| python visualization.py             | # 手动注释/取消注释，可视化实验1/2/3的结果              |
| python curvefit.py                  | # 拟合实验1中的曲线，并可视化                          |
