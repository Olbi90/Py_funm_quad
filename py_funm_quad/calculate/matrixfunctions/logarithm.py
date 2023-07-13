import math

import numpy as np
import scipy as sp
from scipy import sparse

from calculate.matrixfunctions.matrixfunction import Matrixfunction


class Logarithm(Matrixfunction):
    """Matrixfunction log(1+A)/A uses Gauss-Legendre quadrature."""
    
    def first_approximation(self, beta, H, m):
        # f = beta*(V(:,1:m)*(logm(eye(m+ell)+H)*(H\unit(ell+1,m+ell)))))
        h = sparse.csc_array(beta*(sparse.csc_array(
                    sp.linalg.logm(np.eye(m)+H[0:m,0:m])@sp.linalg.solve(
                    H[0:m,0:m].toarray(),super().unit(m,0)))))

        return h

    def evaluate_error_function_via_quadrature(
            self, H:sparse.csc_array, num_quad:int, 
            active_nodes:sparse.csc_array, subdiag:sparse.csc_array): 
        m = H.get_shape()[0]
        
        # Workaround to create Diagonalmatrix T_gauss
        b_gauss = list()
        for i in range(1,num_quad):
            b_gauss.append(0.5/math.sqrt(1-(2*i)**(-2)))
        T_gauss = sparse.csc_array(np.diag(b_gauss, 1) + np.diag(b_gauss,-1))
        
        # Wrong order of the eigenvectors
        D_gauss, V_gauss = sp.linalg.eig(T_gauss.toarray())
        ind = np.argsort(D_gauss)
        D_gauss = np.sort(D_gauss)
        D_gauss = sparse.csc_array(D_gauss)

        weights = list()
        for i in range(len(ind)):
            weights.append(2*V_gauss[0,ind[i]]**2)
        weights = sparse.csc_array(np.array(weights))

        tt = sparse.csc_array(-2/(D_gauss.toarray() + 1))
        rho_vec = super().evalnodal(tt, active_nodes, subdiag)
        rho_vec = rho_vec.transpose()

        # Actual Quadrature
        ee = np.zeros((m,1))
        ee[[0],[0]] = 1
        h = sparse.csc_array(np.zeros((m,1)))
        for j in range(D_gauss.get_shape()[1]):
            h = h + (sp.linalg.solve(((H.toarray()
                                       *(1 + D_gauss[[0],[j]])
                                       +2*np.eye(m))),ee))*(weights[[0],[j]]
                                                            *rho_vec[[j],[0]])

        return sparse.csc_array(h)