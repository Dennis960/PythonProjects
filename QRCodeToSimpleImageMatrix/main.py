from PIL import Image

codeRaw = Image.open("Code.png")
width = codeRaw.width
height = codeRaw.height

offsetLeft = 10
offsetTop = 8
offsetBottom = 8
offsetRight = 9
pixelAmount = 29

mat = []

for x in range(offsetLeft, width-offsetRight+1, round((width-offsetLeft-offsetRight)/pixelAmount)):
    row = []
    for y in range(offsetTop, width-offsetBottom+1, round((width-offsetTop-offsetBottom)/pixelAmount)):
        pixel = codeRaw.getpixel((x, y))[0]
        if pixel > 100:
            row.append(0)
        else:
            row.append(1)
    mat.append(row)

img = Image.new('RGB', (pixelAmount, pixelAmount), color='white')
pixels = img.load()
for x, row in enumerate(mat):
    for y, isBlack in enumerate(row):
        if isBlack:
            pixels[x, y] = (0, 0, 0)


img.save('newCode.png')