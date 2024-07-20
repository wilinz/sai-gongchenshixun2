from mcpi.minecraft import Minecraft
mc = Minecraft.create()
#pos = mc.player.getPos()
x, y, z = mc.player.getPos()
x, y, z = float(str(x)[:3]),float(str(y)[:3]),float(str(z)[:3])
pos = "x="+str(x)+", "+"y="+str(y)+", "+"z="+str(z)
print(pos)