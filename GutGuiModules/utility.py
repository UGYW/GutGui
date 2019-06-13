from tkinter import *

from GutGuiModules.constants import *


def init():
    root = Tk()
    root.resizable(width=False, height=False)
    root.title(WINDOW_TITLE)
    root.geometry("+0+0")
    window = Frame(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    window.pack()
    return window

def tkcolour_from_rgb(rgb):
    '''translates an rgb tuple of int to a tkinter friendly color code'''
    return "#%02x%02x%02x" % rgb

def frame_and_label(window, name, colour, width, height, row, column, rowspan, columnspan):
    frame = Frame(window, bg=tkcolour_from_rgb(colour))
    frame.grid(row=row, rowspan=rowspan, column=column, columnspan=columnspan, sticky=W+E+N+S)
    label = make_label(frame, text=name, row=0, column=0, borderwidth=2)
    return frame, label

def make_button(window, text, command, row, column, height=1, width=10, 
    inner_padx=10, inner_pady=10, outer_padx=0, outer_pady=0, columnspan=1):
    button = Button(window, text=text, command=command, padx=inner_padx, pady=inner_pady, height=height, width=width)
    button.grid(row=row, column=column, padx=outer_padx, pady=outer_pady)
    return button

def make_label(window, text, row, column,
               borderwidth=2, inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=(10,0), relief="solid"):
    label = Label(window, text=text, borderwidth=borderwidth, relief=relief, padx=inner_padx, pady=inner_pady)
    label.grid(row=row, column=column, padx=outer_padx, pady=outer_pady)
    return label

def make_text(window, content, row, column, padx=10, pady=5, height=1, width=2, highlightthickness=0, bg="white", columnspan=1):
    text = Text(window, bg=bg, height=height, width=width, highlightthickness=highlightthickness)
    text.insert(END, content)
    text.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)
    return text

def make_listbox(window, input, row, column, padx=10, pady=10, highlightthickness=0):
    listbox = Listbox(window)
    listbox.grid(row=row, column=column, rowspan=2, padx=padx, pady=pady)
    return listbox

def make_entry(window, row, column, width, columnspan, pady=10, 
    padx=10, highlightthickness=0):
    entry = Entry(window, width=width)
    entry.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return entry


# def make_pop_up(message, title="Warning"):
#     popup = Tk()
#     popup.wm_title(title)
#     label = Label(popup, text=message)
#     label.pack(side="top", fill="x", pady=10)
#     B1 = Button(popup, text="Ok", command = popup.destroy)
#     B1.pack()
#     popup.mainloop()