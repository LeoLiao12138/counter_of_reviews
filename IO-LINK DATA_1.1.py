import tkinter as tk  
import matplotlib.pyplot as plt 
from tkinter import messagebox  
from pymodbus.client import ModbusTcpClient 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams["font.family"]="SimSun"

#stop_click = True
def on_connect():  
    global stop_click
    
    stop_click = False
    try:  

        client = ModbusTcpClient(entry.get(), port=502)  
        client.close() 
        client.connect()  
        # 定义寄存器地址和采样次数  
        register_address = var.get()  # 寄存器地址  
        sampling_interval = 0.01  # 采样间隔（秒）
        # 存储最近10次的数据  
        data_list1 = []  
        data_list2 = [] 
        data_list3 = []
        data_list4 = []
        # 循环采集数据并更新曲线  

        fig= plt.figure()
        

        def update_plot(): 
            global id1
            if stop_click == False:
                result = client.read_holding_registers(address=register_address, count=10,slave=1)  # 读取一个寄存器的数据  
                #print(result.registers[2])
                if result.isError():  
                    print("读取错误")  
                    client.close()
                    #break  
                vRMS = result.registers[2]/100  # 获取读取的数据 
                aRMS = result.registers[4]/100  # 获取读取的数据 
                aPeak = result.registers[6]/100 
                Temperature = result.registers[8] 
                data_list1.append(vRMS)  
                data_list2.append(aRMS)
                data_list3.append(aPeak)
                data_list4.append(Temperature)
                if len(data_list1) > 100:  # 只保留最近10次的数据  
                    data_list1.pop(0)  
                if len(data_list2) > 100:  # 只保留最近10次的数据  
                    data_list2.pop(0)  
                if len(data_list3) > 100:  # 只保留最近10次的数据  
                    data_list3.pop(0) 
                if len(data_list4) > 100:  # 只保留最近10次的数据  
                    data_list4.pop(0) 
                
                # 绘制曲线图  
                
                plt.clf()  # 清空当前图形  
                ax1=plt.subplot(2,2,1)
                plt.plot(data_list1,'g')  
                plt.xlabel('Time')  
                plt.ylabel('vRMS(mm/s)')  
                plt.xlim(0,100)
                plt.ylim(0,250)
                plt.title('振动速度vRMS')  
                plt.text(len(data_list1),data_list1[-1],data_list1[-1])

                ax2=plt.subplot(2,2,2)
                plt.plot(data_list2,'r')  
                plt.xlabel('Time')  
                plt.ylabel('aRMS(g)')  
                plt.xlim(0,100)
                plt.ylim(0,15)
                plt.title('振动加速度aRMS')  
                plt.text(len(data_list2),data_list2[-1],data_list2[-1])

                ax3=plt.subplot(2,2,3)
                plt.plot(data_list3,'b')  
                plt.xlabel('Time')  
                plt.ylabel('aPeak(g)')  
                plt.xlim(0,100)
                plt.ylim(0,15)
                plt.title('峰值振动加速度aPeak')  
                plt.text(len(data_list3),data_list3[-1],data_list3[-1])

                ax4=plt.subplot(2,2,4)
                plt.plot(data_list4,'y')  
                plt.xlabel('Time')  
                plt.ylabel('Teamperature(℃)')  
                plt.xlim(0,100)
                plt.ylim(0,40)
                plt.title('温度Teamperature')  
                plt.text(len(data_list4),data_list4[-1],data_list4[-1])

                plt.tight_layout()

                fig.canvas.draw()  # 重新绘制整个图形  
                
                id1=root.after(100, update_plot)# 每100毫秒更新一次曲线数据
            else:
                client.close()
                
                root.after_cancel(id1)
                canvas.get_tk_widget().pack_forget()
                fig.canvas.draw()
        update_plot()

        canvas = FigureCanvasTkAgg(fig)  
        canvas.draw()  
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
    except Exception as e:  
        # 处理pymodbus的异常，例如连接超时  
        if 'timed out' in str(e):  
            messagebox.showerror("错误", "连接超时，请检查网络连接或增加超时时间。")  
        else:  
            messagebox.showerror("错误", "发生其他Modbus通信异常: " + str(e))  
    finally:  
        client.close()  

def _quit():

    root.quit()
    root.destroy()

def _stop():
    global stop_click
    stop_click = True

if __name__ =="__main__":
    root = tk.Tk()  
    root.title("ICE2/3 ModBus/TCP 数据采集")  

    frame1 = tk.Frame(root)  
    frame1.pack(fill=tk.X)  # 框架填充X方向 
    lable1 = tk.Label(frame1, text="IP:")
    entry = tk.Entry(frame1)
    lable1.pack(side= tk.LEFT)
    entry.pack(side= tk.LEFT)




    frame2 = tk.Frame(root)  
    frame2.pack(fill=tk.X)  # 框架填充X方向 
    # 创建整型变量  
    
    lable2 = tk.Label(frame2, text="Port:")
    connect_button = tk.Button(frame2, text="连接", command=on_connect)  
    stop_button = tk.Button(frame2, text="断开", command=_stop)  
    # 创建单选按钮组  
    var = tk.IntVar() 

    radio1 = tk.Radiobutton(frame2, text="1", variable=var, value=0x3e8)  
    radio2 = tk.Radiobutton(frame2, text="2", variable=var, value=0x7d0)  
    radio3 = tk.Radiobutton(frame2, text="3", variable=var, value=0xbb8)  
    radio4 = tk.Radiobutton(frame2, text="4", variable=var, value=0xfa0)  
    radio5 = tk.Radiobutton(frame2, text="5", variable=var, value=0x1388)  
    radio6 = tk.Radiobutton(frame2, text="6", variable=var, value=0x1770)  
    radio7 = tk.Radiobutton(frame2, text="7", variable=var, value=0x1b58)  
    radio8 = tk.Radiobutton(frame2, text="8", variable=var, value=0x1f40)  

    radio1.select()

    # 添加组件到窗口中  
    lable2.pack(side= tk.LEFT)
    radio1.pack(side= tk.LEFT)  
    radio2.pack(side= tk.LEFT)  
    radio3.pack(side= tk.LEFT)  
    radio4.pack(side= tk.LEFT)  
    radio5.pack(side= tk.LEFT)  
    radio6.pack(side= tk.LEFT)  
    radio7.pack(side= tk.LEFT)  
    radio8.pack(side= tk.LEFT)  
    connect_button.pack(side= tk.LEFT) 
    stop_button.pack(side= tk.LEFT)

    root.protocol("WM_DELETE_WINDOW", _quit)

    root.mainloop()
