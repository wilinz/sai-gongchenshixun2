#!/usr/bin/python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：lcd.py
#  版本：V2.0
#  author: zhulin
#  说明：IIC LCD1602液晶实验模块项目

# 导入LCD  Adafruit 库
import time
import Adafruit_CharLCD as LCD


# 定义16x2液晶显示器的列和行大小。
lcd_columns = 16
lcd_rows    = 2

# Alternatively specify a 20x4 LCD.
# lcd_columns = 20
# lcd_rows    = 4

# 初始化IIC 总线 LCD模块
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# 打开背光
lcd.set_backlight(0)

# 打印两行信息
lcd.message('Makerobot Hello\nworld!')

# 等待5秒
time.sleep(5.0)

# 演示显示光标。
lcd.clear()
lcd.show_cursor(True)
lcd.message('Show cursor')

time.sleep(5.0)

# 显示闪烁光标的演示。
lcd.clear()
lcd.blink(True)
lcd.message('Blink cursor')

time.sleep(5.0)

# 停止闪烁和显示光标。
lcd.show_cursor(False)
lcd.blink(False)

# 演示左右滚动信息。
lcd.clear()
message = 'Makerobo'
lcd.message(message)
for i in range(lcd_columns-len(message)):
    time.sleep(0.5)
    lcd.move_right()
for i in range(lcd_columns-len(message)):
    time.sleep(0.5)
    lcd.move_left()

# 演示如何关闭和打开背光。
lcd.clear()
lcd.message('Flash backlight\nin 5 seconds...')
time.sleep(5.0)
# 关闭背光。
lcd.set_backlight(0)
time.sleep(2.0)
# Change message.
lcd.clear()
lcd.message('Thank you for \n using!')
time.sleep(2.0)
# Turn backlight on.
lcd.set_backlight(1)