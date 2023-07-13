import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmsgbox
import tkinter.filedialog as tkfile

from userinterface.visualisation.databasewindow import DatabaseWindow
from userinterface.visualisation.plotterwindow import PlotterWindow
from userinterface.visualisation.database import Database
from userinterface.mainwindow.output import Output
from userinterface.mainwindow.fileexplorer import FileExplorer
from userinterface.mainwindow.codecreator import CodeCreator
from calculate.solver import Solver

class MainWindow(tk.Tk):
    """ MainWindow is the main part of the program when used with GUI.
    Everthing starts here.
    """

    def __init__(self):
        """ Creates the MainWindow. """

        tk.Tk.__init__(self)

        self.__os_info = sys.platform
        # Style and Icon windows only
        if self.__os_info == 'win32':
            self.iconbitmap(
                os.getcwd() 
                + '\\resources\\pictures\\icon.ico')
            self.style = ttk.Style(self)
            self.style.theme_use('vista')

        # Configure Grid in Window
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # PARAMETER #
        self.__var_function = tk.StringVar(self)
        self.__var_restart_length = tk.IntVar(self, value=5)
        self.__var_restart_cycles = tk.IntVar(self, value=5)
        self.__var_stopping_accuracy = tk.StringVar(self, value='1.00e-2')
        self.__var_last_solver = Solver
        # DATABASE #
        database_columns = Solver.get_measurement_keys()
        self.__database_solver = Database(database_columns)

        # WINDOW
        self.title('Py Funm Quad')
        window_width = str(int(self.winfo_screenwidth()/2))
        window_height = str(int(self.winfo_screenheight()/2))
        self.geometry(#window_width + 'x' + window_height 
            '+' + str(int(self.winfo_screenwidth()/2)
            - int(int(window_width)/2))
            + '+' + str(int(self.winfo_screenheight()/2)
            - int(int(window_height)/2)))
        self.resizable(True,True)

        # MENUE
        self.menue_main_bar = tk.Menu(self)
        # Data Menue
        self.menue_data = tk.Menu(self.menue_main_bar, tearoff=0)
        self.menue_data.add_command(
            label='Change Workspace', underline=0,
            command= lambda: self.__change_drive())
        self.menue_data.add_command(
            label='Import Database', underline=0,
            command=lambda: self.__import_database())
        self.menue_data.add_command(
            label='Save Database', underline=0,
            command= lambda: self.__save_database())
        self.menue_data.add_command(
            label='New Database', underline=0,
            command= lambda: self.__new_database())
        self.menue_data.add_separator()
        self.menue_data.add_command(
            label='Exit', underline=0,
            command= lambda: self.__exit_program())
        # Export Menu
        self.menue_skript = tk.Menu(self.menue_main_bar, tearoff=0)
        self.menue_skript.add_command(
            label='Export Python (Path)', underline=1,
            command= lambda: self.__export_python_script('file'))
        self.menue_skript.add_command(
            label='Export Python (A,b)', underline=2,
            command= lambda: self.__export_python_script('Ab'))
        # Solver Menu
        self.menue_solver = tk.Menu(self.menue_main_bar, tearoff=0)
        self.menue_solver.add_command(
            label='Print Error Norms', underline=0,
            command= lambda: self.__print_errornorms_output())
        self.menue_solver.add_command(
            label='Save Approximation', underline=1,
            command= lambda: self.__save_last_approximation())
        # Merge Menues
        self.menue_main_bar.add_cascade(menu=self.menue_data,
            label='Data', underline=0)
        self.menue_main_bar.add_cascade(menu=self.menue_skript,
            label='Export', underline=0)
        self.menue_main_bar.add_cascade(menu=self.menue_solver,
            label='Solver', underline=0)
        # add Menue to Window
        self.configure(menu=self.menue_main_bar)

        # FRAMES 
        # File Explorer
        self.frame_explorer = ttk.LabelFrame(
            self, relief='groove', text='File')
        self.frame_explorer.grid(
            row=0, column=0, rowspan=2,
            padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        self.frame_explorer.grid_columnconfigure(0, weight=1)
        self.frame_explorer.grid_columnconfigure(1, weight=0)
        self.frame_explorer.grid_rowconfigure(0, weight=1)
        self.frame_explorer.grid_rowconfigure(1, weight=0)
        # Parameterframe
        self.frame_parameter = ttk.LabelFrame(
            self, relief='groove', text='Parameter')
        self.frame_parameter.grid(
            row=0, column=1, padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        self.frame_parameter.grid_columnconfigure(0, weight= 1)
        self.frame_parameter.grid_columnconfigure(1, weight= 1)
        self.frame_parameter.grid_rowconfigure(0,weight=1)
        self.frame_parameter.grid_rowconfigure(1, weight=1)
        # Functionsframe
        self.frame_radio = ttk.LabelFrame(self.frame_parameter, 
                                          relief='groove')
        self.frame_radio.grid(
            row=0, column=0, padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        # Lenghtframe
        self.frame_scale = ttk.LabelFrame(self.frame_parameter, 
                                          relief='groove')
        self.frame_scale.grid(
            row=0, column=1, padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        self.frame_parameter.grid_rowconfigure(0,weight=1)
        self.frame_parameter.grid_rowconfigure(1, weight=1)
        # Optionsframe
        self.frame_options = ttk.LabelFrame(
            self.frame_parameter, relief='groove')
        self.frame_options.grid(
            row=1, column=0, padx=(5,5), pady=(5,5), sticky=tk.NSEW)

        # Controlbuttonsframe
        self.frame_button = ttk.LabelFrame(
            self, relief='groove', text='Control')
        self.frame_button.grid(
            row=1, column=1, padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        # Outputframe
        self.frame_output = ttk.LabelFrame(
            self, relief='groove', text='Output')
        self.frame_output.grid(
            row=2, column=0, columnspan=2,
            padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        self.frame_output.grid_columnconfigure(0, weight=1)
        self.frame_output.grid_rowconfigure(0, weight=1)

        # Commando Output
        self.text_output = tk.Text(
            self.frame_output, state='disabled',height=6)
        self.text_output.grid(
            row=0, column=0, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.NSEW)
        # Comanndo Print
        self.output = Output(self.text_output)
        self.output.entry_log('Py Funm Quad has started')

        # Radiobuttons
        self.radio_inverse = ttk.Radiobutton(
            self.frame_radio, text='Inverse Squareroot',
            variable=self.__var_function, value='invsqrt',
            command=lambda: self.__radio_function())
        self.radio_inverse.grid(
            row=0, column=0, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        self.radio_inverse.invoke()
        self.radio_log = ttk.Radiobutton(
            self.frame_radio, text='log(1+A)/A', variable=self.__var_function,
            value='log', command=lambda: self.__radio_function())
        self.radio_log.grid(
            row=1, column=0, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        self.radio_exp = ttk.Radiobutton(
            self.frame_radio, text='exp(A)', variable=self.__var_function,
            value='exp', command=lambda: self.__radio_function())
        self.radio_exp.grid(
            row=2, column=0, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        
        # Scale
        self.scale_restart = tk.Scale(
            self.frame_scale, label='Restart length', orient='horizontal',
            from_=5, to=100, showvalue=1, variable=self.__var_restart_length)
        self.scale_restart.grid(
            row=0, column=0, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        self.scale_cycles = tk.Scale(
            self.frame_scale, label='Restart Cycles', orient='horizontal',
            from_=1, to=50, showvalue=1, variable=self.__var_restart_cycles)
        self.scale_cycles.grid(
            row=0, column=1, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        self.label_stopping = ttk.Label(self.frame_scale, 
                                        text='Stopping accuracy')
        self.label_stopping.grid(row=1, column=0, padx=(5,5), pady=(5,5), 
                                 ipadx=5, ipady=5, sticky=tk.W)
        self.entry_stopping = ttk.Entry(
            self.frame_scale, textvariable=self.__var_stopping_accuracy, 
            foreground='red')
        self.entry_stopping.grid(row=1, column=1, padx=(5,5), pady=(5,5), 
                                 ipadx=5, ipady=5, sticky=tk.W)

        # FileExplorer
        if self.__os_info == 'win32':
            self.treeview_file = FileExplorer(
                self.frame_explorer, 'C:\\', self.output)
        else:
            self.treeview_file = FileExplorer(
                self.frame_explorer, '/home', self.output)
        self.treeview_file.grid(row=0, column=0, sticky=tk.NSEW)
        # Scrollbars
        self.scrollbar_horizontal = ttk.Scrollbar(
            self.frame_explorer, orient='horizontal',
            command=self.treeview_file.xview)
        self.scrollbar_horizontal.grid(
            row=1, column=0, columnspan=2, sticky=tk.EW)
        self.treeview_file.configure(
            xscrollcommand=self.scrollbar_horizontal.set)
        self.scrollbar_vertical = ttk.Scrollbar(
            self.frame_explorer, orient='vertical',
            command=self.treeview_file.yview)
        self.scrollbar_vertical.grid(row=0, column=1, sticky=tk.NS)
        self.treeview_file.configure(
            yscrollcommand= self.scrollbar_vertical.set)
        self.output.entry_log(('Fileexplorer creation successful'))

        # Buttons
        self.button_solve = ttk.Button(
            self.frame_button, text='Solve',
            command=lambda: self.__solve_equation())
        self.button_solve.grid(
            row=0, column=0, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W + tk.EW)
        self.button_plot_database = ttk.Button(
            self.frame_button, text='Plotter and Settings',
            command=lambda: self.__show_plotterwindow())
        self.button_plot_database.grid(
            row=0, column=1, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W + tk.EW)
        self.button_show_database = ttk.Button(
            self.frame_button, text='Show Database',
            command=lambda: self.__show_database())
        self.button_show_database.grid(
            row=0, column=2, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W + tk.EW)        


    # Return all Parameter
    def __get_solve_parameter(self):
        """ Returns all parameters that are chossen in the GUI. """

        try:
            stopping_accuracy = float(self.__var_stopping_accuracy.get())
        except ValueError:
            self.output.entry_err('Stopping accuracy set to 1.00e-2')
            stopping_accuracy = 1.00e-2
        parameter = {
            'file' : self.treeview_file.get_filepath(),
            'function' : self.__var_function.get(),
            'length' : self.__var_restart_length.get(),
            'cycles' : self.__var_restart_cycles.get(),
            'stopping_accuracy' : stopping_accuracy,
            'output' : self.output,
            'stopping_accuracy' : stopping_accuracy,
            # 'inner_product' : Implemented in Algorithm
        }
        return parameter

    # Menue Commands
    def __change_drive(self):
        """ Change root in file explorer. """

        drive = tkfile.askdirectory(initialdir=os.getcwd())
        if drive == None or drive == '':
            self.output.entry_err(
                'No directory change possible. Please choose a directory.')
        else:
            try:
                self.treeview_file.change_harddrive(drive)
            except NotADirectoryError as err:
                self.output.entry_err(err.args[0])  

    def __import_database(self):
        """ Import a databse into the programm.
        For more information read Database doc.
        """

        try:
            self.__database_solver = Database(
                parameter = None, 
                dataframe = self.__database_solver.import_database())
            self.output.entry_log('Database imported.')
        except NotImplementedError:
            self.output.entry_err('Database format not supported.')
    
    def __save_database(self):
        """ Save a databse into a file.
        For more information read Database doc.
        """

        try:
            self.__database_solver.save_to_file()
            self.output.entry_log('Database saved.')
        except NotImplementedError:
            self.output.entry_err('Format not supported.')

    def __new_database(self):
        """ Resets databse. """

        database_columns = Solver.get_measurement_keys()
        self.__database_solver = Database(database_columns)

    def __export_python_script(self, file_type):
        """ Export a python script with your actual parameters. """
        try:
            CodeCreator(file_type, self.__get_solve_parameter())
            self.output.entry_log('File successfully exported.')
        except NameError:
            self.output.entry_err('File must be a Pythonfile!')
            
    def __print_errornorms_output(self):
        """ Print error norms of last solver. """
        
        try:
            self.output.entry_parameter('Error Norms:',
                str(self.__var_last_solver.get_error_norms()))    
        except:
            self.output.entry_err('No function solved yet.')

    def __save_last_approximation(self):
        """ Save approximation of last solver. """
        
        try:
            self.__var_last_solver.save_approx_to_file()
            self.output.entry_log('Approximation saved.')
        except:
            self.output.entry_err('No function solved yet.')

    # Radiobuttoncommands
    def __radio_function(self):
        """ Select function to solve. """

        value = self.__var_function.get()
        self.output.entry_log(str(value + ' has been selected'))

    # Buttoncommands
    def __show_plotterwindow(self):
        """ Start Plotterwindow to visualize data."""

        try:
            PlotterWindow(self, self.__database_solver)
            self.output.entry_log('Plotter started')
        except:
            self.output.entry_err('Nothing to plot. Import or solve.')

    def __show_database(self):
        """ Opens a window to have a look into the database. """
        DatabaseWindow(self, self.__database_solver)
        self.output.entry_log('Showing Database')

    def __solve_equation(self):
        """ Get Parameters and solve choosen function. """
        parameter = self.__get_solve_parameter()
        try:
            parameter = self.__get_solve_parameter()
            if os.path.isfile(parameter['file']):
                    solved = Solver(parameter)
                    try:
                        self.__database_solver.append_datarow(
                            solved.get_measurment())
                    except:
                        raise RuntimeError('Please try again.') 
            else:
                raise FileNotFoundError('No file to compute.')
            self.__var_last_solver = solved
        except (FileNotFoundError, NotImplementedError, RuntimeError) as err:
            self.output.entry_err(err.args[0])   

    def __exit_program(self):
        """ Exits the program. """
        if tkmsgbox.askyesno('Quit','Do you really want to quit?'):
            self.destroy()