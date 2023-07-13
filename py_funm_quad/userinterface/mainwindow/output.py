from tkinter import END, Text
from datetime import datetime


class Output:
    """ Output is used for a console on the GUI. 
    It is used to give information to the user.
    """
    
    def __init__(self, textbox:Text):
        """ Needs a tkinter Text widget where messages can be displayed. """

        self.textbox = textbox
    
    def entry_log(self, message:str):
        """ Displayes a message. """

        time_now = datetime.now()
        stamp = time_now.strftime('%H:%M:%S')
        self.textbox.config(state='normal')
        self.textbox.insert(END, ('LOG: [' + stamp + '] : ' + message + '\n'))
        self.textbox.config(state='disabled')
        self.textbox.see(END)
        self.textbox.update()
    
    def entry_err(self, message:str):
        """ Displayes an error message. """

        time_now = datetime.now()
        stamp = time_now.strftime('%H:%M:%S')
        self.textbox.config(state='normal')
        self.textbox.insert(END, ('ERR: [' + stamp + '] : ' + message + '\n'))
        self.textbox.config(state='disabled')
        self.textbox.see(END)
        self.textbox.update()

    def entry_warn(self, message:str):
        """ Displayes a warning. """

        time_now = datetime.now()
        stamp = time_now.strftime('%H:%M:%S')
        self.textbox.config(state='normal')
        self.textbox.insert(END, ('WNG: [' + stamp + '] : ' + message + '\n'))
        self.textbox.config(state='disabled')
        self.textbox.see(END)
        self.textbox.update()

    def entry_parameter(self, name, parameter):
        """ Displayes an info with a parameter value """

        time_now = datetime.now()
        stamp = time_now.strftime('%H:%M:%S')
        self.textbox.config(state='normal')
        self.textbox.insert(END, ('INF: [' + stamp + '] : ' + name 
            + '\n' + str(parameter) + '\n'))
        self.textbox.config(state='disabled')
        self.textbox.see(END)
        self.textbox.update()