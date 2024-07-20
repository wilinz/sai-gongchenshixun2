#!/usr/bin/python
# -*- coding: utf-8 -*-

# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：segment.py
#  版本：V2.0
#  author: zhulin

import time
import datetime
from Adafruit_LED_Backpack import SevenSegment

makerobo_segment = SevenSegment.SevenSegment(address=0x70)
# ===========================================================================
# 4位七段数码管显示树莓派系统时间显示的案例
# ===========================================================================
def makerobo_setup():
  # 初始化显示。在使用数码管显示前必须调用一次。
  makerobo_segment.begin()
  print("Press CTRL+C to exit")

# 持续更新4个字符、7段显示的时间
# 程序入口
if __name__ == "__main__":
  try:
    makerobo_setup()    # 初始化
    while(True):
      time_now = datetime.datetime.now()  # 获取时间
      time_hour = time_now.hour  # 获取小时
      time_minute = time_now.minute # 获取分钟
      time_second = time_now.second # 获取秒

      makerobo_segment.clear() # 清除一下显示
      # 设置小时
      makerobo_segment.set_digit(0, int(time_hour / 10))     # 取十位
      makerobo_segment.set_digit(1, time_hour % 10)          # 取个位
      # 设置分钟
      makerobo_segment.set_digit(2, int(time_minute / 10))   # 取十位
      makerobo_segment.set_digit(3, time_minute % 10)        # 取个位
      # 切换冒号
      makerobo_segment.set_colon(time_second % 2)            # 控制点位闪烁

      # 将显示缓冲区写入硬件。
      # 必须调用此函数才能更新实际的显示led。
      makerobo_segment.write_display()

      # 等待1/4秒(少于1秒以防止冒号闪烁）
      time.sleep(0.25)
  except KeyboardInterrupt:
      makerobo_segment.clear()  # 释放资源
      makerobo_segment.write_display() # 清空显示