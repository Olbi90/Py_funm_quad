import os
import sys
import tkinter.ttk as ttk
import tkinter as tk

from userinterface.mainwindow.output import Output

# https://stackoverflow.com/questions/36972402/tree-tk-file-explorer
# was used as an inspiration for the function __startup_tree

class FileExplorer(ttk.Treeview):
    """ FileExplorer creates a Treeview widget to use as a file explorer. """

    def __init__(self, master, mount, output:Output):
        """ Creates a FileExplorer object.
        master : tkinter widget
        mount : path to show on creation
        output : textwidget to show messages, optional
        """

        ttk.Treeview.__init__(self, master)
        self.output = output
        self.output.entry_log(('Start Fileexplorer'))
        # Mount Variable
        self.var_drive = tk.StringVar(self, value=mount)
        self.var_file = tk.StringVar(self, value='EMPTY')
                
        self.heading('#0', text='Directory', anchor=tk.W)
        self.column('#0', stretch=True, minwidth=500)

        self.root = self.insert('', tk.END, text=mount)
        self.__startup_tree(self.var_drive.get(), self.root, 0)
        
        self.bind('<<TreeviewSelect>>', self.__choose_file)

    def __startup_tree(self, path, parent, k):
        """ Fills the widget recursive with a directory tree. """

        if sys.platform == 'win32':
            for sub_dir in os.listdir(path):
                if sub_dir != 'Windows':
                    new_dir = os.path.join(path + r'\\' + sub_dir)
                    item_value = str(str(path) + r'\\' + str(sub_dir))
                    parent_dir = self.insert(
                        parent, tk.END, value=item_value, text=sub_dir)
                    if os.path.isdir(new_dir):
                        try:
                            self.__startup_tree(new_dir,parent_dir, k)
                            k = 1
                        except:
                            if k == 0:
                                self.output.entry_log(
                                ('Permission Denied in' 
                                + ' some System Directorys'))
                            k = 1
        else:
            for sub_dir in os.listdir(path):
                if sub_dir != 'root':
                    if sub_dir.startswith('.') != True:
                        new_dir = os.path.join(path + r'/' + sub_dir)
                        item_value = str(str(path) + r'/' + str(sub_dir))
                        parent_dir = self.insert(
                            parent, tk.END, value=item_value, text=sub_dir)
                        if os.path.isdir(new_dir):
                            try:
                                self.__startup_tree(new_dir,parent_dir, k)
                                k = 1
                            except:
                                if k == 0:
                                    self.output.entry_log(
                                    ('Permission Denied in' 
                                    + ' some System Directorys'))
                                k = 1

    def __choose_file(self, event):
        """ Sets the path to the file, that has been choosen. """

        file = self.focus()
        if sys.platform == 'win32':
            if len(self.item(file, 'value')) > 1:
                file_path = self.item(file, 'value')[0]
                for i in range(1,len(self.item(file, 'value'))):
                    file_path += (' ' + self.item(file, 'value')[i])
                file_name = file_path.rpartition('\\')[2]
                self.output.entry_log((str(file_name) + ' selected!'))
                self.var_file.set(file_path)
            else:
                if self.parent(file) == '':
                    self.output.entry_warn('No File selected!')
                else:
                    if os.path.isdir(self.item(file, 'value')[0]):
                        self.output.entry_warn('No File selected!')
                    else:
                        file_path = self.item(file, 'value')[0]
                        file_name = file_path.rpartition('\\')[2]
                        self.output.entry_log((str(file_name) + ' selected!'))
                        self.var_file.set(file_path)
        else:
            if len(self.item(file, 'value')) > 1:
                file_path = self.item(file, 'value')[0]
                for i in range(1,len(self.item(file, 'value'))):
                    file_path += (' ' + self.item(file, 'value')[i])
                file_name = file_path.rpartition('/')[2]
                self.output.entry_log((str(file_name) + ' selected!'))
                self.var_file.set(file_path)
            else:
                if self.parent(file) == '':
                    self.output.entry_warn('No File selected!')
                else:
                    if os.path.isdir(self.item(file, 'value')[0]):
                        self.output.entry_warn('No File selected!')
                    else:
                        file_path = self.item(file, 'value')[0]
                        file_name = file_path.rpartition('/')[2]
                        self.output.entry_log((str(file_name) + ' selected!'))
                        self.var_file.set(file_path)

    def get_filepath(self):
        """ Returns the filepath to the file, that has been choosen. """
        return self.var_file.get()
    
    def change_harddrive(self, mount):
        """ Change the root directory in the file explorer. """
        
        try:
            self.delete(self.root)
            self.var_drive.set(mount)
            self.root = self.insert('', tk.END, text=mount)
            self.__startup_tree(self.var_drive.get(), self.root, 0)
            self.item(self.root, open=True)
        except:
            raise NotADirectoryError('Directory not found.')