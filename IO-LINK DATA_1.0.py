import time  
import matplotlib.pyplot as plt  
from pymodbus.client import ModbusTcpClient  

plt.rcParams["font.family"]="SimSun"
def get_bit_val(byte, index):
    """
    得到某个字节中某一位（Bit）的值

    :param byte: 待取值的字节值
    :param index: 待读取位的序号，从右向左0开始，0-7为一个完整字节的8个位
    :returns: 返回读取该位的值，0或1
    """
    if byte & (1 << index):
        return 1
    else:
        return 0

# 连接Modbus TCP设备  
client = ModbusTcpClient("192.168.0.250", port=502)  
client.connect()  
  
# 定义寄存器地址和采样次数  
register_address = 0x3e8  # 寄存器地址  
sampling_interval = 0.01  # 采样间隔（秒）
# 存储最近10次的数据  
data_list1 = []  
data_list2 = [] 
data_list3 = []
data_list4 = []
# 循环采集数据并更新曲线  
while True:  
    result = client.read_holding_registers(address=register_address, count=10,slave=1)  # 读取一个寄存器的数据  
    print(result.registers[2])
    if result.isError():  
        print("读取错误")  
        client.close()
        break  
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
   # plt.draw()  # 更新图形显示  

    plt.pause(sampling_interval)  # 暂停一段时间，以便用户能够看到更新的曲线  
    #time.sleep(sampling_interval)  # 等待采样间隔时间
    if len(plt.get_fignums())==0:
        break
    else:
        plt.draw()