#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Original author WindVoiceVox
# Original Author Github: https://github.com/WindVoiceVox/Raspi_SG90
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：servo.py
#  版本：V2.0
#  author: zhulin
#  说明：在做这个项目的时候，要把指拨开关（BUTTON:UX2）的第8位拨到ON上，
#  做完实验之后，记得拔下来

# 导入相关的库
import RPi.GPIO as GPIO
import time
import sys
import atexit

class sg90:
  '''
    Raspberry pi上使Servo Motor SG90易于使用的类。
    需要RPi软件包。
    适用于带有Raspberry pi的易用伺服电机SG90的类。
  '''
  def __init__( self, pin, direction ):
    '''
    初始化。
    引脚：GPIO引脚号。可以使用PWM。
    方向：初始方向。指定从-100（最左边）到100（最右边）的整数。
    初始化类。
    引脚：GPIO引脚号，该引脚必须能够使用PWM。
    direction：初始伺服方向，介于-100到100之间。
    '''
    GPIO.setmode( GPIO.BOARD )
    GPIO.setwarnings(False)
    GPIO.setup( pin, GPIO.OUT )
    self.pin = int( pin )
    self.direction = int( direction )
    self.servo = GPIO.PWM( self.pin, 50 )
    self.servo.start(0.0)
    atexit.register( self.cleanup )

  def cleanup( self ):
    '''
    清理类
    '''
    self.servo.ChangeDutyCycle(self._henkan(0))
    time.sleep(0.3)
    self.servo.stop()
    GPIO.cleanup()

  def currentdirection( self ):
    '''
    返回当前的SG90方向。
    返回当前伺服方向。
    '''
    return self.direction

  def _henkan( self, value ):
    '''
    计算要传递给ChangeDutyCycle的值。
    -输入介于-100到100之间的浮点值，并返回介于2到12之间的值。
    传递给ChangeDutyCycle的值为0.0 <= dc <= 100.0
    应该是...但是出于某种原因它可以在2到12之间工作。
    '''
    return 0.05 * value + 7.0

  def setdirection( self, direction, speed ):
    '''
    更改SG90的方向。
    方向：-100到100之间的整数值
    速度：变化量
    设置SG90方向。
    方向：新的SG90方向。介于100到100之间。
    speed：移动速度，整数1至50。
    '''
    for d in range( self.direction, direction, int(speed) ):
      self.servo.ChangeDutyCycle( self._henkan( d ) )
      self.direction = d
      time.sleep(0.1)
    self.servo.ChangeDutyCycle( self._henkan( direction ) )
    self.direction = direction

#使用GPIO编号22
s = sg90( 22, 0 )
if __name__ == "__main__":
    try:
        while True:
          print("Turn left ...")
          s.setdirection( 100, 10 )
          time.sleep(0.5)
          print("Turn right ...")
          s.setdirection( -100, -10 )
          time.sleep(0.5)
    except KeyboardInterrupt:
        s.cleanup()

