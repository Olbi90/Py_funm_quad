import os
import pathlib
import tkinter.filedialog as tkfile

class CodeCreator:
    """ CodeCreator is used for creating python scripts 
    for your own programm in two versions. One with a path to a file, and
    one with A and b in the call of Solver.
    """

    def __init__(self, save_type, parameter:dict):
        """ Create a python script.
        save_type : wich script type you want to save
            file - for path to file,
            Ab - A and b in call
        parameter : the parameters you used in the GUI
        """
        
        py_file = tkfile.asksaveasfile(initialdir=os.getcwd(),
                                       initialfile='thesis_template',
                                       defaultextension='.py', mode='w',
                                       filetypes=[('Pythonfile','*.py')])
        if py_file is None:
            return
        if pathlib.Path(py_file.name).suffix != '.py':
            raise NameError()
        else:
            py_file.write(
                'from calculate.solver import Solver\n')
            py_file.write('\n')
            py_file.write('your_parameter = {\n')
            parameter_list = list()
            if save_type == 'file':
                for key in parameter.keys():
                    if key == 'output':
                            parameter_list.append("    '" + key + "'" + ' : ' 
                                                  + 'None' + ',' + '\n')
                    else:
                        if (type(parameter[key]) == int or 
                            type(parameter[key]) == float):
                            parameter_list.append("    '" + key + "'" + ' : ' 
                                                  + str(parameter[key]) + ',' 
                                                  + '\n')
                        else:
                            parameter_list.append("    '" + key + "'" + ' : ' 
                                                  + "'" + str(parameter[key]) 
                                                  + "'" + ',' + '\n') 
            elif save_type == 'Ab':
                for key in parameter.keys():
                    if key == 'output' or key == 'file':
                        parameter_list.append("    '" + key + "'" + ' : ' 
                                              + 'None' + ',' + '\n')
                    else:
                        if (type(parameter[key]) == int or
                            type(parameter[key]) == float):
                            parameter_list.append("    '" + key + "'" + ' : ' 
                                                  + str(parameter[key]) + ',' 
                                                  + '\n')
                        else:
                            parameter_list.append("    '" + key + "'" + ' : ' 
                                                  + "'" + str(parameter[key]) 
                                                  + "'" + ',' + '\n')
            else: 
                parameter_list.append('Wrong Input')     
                     
            py_file.writelines(parameter_list)
            py_file.write('}\n\n')
            if save_type == 'file':
                py_file.write('your_solver = Solver(your_parameter)')
            elif save_type == 'Ab':
                py_file.write('your_solver = Solver(your_parameter, A, b)')
            else:
                py_file.write('Something went wrong here!')