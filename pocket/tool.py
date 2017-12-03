from PIL import Image, ImageDraw

black = (0, 0, 0)
white = (255, 255, 255)
im = Image.new("RGBA", (100, 50), (0, 100, 0, 50))

im.show()
im.save("target.PNG")

