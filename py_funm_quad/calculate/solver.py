import os
import sys
import warnings
import pathlib
import tkinter.filedialog as tkfile

import numpy as np
import scipy as sp
import scipy.sparse as sparse
from scipy.io import loadmat, savemat

from calculate.matrixfunctions.invsqrt import Invsqrt
from calculate.matrixfunctions.logarithm import Logarithm
from calculate.matrixfunctions.exp import Exp
from calculate.algorithm.standard import StandardAlgorithm
from calculate.timekeeper import Timekeeper


class Solver:
    """ Solver is the Interface for use in your own program. When used in GUI
    it is used to solve f(A)b with a restart Arnoldi algorithm.
    """

    def __init__(self, parameter:dict, A=None, b=None, exact=None):
        """ Creates a solver object that stores the approximation f(A)b and
        a dictionary of parameters that are tracked while solving.
        parameter : dictionary with your parameters
        If path is not given
        A : sparse.csc_array
        b : sparse.csc_array
        exact : exact solution, optional, sparse.csc_array
        """

        try:
            try:
                A, b, exact_calc = self.__load_components(
                    parameter['file'])
                self.__approx, self.__data = self.__restart_arnoldi(
                    parameter, A, b, exact_calc)
            except NotADirectoryError:
                try:
                    if type(A) == sparse.csc_array and type(b) == sparse.csc_array:
                        if type(exact) == sparse.csc_array:
                            self.exact = exact
                        else:
                            self.exact = None

                        self.__approx, self.__data = self.__restart_arnoldi(
                            parameter, A, b, self.exact)
                    else:
                        raise TypeError()

                except ValueError:
                    raise ValueError()
                except TypeError:
                    raise TypeError()
            except ValueError:
                raise ValueError()
            except TypeError:
                raise TypeError()
            except NotImplementedError:
                raise NotImplementedError()
            except KeyError:
                raise KeyError()
        except KeyError:
            if parameter['output'] != None:
                output = parameter['output']
                output.entry_err(('Wrong structure in file. Canceled!'))
            else:
                print('Error: Wrong structure in file. Canceled!')
        except ValueError:
            if parameter['output'] != None:
                output = parameter['output']
                output.entry_err(('Wrong dictionary. Canceled!'))
            else:
                print('Error: Wrong dictionary. Canceled!')
        except TypeError:
            if parameter['output'] != None:
                output = parameter['output']
                output.entry_err(('A and b must be from type sparse.csc_array. Canceled!'))
            else:
                print('A and b must be from type sparse.csc_array. Canceled!')
        except FileNotFoundError:
            if parameter['output'] != None:
                output = parameter['output']
                output.entry_err(('No components to use. Canceled!'))
            else:
                print('Error: No Components to use. Canceled!')
        except NotImplementedError:
                if parameter['output'] != None:
                    output = parameter['output']
                    output.entry_err(
                        ('Extension / Function still to implements. Canceled!'))
                else:
                    print('Error: Extension / Function still to implement. Canceled!')
               
    def __restart_arnoldi(
            self, parameter:dict, A:sparse.csc_array, b:sparse.csc_array, 
            exact:sparse.csc_array = None):
        """ Simple Restart arnoldi to approximate f(A)b. """
        # Supress Warnings for sparse changing and 0 divide
        warnings.filterwarnings("ignore")
        # initialisation
        try:
            output = parameter['output']
            m = parameter['length']
            restarts = parameter['cycles']
            function = parameter['function']
            stopping_accuracy = parameter['stopping_accuracy']
        except:
            raise ValueError()
        if (type(m) != int 
            or type(restarts) != int or type(stopping_accuracy) != float):
            raise ValueError()
        
        hermitian = sparse.linalg.norm((A-A.getH()))
        measure_mxA = 0
        measure_scalar = 0
        error = sparse.csc_array((1,restarts))
        update = sparse.csc_array((1,restarts))
        beta = sparse.linalg.norm(b)
        timekeeper = Timekeeper()

        arnoldi = StandardAlgorithm()
        # Chosse Function
        fts = self.__get_function(function)
        if type(fts) == int:
            if output != None:
                output.entry_log(('No such function!'))
                raise NotImplementedError()
            else:
                print('No such function!')
                raise NotImplementedError()
        if output != None:
            output.entry_log(('Start ' + function + ' Approximation'))

        #### Start Restart Loop ####
        for k in range(restarts):
            if output != None:
                output.entry_log(('Restart Cycle: ' + str(k+1)))
            # Watch Out Starts at 0
            if k == 0:
                # First Arnoldi
                timekeeper.start_timer('arnoldi')
                if hermitian:
                    V,H, mA, sc = arnoldi.arnoldi(A,b,m, timekeeper)
                    if output != None:
                        output.entry_log(('Start Arnodli'))
                    else:
                        print('Use Arnodli.')
                else:
                    V,H, mA, sc = arnoldi.lanczos(A,b,m, timekeeper)
                    if output != None:
                        output.entry_log(('Start Lanczos'))
                    else:
                        print('Use Lanczos.')
                timekeeper.stop_timer('arnoldi')
                measure_mxA += mA
                measure_scalar += sc
                # Approximation   
                timekeeper.start_timer('approx_f')      
                h = fts.first_approximation(beta, H, m)
                f_approx = sparse.csc_array(V[:,0:m]@h)
                timekeeper.stop_timer('approx_f')

                subdiag = sparse.csc_array(H[0:m+1,0:m].diagonal(-1))
                active_nodes = sparse.csc_array(
                    sp.linalg.eigvals(H[0:m,0:m].toarray()))
            else:
                v = V[:,[m]]
                timekeeper.start_timer('arnoldi')
                if hermitian:
                    V,H, mA, sc = arnoldi.arnoldi(A,v,m, timekeeper)
                else:
                    V,H, mA, sc = arnoldi.lanczos(A,v,m, timekeeper)

                timekeeper.stop_timer('arnoldi')
                measure_mxA += mA
                measure_scalar += sc
                # Error via quadrature
                # fix for test reasons
                num_quad = 100
                timekeeper.start_timer('quadrature')
                h = fts.evaluate_error_function_via_quadrature(
                    H[0:m,0:m], num_quad, active_nodes, subdiag)
                timekeeper.stop_timer('quadrature')
                
                # Approximation
                timekeeper.start_timer('approx_f')
                f_approx = f_approx + sparse.csc_array(beta*(V[:,0:m]@h))
                timekeeper.stop_timer('approx_f')

                subdiag = sparse.vstack(
                    (subdiag,sparse.csc_array(H[0:m+1,0:m].diagonal(-1))))
                active_nodes = sparse.csc_array(sparse.vstack(
                    (active_nodes,
                    sp.linalg.eigvals(H[0:m,0:m].toarray()))))

            update[[0],[k]] = beta*sparse.linalg.norm(h)

            if exact == None:
                error = 'No exact solution given'
            else:
                error[[0],[k]] = sparse.linalg.norm(f_approx-exact)
            
            # Stopping Accuracy Check
            if (update[[0],[k]]/sparse.linalg.norm(f_approx)) < stopping_accuracy:
                restarts = k + 1
                if output != None:
                    output.entry_log('Stopping accuracy reached!')
                else:
                    print('Stopping accuracy reached!')
                break
        
        #### Restart Loop End ####

        timekeeper.stop_timer('complete')
        timekeeper.round_time()
        timebook = timekeeper.get_timer()

        measurement = {
            'Name' : function + '_' + str(A.get_shape()[0]) 
                     + '_' + str(m) + '_' + str(restarts),
            'Function' : function,
            'Dimension' : A.get_shape()[0],
            'Length' : m,
            'Cycles' : restarts,
            'MxA' : measure_mxA,
            'Inner_product' : measure_scalar,  
        }

        if exact == None:
            measurement.update({'Error_end' : 'NaN'})
        else:
            measurement.update(
                {'Error_end' : round(float(error[[0], [restarts-1]]), 4)})
        if output != None:
            output.entry_log('Successful!')
        else:
            print('Successful!')

        measurement.update(timebook)
        if type(error) == str:
            measurement.update({'Eigenvalues' : active_nodes.toarray().tolist(), 
                                'Error_norms' : error})
        else:
            measurement.update({'Eigenvalues' : active_nodes.toarray().tolist(), 
                                'Error_norms' : error.toarray().tolist()})

        return f_approx, measurement
    
    def __load_components(self, path:str):
        """ Load a file into solver via path. 
        Supported filetypes .mat, .npz
        """

        try:
            if path == 'EMPTY' or path == '' or path == None:
                raise NotADirectoryError()
            else:
                try:
                    ext_ind = path.rfind('.')
                    extension = path[ext_ind:]
                    match extension:
                        case '.mat':
                            comp_dict = loadmat(path)
                            A = sparse.csc_array(comp_dict['A'])
                            b = sparse.csc_array(comp_dict['b'])
                            try:
                                exact = sparse.csc_array(comp_dict['exact'])
                            except:
                                exact = None
                        case '.npz':
                            comp_dict = np.load(path, allow_pickle=True)
                            A = sparse.csc_array(comp_dict['A'])
                            b = sparse.csc_array(comp_dict['b'])
                            try:
                                exact = sparse.csc_array(comp_dict['exact'])
                            except:
                                exact = None
                        case _:
                            raise NotImplementedError()
                    
                    return A,b, exact
                except:
                    raise KeyError()
        except NotImplementedError:
            raise NotImplementedError()
        except NotADirectoryError:
            raise NotADirectoryError()
        except KeyError:
            raise KeyError()
        
    def save_approx_to_file(self, path:str=None):
        """ Save an approximation f(A)b to a file. Use path for use without
        graphical userinterface. Supported .mat, .npy, .npz
        """
        if path == None:
            file_typelist = [('Matfile','*.mat'),('Numpy','*.npy'),
                             ('Numpy Compressed','*.npz')]
            save_file = tkfile.asksaveasfile(initialdir= os.getcwd(), 
                                             initialfile='thesis_approx', 
                                             defaultextension='.npy', mode='w',
                                             filetypes=file_typelist)
            data_type = pathlib.Path(save_file.name).suffix
            save_file = pathlib.Path(save_file.name)
            match data_type:
                case '.mat':
                    self.__approx.toarray()
                    savemat(save_file,{'approx' : self.__approx})
                case '.npy':
                    self.__approx.toarray()
                    np.save(save_file, self.__approx)
                case '.npz':
                    sparse.save_npz(save_file, self.__approx)
                case _:
                    raise NotImplementedError('Still to implement.')
        else:
            ext_ind = path.rfind('.')
            data_type = path[ext_ind:]
            match data_type:
                case '.mat':
                    self.__approx.toarray()
                    savemat(path,{'approx' : self.__approx})
                case '.npy':
                    self.__approx.toarray()
                    np.save(path, self.__approx)
                case '.npz':
                    sparse.save_npz(path, self.__approx)
                case _:
                    raise NotImplementedError('Still to implement.')

    def get_measurment(self):
        """ Returns a dictionary with tracked parameters. """
        return self.__data

    def get_error_norms(self):
        """ Returns the error norms. """

        return self.__data['Error_norms']
    
    def get_approx_f(self):
        """ Returns the approximation of f(A)b. """
        return self.__approx
    
    def __get_function(self, function):
        """ Returns an Object of the matrixfunction to solve. 
        If the function is not implemented returns: 0
        """
        
        if function == 'log':
            fts = Logarithm()
        elif function == 'invsqrt':
            fts = Invsqrt()
        elif function == 'exp':
            fts = Exp()
        else:
            fts = 0

        return fts

    @staticmethod
    def create_parameter(path=None) -> dict:
        """ Creates a default dictionary for your program. 
        path : path to file, optional
        """

        if sys.platform == 'win32':
            parameter = {
                'file' : path,
                'function' : 'invsqrt',
                'length' : 5,
                'cycles' : 5,
                'output' : None,
            }
        else:
            parameter = {
            'file' : path,
            'function' : 'invsqrt',
            'length' : 5,
            'cycles' : 5,
            'output' : None,
        }

        return parameter
    
    @staticmethod
    def get_measurement_keys() -> list:
        """ Returns a list with the keys of the parameters 
        that are tracked during solving f(A)b. 
        --> If you implement an own parameter please add him here.
        """

        measurement_keys = list([
            # For Matlab Compability no Spaces in the Header
            'Name','Function','Dimension','Length',
            'Cycles','MxA','Inner_product','Error_end','Time_complete','Time_arnoldi',
            'Time_mult_A', 'Time_scalar',
            'Time_quadrature','Time_approx_f','Eigenvalues',
            'Error_norms'])
        
        return measurement_keys