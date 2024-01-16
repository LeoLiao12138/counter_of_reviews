import tkinter as tk  
import matplotlib.pyplot as plt 
from tkinter import messagebox  
from pymodbus.client import ModbusTcpClient 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams["font.family"]="SimSun"


data_list1 = []  
data_list2 = [] 
data_list3 = []
data_list4 = []

def VIM_update_plot(): 
    global fig
    global id1
    # 定义寄存器地址和采样次数  
    register_address = PDI_modbus_address  # 寄存器地址  
    # 存储最近10次的数据  
    global data_list1
    global data_list2 
    global data_list3
    global data_list4
    # 循环采集数据并更新曲线 
    print(stop_click) 
    if stop_click == False:
        result = client.read_holding_registers(address=register_address, count=10,slave=1)  # 读取一个寄存器的数据  
        print(result.registers[2])
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
        id1=root.after(100, VIM_update_plot)# 每100毫秒更新一次曲线数据

       
        
    else:
        client.close()
        root.after_cancel(id1)
        canvas.get_tk_widget().pack_forget()
        fig.canvas.draw()

def RFID_plot(): 
    global root
    global lable_read_data
    global lable_write_data
    global lable_length_read_data
    global lable_length_write_data
    frame_RIFD = tk.Frame(root)
    RFID_read_bottom = tk.Button(frame_RIFD, text = "Read", command = RFID_read)
    RFID_stop_bottom = tk.Button(frame_RIFD, text = "Stop", command = RFID_stop)
    RFID_write_bottom = tk.Button(frame_RIFD, text = "Write", command = RFID_write)
    frame_RIFD.pack(fill=tk.X)
    RFID_read_bottom.pack(side= tk.LEFT)
    RFID_stop_bottom.pack(side= tk.LEFT)
    RFID_write_bottom.pack(side= tk.LEFT)

    frame_RIFD_1 = tk.Frame(root)
    lable_read = tk.Label(frame_RIFD_1, text = "Read data")
    lable_read_data = tk.Text(frame_RIFD_1, height=5, width=45)
    frame_RIFD_1.pack(fill=tk.X)
    lable_read.pack(fill=tk.X)
    lable_read_data.pack(side= tk.TOP)

    frame_RIFD_2 = tk.Frame(root)
    lable_write = tk.Label(frame_RIFD_2, text = "Write data")
    lable_write_data = tk.Text(frame_RIFD_2, height=5, width=45)
    frame_RIFD_2.pack(fill=tk.X)
    lable_write.pack(fill=tk.X)
    lable_write_data.pack(side= tk.TOP)

    frame_RIFD_3 = tk.Frame(root)
    lable_length_read = tk.Label(frame_RIFD_3, text = "Number of bytes to read")
    lable_length_read_data = tk.Text(frame_RIFD_3, height=1, width=3)
    read_length_read_button = tk.Button(frame_RIFD_3, text = "Read", command = Read_RFID_read_length)
    write_length_read_button = tk.Button(frame_RIFD_3, text = "Write", command = Write_RFID_read_length)
    frame_RIFD_3.pack(fill=tk.X)
    lable_length_read.pack(fill=tk.X)
    read_length_read_button.pack(side= tk.LEFT)
    write_length_read_button.pack(side= tk.LEFT)
    lable_length_read_data.pack(side= tk.LEFT)

    frame_RIFD_4 = tk.Frame(root)
    lable_length_write = tk.Label(frame_RIFD_4, text = "Number of bytes to write")
    lable_length_write_data = tk.Text(frame_RIFD_4, height=1, width=3)
    read_length_write_button = tk.Button(frame_RIFD_4, text = "Read", command = Read_RFID_write_length)
    write_length_write_button = tk.Button(frame_RIFD_4, text = "Write", command = Write_RFID_write_length)
    frame_RIFD_4.pack(fill=tk.X)
    lable_length_write.pack(fill=tk.X)
    read_length_write_button.pack(side= tk.LEFT)
    write_length_write_button.pack(side= tk.LEFT)
    lable_length_write_data.pack(side= tk.LEFT)

def Read_RFID_read_length():
    global lable_length_read_data
    global client
    lable_length_read_data.delete(1.0, tk.END)# 清空文本框内容
    register_address = PDI_modbus_address
    ISDU_command_length_read = [0x0001,0x00cc,0x0002,0x0001]

    result_ISDU_commmand_length_read = client.write_registers(address=register_address+0x12c, values=ISDU_command_length_read[:], slave=1)
    result_ISDU_response_length_read = client.read_holding_registers(address=register_address+0x64, count=5,slave=1)

    print(result_ISDU_commmand_length_read)
    print(result_ISDU_response_length_read)
    ISDU1,ISDU2 = word_to_hex(result_ISDU_response_length_read.registers[4])
    lable_length_read_data.insert(tk.END, str(int(ISDU1,16))+"\n")

def Write_RFID_read_length():
    global lable_length_read_data
    global client
    register_address = PDI_modbus_address
    ISDU_command_length_read = [0x0002,0x00cc,0x0002,0x0001]
    if lable_length_read_data.get(1.0, tk.END) == "\n":
        messagebox.showinfo("提示", "请先输入要写入的数据")
        return
    else:
        length_to_write = int(lable_length_read_data.get(1.0, 1.2))*256
        ISDU_command_length_read.append(length_to_write)

        result_ISDU_commmand_length_read = client.write_registers(address=register_address+0x12c, values=ISDU_command_length_read[:], slave=1)

        print(result_ISDU_commmand_length_read)

def Read_RFID_write_length():
    global lable_length_write_data
    global client
    lable_length_write_data.delete(1.0, tk.END)# 清空文本框内容
    register_address = PDI_modbus_address
    ISDU_command_length_read = [0x0001,0x00cd,0x0002,0x0001]

    result_ISDU_commmand_length_read = client.write_registers(address=register_address+0x12c, values=ISDU_command_length_read[:], slave=1)
    result_ISDU_response_length_read = client.read_holding_registers(address=register_address+0x64, count=5,slave=1)

    print(result_ISDU_commmand_length_read)
    print(result_ISDU_response_length_read)
    ISDU1,ISDU2 = word_to_hex(result_ISDU_response_length_read.registers[4])
    lable_length_write_data.insert(tk.END, str(int(ISDU1,16))+"\n")

def Write_RFID_write_length():
    global lable_length_write_data
    global client
    register_address = PDI_modbus_address
    ISDU_command_length_read = [0x0002,0x00cd,0x0002,0x0001]
    if lable_length_write_data.get(1.0, tk.END) == "\n":
        messagebox.showinfo("提示", "请先输入要写入的数据")
        return
    else:
        length_to_write = int(lable_length_write_data.get(1.0, 1.2))*256
        ISDU_command_length_read.append(length_to_write)

        result_ISDU_commmand_length_read = client.write_registers(address=register_address+0x12c, values=ISDU_command_length_read[:], slave=1)

        print(result_ISDU_commmand_length_read)

def word_to_hex(word):  
    # 将整数转换为16进制字符串  
    hex_string = format(word, '04x')  
    # 将字符串分割为两个部分  
    hex_part1 = hex_string[0:2]  
    hex_part2 = hex_string[2:]  
    return hex_part1, hex_part2

def RFID_stop():
    global client
    global lable_read_data
    lable_read_data.delete(1.0, tk.END)# 清空文本框内容  
    register_address = PDI_modbus_address
    stop_command = [0x0000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    result = client.write_registers(address=PDO_modbus_address, values=stop_command[:], slave=1)
    lable_read_data.insert(tk.END, "Stopped"+"\n")

def RFID_write():
    global lable_read_data
    global lable_write_data
    global client
    lable_read_data.delete(1.0, tk.END)# 清空文本框内容
    register_address = PDI_modbus_address
    write_command = [0x0200,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000]
    word=[]
    data_write = lable_write_data.get(1.0, tk.END)
    if data_write == "\n":
        messagebox.showinfo("提示", "请先输入要写入的数据")
        return
    else:
        for i in range(0, len(data_write)-2, 4):  
            hex_part1 = data_write[i:i+2]  
            hex_part2 = data_write[i+2:i+4]
            word.append(int(hex_part1, 16) * 256 + int(hex_part2, 16))
        write_command[2:2+len(word)] = word  
        result_write = client.write_registers(address=PDO_modbus_address, values=write_command[:], slave=1)  # 
        if result_write.isError():  
            print(result_write)  
            client.close()
            #break
        else:
            lable_read_data.insert(tk.END, "Write start"+"\n")

def RFID_read():
    global root
    #global var
    register_address = PDI_modbus_address
    hex_list = []
    global lable_read_data
    lable_read_data.delete(1.0, tk.END)# 清空文本框内容  
    def display_array(array):  
        for item in array:  
            lable_read_data.insert(tk.END, str(item) + " ")  # 插入数组元素并换行 
    read_command = [0x0100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    result1 = client.write_registers(address=PDO_modbus_address, values=read_command[:], slave=1)
    print(result1)

    if stop_click == False:
        result = client.read_holding_registers(address=register_address, count=18,slave=1)  # 读取一个寄存器的数据  
        #print(result.registers[2])
        for item in result.registers:
            hex_part1, hex_part2 = word_to_hex(item)
            hex_list.append(hex_part1) 
            hex_list.append(hex_part2)
        if result.isError():  
            print("读取错误")  
            client.close()
            #break  
        if hex_list[4]=='05':   
            lable_read_data.insert(tk.END, "Read success"+"\n")
            length = int(hex_list[5],16)
            lable_read_data.insert(tk.END, "The length of data is:" + str(length)+"\n")
            lable_read_data.insert(tk.END, "The data is:"+"\n")
            display_array(hex_list[8:length+8])
        else:
            lable_read_data.insert(tk.END, "Read failed"+"\n")

def on_connect():  
    global stop_click
    global port
    global master_type
    global PDI_modbus_address
    global PDO_modbus_address

    ICE23_PDI_modbus_address = [0x3e8,0x7d0,0xbb8,0xfa0,0x1388,0x1770,0x1b58,0x1f40]
    ICE23_PDO_modbus_address = [0x41A,0x802,0xbea,0xfd2,0x13ba,0x17a2,0x1b8a,0x1f72]
    ICE11_PDI_modbus_address = [0x101,0x111,0x121,0x131,0x141,0x151,0x161,0x171]
    ICE11_PDO_modbus_address = [0x1,0x11,0x21,0x31,0x41,0x51,0x61,0x71]

    if master_type.get() == 1:
        PDI_address_value = ICE11_PDI_modbus_address
        PDO_address_value = ICE11_PDO_modbus_address

    else:
        PDI_address_value = ICE23_PDI_modbus_address   
        PDO_address_value = ICE23_PDO_modbus_address

    PDI_modbus_address = PDI_address_value[port.get()-1]
    PDO_modbus_address = PDO_address_value[port.get()-1]

    stop_click = False
    print(stop_click)
    try:  
        global client
        global Device_type
        global fig
        global canvas
        fig= plt.figure()
        client = ModbusTcpClient(entry.get(), port=502)  
        client.close() 
        client.connect()  

        
        
        if Device_type.get() == 0:
            VIM_update_plot()
            canvas = FigureCanvasTkAgg(fig)  
            canvas.draw()  
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        elif Device_type.get() == 1:
            RFID_plot()

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
    print(stop_click)


if __name__ == '__main__':  
    root = tk.Tk()  
    root.title("ICE2/3 ModBus/TCP 数据采集")  

    frame1 = tk.Frame(root)  
    frame1.pack(fill=tk.X)  # 框架填充X方向 
    lable1 = tk.Label(frame1, text="IP:")
    entry = tk.Entry(frame1)
    lable1.pack(side= tk.LEFT)
    entry.pack(side= tk.LEFT)


    




    frame21 = tk.Frame(root)  
    frame21.pack(fill=tk.X)
    lable_master_type = tk.Label(frame21, text="Master type: ")
    lable_master_type.pack(side= tk.LEFT)
    master_type = tk.IntVar()
    Master_type_ICE11= tk.Radiobutton(frame21, text="ICE11", variable=master_type, value=1)
    Master_type_ICE23= tk.Radiobutton(frame21, text="ICE2/3", variable=master_type, value=2)
    Master_type_ICE11.select()
    Master_type_ICE11.pack(side= tk.LEFT)
    Master_type_ICE23.pack(side= tk.LEFT)
    


    frame22 = tk.Frame(root)  
    frame22.pack(fill=tk.X)
    lable2 = tk.Label(frame22, text="Port:")
    lable2.pack(side= tk.LEFT)
    # 创建单选按钮组  
    port = tk.IntVar() 
    radio1 = tk.Radiobutton(frame22, text="1", variable=port, value=1)  
    radio2 = tk.Radiobutton(frame22, text="2", variable=port, value=2)  
    radio3 = tk.Radiobutton(frame22, text="3", variable=port, value=3)  
    radio4 = tk.Radiobutton(frame22, text="4", variable=port, value=4)  
    radio5 = tk.Radiobutton(frame22, text="5", variable=port, value=5)  
    radio6 = tk.Radiobutton(frame22, text="6", variable=port, value=6)  
    radio7 = tk.Radiobutton(frame22, text="7", variable=port, value=7)  
    radio8 = tk.Radiobutton(frame22, text="8", variable=port, value=8)  
    radio1.select()

    # 添加组件到窗口中  
    
    radio1.pack(side= tk.LEFT)  
    radio2.pack(side= tk.LEFT)  
    radio3.pack(side= tk.LEFT)  
    radio4.pack(side= tk.LEFT)  
    radio5.pack(side= tk.LEFT)  
    radio6.pack(side= tk.LEFT)  
    radio7.pack(side= tk.LEFT)  
    radio8.pack(side= tk.LEFT)  


    frame3 = tk.Frame(root)
    frame3.pack(fill=tk.X)
    lable3 = tk.Label(frame3, text="Device Type:")
    Device_type = tk.IntVar() 
    radio_Device_type1 = tk.Radiobutton(frame3, text="VIM3", variable=Device_type, value=0)  
    radio_Device_type2 = tk.Radiobutton(frame3, text="RFID", variable=Device_type, value=1)
    radio_Device_type1.select()
    lable3.pack(side= tk.LEFT)
    radio_Device_type1.pack(side= tk.LEFT)
    radio_Device_type2.pack(side= tk.LEFT)

    frame4 = tk.Frame(root)  
    frame4.pack(fill=tk.X)  # 框架填充X方向 
    
    connect_button = tk.Button(frame4, text="连接", command=on_connect)  
    stop_button = tk.Button(frame4, text="断开", command=_stop)  
    connect_button.pack(side= tk.LEFT) 
    stop_button.pack(side= tk.LEFT)


    root.protocol("WM_DELETE_WINDOW", _quit)

    root.mainloop()
