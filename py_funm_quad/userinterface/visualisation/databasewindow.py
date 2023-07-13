import sys
import tkinter as tk
import tkinter.ttk as ttk


class DatabaseWindow(tk.Toplevel):
    """ DatabaseWindow is there to have a look into the Database.
    Without error_norms and eigenvalues.
    """

    def __init__(self, master, database):
        """ Opens a window with the Database that is 
        actually stored in MainWindow.
        """

        tk.Toplevel.__init__(self, master)
        # windows only
        if sys.platform == 'win32':
            self.style = ttk.Style(self)
            self.style.theme_use('vista')

        # Menue
        self.main_menue_bar = tk.Menu(self)
        # Data Menue
        self.data_menue = tk.Menu(self.main_menue_bar, tearoff=0)
        self.data_menue.add_command(label='Export Database', underline=0, 
            command=lambda: database.safe_to_file())
        # Merge Menues
        self.main_menue_bar.add_cascade(menu=self.data_menue, 
            label='Data', underline=0)
        # add Menue to Window
        self.configure(menu=self.main_menue_bar)

        # Frame
        self.frame_main = tk.Frame(self)
        self.frame_main.grid(row=0, column=0)
        # Prepare Columns Headertext
        db_header = list(['Nr.'])
        for val in database.columns.values.tolist():
            if val != 'Eigenvalues' and val != 'Error_norms':
                db_header.append(val)
        column_width = int((self.winfo_screenwidth()-50)/len(db_header))
        
        # Create Treeviewtool
        self.view_window = ttk.Treeview(self.frame_main, 
                                        columns=db_header, show='headings')
        self.view_window.grid(row=0, column=0, sticky=tk.NSEW)
        self.view_window['columns'] = db_header
        # Delete 'Ghost Column'
        self.view_window.column('#0', width = 0, stretch=tk.NO)
        # Create Columns and Heading
        for value in db_header:
            self.view_window.column(value, anchor=tk.CENTER, 
                                    width=column_width)
        for value in db_header:
            self.view_window.heading(value, text=value, anchor=tk.CENTER)
        # Fill each row
        for x in database.index:
            value = database.return_datarow_window(x)
            self.view_window.insert('', index=x, iid=x, text='', values=value)

        # Scrollbars
        self.scrollbar_horizontal = ttk.Scrollbar(
            self.frame_main, orient='horizontal',
            command=self.view_window.xview)
        self.scrollbar_horizontal.grid(
            row=1, column=0, columnspan=2, sticky=tk.EW)
        self.view_window.configure(
            xscrollcommand=self.scrollbar_horizontal.set)
        self.scrollbar_vertical = ttk.Scrollbar(
            self.frame_main, orient='vertical',
            command=self.view_window.yview)
        self.scrollbar_vertical.grid(row=0, column=1, sticky=tk.NS)
        self.view_window.configure(
            yscrollcommand= self.scrollbar_vertical.set)