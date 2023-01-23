import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
import numpy as np
import os, sys

# constants

HEIGHT_WINDOW = 400
WIDTH_WINDOW = 500

MAX_HEIGHT_VIEWER = 0
MAX_WIDTH_VIEWER = 0

# class

class Session():
    def __init__(self):
        self.filename = None
        self.image = None
        self.height = 0
        self.width = 0

        self.viewer = tk.Label()

        self.buttons = {}
        self.buttonColors = {}
        self.state = []     # for undo/redo
        self.stateIndex = 0
        
        self.zoom = 100     # for zoom in/out


    def save_image(self):
        f = filedialog.asksaveasfile(title = "Save Image", mode = "a", defaultextension = ".png", filetypes=[(".png", "PNG")])
        if not f:
            return

        abs_path = os.path.abspath(f.name)
        self.image.save(abs_path)
        print("Done")

    def undo(self):
        pass

    def redo(self):
        pass

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def choose_image(self):
        self.filename = filedialog.askopenfilename(title = "Open Image", filetypes = (("PNG", "*.png"), ("GIF", "*.gif")))
        self.image = Image.open(self.filename)
        self.show_image()
        
    
    def show_image(self):
        img = ImageTk.PhotoImage(self.image)
        self.viewer.configure(image = img)
        self.viewer.photo = img

        canvas.create_window(10, 40, window = self.viewer, anchor = "nw")

        # additional GUI buttons

        exportButton = tk.Button(root, text = "Save Image", command = self.save_image)
        canvas.create_window(10, 390, window = exportButton, anchor = "sw")

        # zoom in/out buttons
        # undo/redo buttons
        # scroll buttons (if needed)
        
        self.get_colors()

    def get_colors(self):
        rgba_img = np.array(self.image.convert(matrix = "RGB"), dtype = np.uint8)

        colors = set()

        for row in rgba_img:
            for pixel in row:
                colors.add(tuple(pixel))

        if len(rgba_img[0][0]) == 4:
            colors = [x[0:3] for x in colors if x[3] != 0]      # filter out transparent pixels and convert to list
        else:
            colors = [x for x in colors]        # convert to list

        for i in range(len(colors)):
            self.buttonColors[i] = rgb_to_hex(colors[i])
            self.buttons[i] = tk.Button(bg = self.buttonColors[i], width = 1, height = 1, command = lambda i = i: self.change_color(i))
            canvas.create_window(490, 10 + (40 * i), window = self.buttons[i], anchor = "ne")


    def change_color(self, id):
        newColor = colorchooser.askcolor(title = "Choose color")
        oldColor = hex_to_rgb(self.buttonColors[id][1:])      # remove the hashtag then convert to RGB

        if newColor[1] == None:
            return
    
        rgba_img_disp = np.array(self.image.convert(matrix = "RGB"), dtype = np.uint8)

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

        self.image = Image.fromarray(rgba_img_disp)

        self.viewer.image = ImageTk.PhotoImage(self.image)
        self.viewer.configure(image = self.viewer.image)

        self.buttonColors[id] = newColor[1]
        self.buttons[id].configure(bg = self.buttonColors[id])



# functions

def new_session():
    session = Session()
    session.choose_image()

def rgb_to_hex(rgb):
    return ('#{:02X}{:02X}{:02X}').format(rgb[0], rgb[1], rgb[2])

def hex_to_rgb(hex):
    return np.array(tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))


# GUI

root = tk.Tk()
root.title("Palette Changer")
icon = tk.PhotoImage(file = os.path.join(sys.path[0], "palette-changer.ico"))
root.iconphoto(False, icon)

canvas = tk.Canvas(root, width = WIDTH_WINDOW, height = HEIGHT_WINDOW)

newImageButton = tk.Button(root, text = "New Image", command = new_session)
canvas.create_window(10, 10, window = newImageButton, anchor = "nw")


canvas.pack()
root.mainloop()