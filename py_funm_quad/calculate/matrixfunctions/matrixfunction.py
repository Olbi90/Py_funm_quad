from abc import ABC, abstractmethod

import numpy as np
from scipy import sparse


class Matrixfunction(ABC):
    """ Matrixfunction is an abstract class, wich gives you a simple evalnodal
    function and a unit vector function. You have to implement a 
    first_approximation and an evaluate_error_function_via_quadrature for
    your own matrixfunction. The return type has to be sparse.csc_array in 
    both functions! 
    """

    @abstractmethod
    def first_approximation(self, beta, H, m):
        return

    @abstractmethod
    def evaluate_error_function_via_quadrature(
            self, H, num_quad, active_nodes, subdiag):
        return
    
    def unit(self, dim, pos):
        """ Creates an unit vector with 1 on pos."""
        e = np.zeros((dim,1))
        e[pos] = 1

        return e
    
    def evalnodal(
            self, x:sparse.csc_array, active_nodes:sparse.csc_array, 
            subdiag:sparse.csc_array):
        """ """
        p = (0*x + np.ones((1,x.get_shape()[0])))
        for i in range(active_nodes.get_shape()[0]):
            for j in range(active_nodes.get_shape()[1]):
                p = (subdiag[[i],[j]] * p)/(x - np.ones((1,x.get_shape()[0]))
                                            *active_nodes[[i],[j]])
        
        return p