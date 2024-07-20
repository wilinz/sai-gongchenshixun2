from mcpi.minecraft import Minecraft
import PCF8591 as ADC
import time


# create Minecraft Object
mc = Minecraft.create()
ADC.setup(0x48)					# 设置 PCF8591 芯片的IIC地址
global state

while True:
    x,y,z = mc.player.getPos()
    #pos1 = mc.player.

    if ADC.read(1) >=250:  # 前进
        mc.player.setPos(x+0.1, y, z+0.1)
        print("Moving up ...")
    if ADC.read(1) <= 5: # 后退
        mc.player.setPos(x-0.1, y, z-0.1)
        print("Moving down ...")
    if ADC.read(0) <=5: # 左转
        mc.player.setPos(x+0.1, y, z)
        print("Moving left ...")
    if ADC.read(0) >= 250:# 右转
        mc.player.setPos(x, y, z+0.1)
        print("Moving right ...")