from mcpi.minecraft import Minecraft

mc = Minecraft.create()
x,y,z = mc.player.getPos() # player position (x, y, z)
tnt = 46
#mc.setBlock(x, y, z, tnt,1)
mc.setBlocks(x+1, y+1, z+1, x+11, y+11, z+11, tnt, 1)