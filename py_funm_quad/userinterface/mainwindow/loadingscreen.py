import os
import sys
import tkinter as tk

from PIL import Image, ImageTk


class LoadingScreen(tk.Tk):
    """ Looadingscreen only needed for shorten the waiting time on startup. """
    
    def __init__(self):
        """ Creates a Window with an image. No other functions. """
        tk.Tk.__init__(self)

        window_width = str(int(self.winfo_screenwidth()/2))
        window_height = str(int(self.winfo_screenheight()/2))
        self.geometry(window_width + 'x' + window_height 
            +'+' + str(int(self.winfo_screenwidth()/2)
            - int(int(window_width)/2))
            + '+' + str(int(self.winfo_screenheight()/2)
            - int(int(window_height)/2)))
        self.resizable(False,False)
        self.title('Programm wird geladen...')
        if sys.platform == 'win32':
            self._image = ImageTk.PhotoImage(
                Image.open(os.getcwd() 
                + '\\resources\\pictures\\intro.png').resize(
                    (int(window_width), int(window_height))))
        else:
            self._image = ImageTk.PhotoImage(
                Image.open(os.getcwd() 
                + '/resources/pictures/intro.png').resize(
                    (int(window_width), int(window_height))))

        self.label_image = tk.Label(self, image=self._image)
        self.label_image.pack(fill='both')

    def quit(self):
        """ Closes the Loadingscreen. """
        self.destroy()