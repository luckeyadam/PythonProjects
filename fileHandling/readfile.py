file=open("./files/example.txt", 'r')

content = file.readlines()

print(content)

content = [i.rstrip("\n") for i in content]
print(content)
file.close()
