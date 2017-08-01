# write a single line to file
file=open("./files/examplewrite.txt", 'w')
file.write("Line 1\n")
file.close()

# append to file
file=open("./files/examplewrite.txt", 'a')
file.write("Line 2\n")
file.close()

# using with statement
with open("./files/examplewrite.txt", 'a+') as file:
   file.seek(0)
   content=file.read()
   file.write("with\n")
