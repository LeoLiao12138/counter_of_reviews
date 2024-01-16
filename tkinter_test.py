import tkinter as tk  
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
  
# 创建Tkinter窗口  
root = tk.Tk()  
root.title("Tkinter with Matplotlib Subplots")  
  
# 创建多个子图  
fig, axs = plt.subplots(2, 2)  # 创建一个2x2的子图网格  
  
# 在每个子图上绘制数据  
axs[0, 0].plot([1, 2, 3], [1, 2, 3])  
axs[0, 0].set_title("子图1")  
  
axs[0, 1].plot([1, 2, 3], [3, 2, 1])  
axs[0, 1].set_title("子图2")  
  
axs[1, 0].plot([1, 2, 3], [5, 4, 3])  
axs[1, 0].set_title("子图3")  
  
axs[1, 1].plot([1, 2, 3], [7, 6, 5])  
axs[1, 1].set_title("子图4")  
  
# 将图形嵌入到Tkinter窗口中  
canvas = FigureCanvasTkAgg(fig)  
canvas.draw()  
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  
  
# 运行Tkinter事件循环  
root.mainloop()