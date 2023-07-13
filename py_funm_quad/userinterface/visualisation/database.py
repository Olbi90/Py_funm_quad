import os
import pathlib
import tkinter.filedialog as tkfile

import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import savemat


class Database(pd.DataFrame):
    """ Database is neccessary to store information about the different 
    solvings of f(A)b.
    """

    def __init__(self, parameter:list, dataframe = None):
        """ Creates an empty Dataframe with given columns.
        Or creates one with given data.
        parameter : columns
        dataframe : dataframe
        """

        # Create the columns
        if dataframe is None:
            pd.DataFrame.__init__(self, columns=parameter)
        else:
            pd.DataFrame.__init__(self, data=dataframe)

    def append_datarow(self,row_values:dict):
        """ Append a new row to Database. """

        self.loc[len(self)] = row_values.values()

    def return_datarow(self,index):
        """ Returns row with given index. """

        ind = list([index])
        value_list = self.iloc[index,:]
        return ind + value_list.values.tolist()
    
    def return_datarow_window(self,index):
            """ Returns a row without the error_norms and eigenvalues lists. 
            Used for better readability in Databasewindow. 
            """

            ind = list([index])
            value_list = self.iloc[index,:]
            for i in range(len(value_list)-2):
                ind.append(value_list[i])
            return ind

    def save_to_file(self):
        """ Saves Database into a file. 
        Supported .csv, .mat
        """

        file_typelist = [('Csvfile','*.csv'), ('Matfile','*.mat')]
        save_file = tkfile.asksaveasfile(initialdir=os.getcwd(),
                                         initialfile='thesis_database', 
                                         defaultextension='.csv', mode='w', 
                                         filetypes=file_typelist)
        if save_file is None:
            return
        extension = pathlib.Path(save_file.name).suffix
        match (extension):
            case '.csv':
                self.to_csv(save_file)
            case '.mat':
                dict_db = self.to_dict('list')
                savemat(save_file.name, dict_db)
            case _:
                raise NotImplementedError()

    def import_database(self):
        """ Import a Database. 
        Supported .csv
        """
        
        file_typelist = [('Csvfile','*.csv')]#,('Json','*.json')]
        import_file = tkfile.askopenfile(initialdir=os.getcwd(), 
                                         defaultextension='.csv', mode='r', 
                                         filetypes=file_typelist)
        if import_file is None:
            return
        extension = pathlib.Path(import_file.name).suffix
        match (extension):
            case '.csv':
                temp = pd.read_csv(import_file, index_col=0)
            case _:
                raise NotImplementedError()
        
        return temp
