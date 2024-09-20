from PIL import Image
import math

#chars = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """[::-1]
chars = """@%#*+=-:. """[::-1]
#chars = """. """#[::-1]
#chars = """!\"#$%&'()*+,-./:;<=>?@[\\]^_{|}~ """
#chars = """1234567890+-/*= """

#program built for jpg and jpeg file types, 
try:
    im = Image.open("input.jpg")
except:
    im=Image.open("input.jpeg")


w,h=im.size
pix=im.load()

#converting to grayscale
for i in range(w):
    for j in range(h):
        r,g,b=pix[i,j]

        #average method: assign average of r,g,b to the pixel
        #a=int((r+g+b)/3)
        
        #luminosity method: assigns the weighted average
        a=int((0.3*r)+(0.59*g)+(0.11*b))

        pix[i,j]=(a,a,a)

im.save("output.png")

im=Image.open("output.png")

#resize the img as ASCII chars are longer in height
#ht*wd = 86*34
#w*h
newSize=(int(86),34)
im=im.resize(newSize)
pix=im.load()
w,h=im.size

#writes ASCII characters in txt file
file=open("output.txt","w")
for j in range(h):
    for i in range(w):
        a,a,a=pix[i,j]
        file.write(chars[int((a/256)*len(chars))])
    file.write("\n")