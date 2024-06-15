import aes

tool = aes.AESCipher("FIAP")

x = tool.encrypt('teste')
y = tool.encrypt('teste')
z = tool.encrypt('teste')

print(x, y, z)
print("\n")
_x = tool.decrypt(x)
_y = tool.decrypt(y)
_z = tool.decrypt(z)

print(_x, _y, _z)