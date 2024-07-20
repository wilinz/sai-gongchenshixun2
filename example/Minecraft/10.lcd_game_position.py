#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：10.lcd_game_position.py
#  版本：V2.0
#  author: zhulin
# 说明：LCD 显示Minecraft 角色位置
#------------------------------------------
import time
import Adafruit_CharLCD as LCD
from mcpi.minecraft import Minecraft

# 建立一个Minecraft对象
CreatePi_mc = Minecraft.create()

# 定义16x2液晶显示器的列和行大小。
CreatePi_lcd_columns = 16
CreatePi_lcd_rows    = 2

# 初始化IIC地址，LCD的IIC地址为0x21
CreatePi_lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# 打开LCD背光
CreatePi_lcd.set_backlight(0)
# 程序入口
if __name__ == "__main__":
	try:
		while True:
			# 获取角色的位置
			x, y, z = CreatePi_mc.player.getPos()
			x, y, z = float(str(x)[:3]),float(str(y)[:3]),float(str(z)[:3])
			CreatePi_pos = str(x)+", "+str(y)+", "+str(z)
			print(CreatePi_pos)
			CreatePi_lcd.message('coordinates:\n%s' % CreatePi_pos)
			time.sleep(1)
			CreatePi_lcd.clear()
	except KeyboardInterrupt:
		# 按下 CTRL+C 键, 清除并退出脚本
		CreatePi_lcd.clear()
		CreatePi_lcd.set_backlight(1)