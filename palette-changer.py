from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import filedialog, colorchooser
import os
import sys


root = tk.Tk()
root.title("Palette Changer")
icon = tk.PhotoImage(file = os.path.join(sys.path[0], "palette-changer.ico"))
root.iconphoto(False, icon)

canvas = tk.Canvas(root, width = 500, height = 400)

colorsLabel = {}
colorsDict = {}


def rgb_to_hex(rgb):
    return ('#{:02X}{:02X}{:02X}').format(rgb[0], rgb[1], rgb[2])

def hex_to_rgb(hex):
    return np.array(tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))

def choose_color(x, oldColor, imageFile, label):
    newColor = colorchooser.askcolor(title = "Choose color")
    oldColor = hex_to_rgb(oldColor[1:])

    # change image color here
    
    rgba_img_disp = np.array(imageFile.convert(matrix = "RGB"), dtype = np.uint8)

    if len(rgba_img_disp[0, 0]) == 4:
        for r in range(len(rgba_img_disp)):
            for c in range(len(rgba_img_disp[0])):
                if rgba_img_disp[r, c, 3] == 0:
                    continue

                if np.array_equal(oldColor, rgba_img_disp[r, c, 0:3]):
                    newColorWAlpha = np.append(newColor[0], 255)
                    rgba_img_disp[r, c] = newColorWAlpha
    else:
        for r in range(len(rgba_img_disp)):
            for c in range(len(rgba_img_disp[0])):
                if np.array_equal(oldColor, rgba_img_disp[r, c]):
                    rgba_img_disp[r, c] = newColor[0]

    newImgFile = Image.fromarray(rgba_img_disp)
    newImg = ImageTk.PhotoImage(newImgFile)

    # change button color here
    colorsDict[x] = newColor[1]
    colorsLabel[x].configure(bg = newColor[1])

    for k in colorsLabel.keys():
        hexColor = colorsDict[k]
        colorsLabel[k].configure(command = lambda k = k, hexColor = hexColor, newImgFile = newImgFile, label = label: choose_color(k, hexColor, newImgFile, label))

    label.configure(image = newImg)
    label.image = newImg

    saveButton.configure(state = "normal", command = lambda newImgFile = newImgFile: export_image(newImgFile))


def choose_image():
    global img
    global colorsLabel
    global filename

    # showing the original image
    f = filedialog.askopenfilename(title = "Open Image", filetypes = (("PNG", "*.png"), ("GIF", "*.gif")))
    imgFile = Image.open(f)
    img = ImageTk.PhotoImage(imgFile)
    label = tk.Label(image = img)
    canvas.create_window(10, 40, window = label, anchor="nw")

    rgba_img = np.array(imgFile.convert(matrix = "RGB"), dtype = np.uint8)

    colors = set()

    for row in rgba_img:
        for pixel in row:
            colors.add(tuple(pixel))

    if len(rgba_img[0][0]) == 4:
        colors = [x[0:3] for x in colors if x[3] != 0]
    else:
        colors = [x for x in colors]

    for i in range(len(colors)):
        hexColor = rgb_to_hex(colors[i])
        colorsLabel[i] = tk.Button(bg = hexColor, width = 1, height = 1, command = lambda i = i, hexColor = hexColor, imgFile = imgFile, label = label: choose_color(i, hexColor, imgFile, label))
        colorsDict[i] = rgb_to_hex(colors[i])
        canvas.create_window(490, 10 + (40 * i), window = colorsLabel[i], anchor = "ne")

    saveButton.configure(state = "normal", command = lambda imgFile = imgFile: export_image(imgFile))
    selectButton.configure(state = "disabled")


def export_image(imageFile):
    f = filedialog.asksaveasfile(title = "Save Image", mode = "a", defaultextension = ".png", filetypes=[(".png", "PNG")])
    if not f:
        return

    abs_path = os.path.abspath(f.name)
    imageFile.save(abs_path)
    print("Done")


selectButton = tk.Button(root, text = "Select image", command = choose_image)
canvas.create_window(10, 10, window = selectButton, anchor= "nw")

saveButton = tk.Button(root, text = "Export image", state = "disabled")
canvas.create_window(10, 390, window = saveButton, anchor= "sw")

canvas.pack()
root.mainloop()