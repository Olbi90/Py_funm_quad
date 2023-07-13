import numpy as np
import scipy as sp
from scipy import sparse

from calculate.matrixfunctions.matrixfunction import Matrixfunction


class Invsqrt(Matrixfunction):
    """ Matrixfunction inverse squareroot uses Gauss-Jacobi quadrature."""

    def first_approximation(self, beta, H, m):
        # f = beta*(V(:,1:m)*(sqrtm(H(1:m,1:m))\(V(:,1:m)'*b)))
        h = sparse.csc_array(beta*(sparse.csc_array(
                    sp.linalg.solve(sp.linalg.sqrtm(H[0:m,0:m].toarray()),
                    super().unit(m,0)))))

        return h

    def evaluate_error_function_via_quadrature(
            self, H:sparse.csc_array, num_quad:int, 
            active_nodes:sparse.csc_array, subdiag:sparse.csc_array): 
        m = H.get_shape()[0]

        # Workaround for weights
        weights = list()
        for i in range(1,num_quad+1):
            weights.append(np.pi/num_quad)
        weights = sparse.csc_array(np.array(weights))
        
        # Workaround for t
        t = list()
        for i in range(1,num_quad+1):
            t.append(np.cos(((2*i-1)/(2*(num_quad)))*np.pi))
        t = sparse.csc_array(np.array(t))
        
        # Fixed for testing reason
        beta_transform = 1
        tt = sparse.csc_array(-beta_transform
                              *(np.ones((1,num_quad))-t.toarray())
                              /(np.ones((1,num_quad))+t.toarray()))
        rho_vec = super().evalnodal(tt, active_nodes, subdiag)
        rho_vec = rho_vec.transpose()

        # Actual Quadrature
        ee = np.zeros((m,1))
        ee[[0],[0]] = 1
        h = sparse.csc_array(np.zeros((m,1)))

        for j in range(t.get_shape()[1]):
            h = h + (sp.linalg.solve((-beta_transform*(1-t[[0],[j]])
                                      *np.eye(m)-(H.toarray()*(1+t[[0],[j]]))),
                                      ee))*(weights[[0],[j]]*rho_vec[[j],[0]])
        
        h = (-2*np.sqrt(beta_transform)/np.pi)*h
    
        return sparse.csc_array(h)