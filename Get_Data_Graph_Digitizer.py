from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog


root = Tk()
root.title('GetData Graph Digitizer')
root.configure(bg = 'PeachPuff')
root.geometry()
root.resizable(width=True, height=True)
states = ["free", "scale", "coordinates", "free2"]
state = states[0]
kx = 1
ky = 1
coordinate_states = ["x minimum", "x maximum", "y minimum", "y maximum"]
coordinate_state = coordinate_states[0]
x_min = 0
x_max = 1
x_min_pixel = (1, 1)
x_max_pixel = (1, 1)
y_min = 0
y_max = 1
y_min_pixel = (1, 1)
y_max_pixel = (1, 1) 
x0 = 0
y0 = 0
old_x = 0
old_y = 0
is_first_click = True
canvas = None
cnt = 0


def point_capture():
    global state
    state = states[2]


def scale():
    global state
    state = states[1]
    zoom()


def coordinates_info(event):
    global kx
    global ky
    global x0
    global y0
    x, y = event.x, event.y
    label = Label(root, text='Current coordinates', font='System',bg = 'Moccasin',fg='SystemActiveCaption')
    label.pack()
    label['text'] = f'X: {(x - x0) / kx + x_min} , Y: {-(y - y0) / ky + y_min}'


def tracker(event):
    global imagesprite2
    global pilImage
    global imagetk
    if imagesprite2:
        canvas2.delete(imagesprite2)
    imagesprite2 = None
    imagetk = None
    canvas2.imagetk = None
    new_size = 3000, 1500
    imagetk = ImageTk.PhotoImage(pilImage.resize(new_size))
    imagesprite2 = canvas2.create_image((image.width()//2 - event.x)*5 +200,
                                        (image.height()//2 - event.y)*5+150,
                                        image=imagetk)
    canvas2.create_oval(197, 147, 203, 153, fill='red')


def zoom():
    global imagesprite2
    global pilImage
    global imagetk
    global canvas2
    newwin = Toplevel(root)
    newwin.configure(bg = 'PeachPuff')
    canvas2 = Canvas(newwin)
    canvas2.pack()
    image2 = ImageTk.PhotoImage(pilImage)
    imagesprite2 = canvas2.create_image(image.width()//2, image.height()//2, image=image)
    root.bind('<Motion>', tracker)


def openbutton():
    a = filedialog.askopenfilename(title='open')
    return a


def picture():
    global canvas
    x = openbutton()
    test(x)


def test(x):
    global canvas
    global pilImage
    global image
    canvas = Canvas(height = 300, width = 600, bg='PeachPuff')
    canvas.pack()
    pilImage = Image.open(x)
    image = pilImage.resize((600, 300))
    image = ImageTk.PhotoImage(image)
    canvas.create_image(image.width()//2, image.height()//2, image=image)
    root.mainloop()


def save(s, is_first_click):
    if is_first_click:
        with open('Coordinates.txt', 'w') as f:
            f.write(s + '\n')
    else:
        with open('Coordinates.txt' , 'a+') as f:
            f.write(s + '\n')  


def click(event):
    global state
    global coordinate_state
    global e
    global kx
    global ky
    global x0
    global y0
    global old_x
    global old_y
    global is_first_click
    x, y = event.x, event.y
    if state == states[2]:
        print(f"Current Coordinates = [X: {(x - x0) / kx + x_min} , Y: {-(y - y0) / ky + y_min}]")
        save(f"Current Coordinates = [X: {(x - x0) / kx + x_min} , Y: {-(y - y0) / ky + y_min}]", is_first_click)
        coordinates_info(event)
        if not is_first_click:
            canvas.create_line(old_x, old_y, x, y)
        else:
            is_first_click = False
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='SystemActiveCaption')
        old_x = x
        old_y = y
    elif state == states[1]:
        newwin = Toplevel(root)
        newwin.configure(bg = 'PeachPuff')
        if coordinate_state == coordinate_states[0]:
            lbl = Label(newwin, text='x minimum', font='System',bg = 'Moccasin',fg='SystemActiveCaption')
            e = Entry(newwin, width=20)
            lbl.pack()
            e.pack()
            def xminf():
                global coordinate_state
                global y0
                global x_min
                global x_min_pixel
                x_min = int(e.get())
                x_min_pixel = (x, y)
                coordinate_state = coordinate_states[1]
                y0 = y
                newwin.destroy()
            b = Button(newwin, text='ok', font='System',bg = 'Moccasin',fg='SystemActiveCaption', command=xminf).pack()
        elif coordinate_state == coordinate_states[1]: 
            lbl = Label(newwin, text='x maximum', font='System',bg = 'Moccasin',fg='SystemActiveCaption')
            e = Entry(newwin, width=20)
            lbl.pack()
            e.pack()
            def xmaxf():
                global coordinate_state
                global kx
                global x_max
                global x_max_pixel
                x_max = int(e.get())
                x_max_pixel = (x, y)
                coordinate_state = coordinate_states[2]
                kx = x_max_pixel[0] - x_min_pixel[0]
                kx = abs(kx / (x_max - x_min))
                newwin.destroy()        
            b = Button(newwin, text='ok', font='System',bg = 'Moccasin',fg='SystemActiveCaption', command=xmaxf).pack()
        elif coordinate_state == coordinate_states[2]: 
            lbl = Label(newwin, text='y minimum', font='System',bg = 'Moccasin',fg='SystemActiveCaption')
            e = Entry(newwin, width=20)
            lbl.pack()
            e.pack()
            def yminf():
                global coordinate_state
                global y_min
                global y_min_pixel
                global x0
                y_min = int(e.get())
                y_min_pixel = (x, y)
                coordinate_state = coordinate_states[3]
                x0 = x
                newwin.destroy()
            b = Button(newwin, text='ok', font='System',bg = 'Moccasin',fg='SystemActiveCaption', command=yminf).pack()        
        elif coordinate_state == coordinate_states[3]: 
            lbl = Label(newwin, text='y maximum', font='System',bg = 'Moccasin',fg='SystemActiveCaption')
            e = Entry(newwin, width=20)
            lbl.pack()
            e.pack()
            def ymaxf():
                global state
                global coordinate_state
                global y_max
                global y_max_pixel
                global ky
                y_max = int(e.get())
                y_max_pixel = (x, y)
                coordinate_state = coordinate_states[0]
                ky = y_max_pixel[1] - y_min_pixel[1]
                ky = abs(ky / (y_max - y_min))
                state = states[3]
                newwin.destroy()
            b = Button(newwin, text='ok', font='System',bg = 'Moccasin',fg='SystemActiveCaption', command=ymaxf).pack()


def main():
    btn1 = Button(root, text='Open Image', font='System',bg = 'Moccasin',fg='SystemActiveCaption', command=picture).pack()
    btn3 = Button(root, text='Set the scale', font='System',bg = 'Moccasin',fg='SystemActiveCaption', command=scale).pack()
    btn4 = Button(root, text='Point capture mode', font='System',bg = 'Moccasin',fg='SystemActiveCaption', command=point_capture).pack()
    btn2 = Button(root, text="Quit", font='System',bg = 'Moccasin',fg='SystemActiveCaption', command=root.destroy).pack()
    root.bind('<Button-3>', click)
    root.mainloop()


if __name__ == '__main__':
    main()
