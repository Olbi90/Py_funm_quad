import numpy as np
import scipy as sp
from scipy import sparse

from calculate.matrixfunctions.matrixfunction import Matrixfunction


class Exp(Matrixfunction):
    """Matrixfunction exp(A) uses midpoint rule on parabolic
    Hankel contour for quadrature.
    """
    def first_approximation(self, beta, H, m):
        # f = beta*(V(:,1:m)*expm(H)*unit(ell+1,m+ell)
        h = sparse.csc_array(beta*(sp.linalg.expm((H[0:m,0:m]).toarray())
                    @super().unit(m,0)))

        return h

    def evaluate_error_function_via_quadrature(
            self, H:sparse.csc_array, num_quad:int, 
            active_nodes:sparse.csc_array, subdiag:sparse.csc_array):
        tol = 1e-13
        m = H.get_shape()[0]

        # Use midpoint rule on parabolic Hankel contour
        aa = np.maximum(1,((np.real(active_nodes.max()))+1))
        bb = 1
        thetas = np.imag(active_nodes)
        thetas.reshape(active_nodes.get_shape())
        ccs = np.absolute((np.subtract(active_nodes.toarray(),aa) 
                           - 1j*thetas)/thetas.power(2).toarray())
        cc = np.min(ccs)/5
        cc = np.minimum(cc,0.25)

        def phi(theta):
            phi = np.array((np.add(aa, 1j*bb*theta) - cc*theta**2))
            
            return phi
        
        # critical theta
        thetac = np.sqrt((aa-np.log(tol))/cc)
        theta = np.linspace(-thetac,thetac,num_quad)
        hh = theta[1]-theta[0]
        z = phi(theta)
        c = -hh/(2j*np.pi)*np.exp(z)*(np.subtract(1j*bb,2*cc*theta))
        tt = list()
        count = int(num_quad/2)
        for i in range(count):
            tt.append(z[i])
        tt = sparse.csc_array(np.array(tt))
        rho_vec = super().evalnodal(tt, active_nodes, subdiag)
        rho_vec.transpose()
        ee = np.eye(m,1)
        h = np.zeros((m,1))
        
        # Workaround
        c2 = list()
        for i in range(count):
            c2.append(c[i])
        c = np.array(c2)
        rho_vec.transpose()
        c = np.multiply(c,rho_vec)

        for j in range(count):
            h = h - (sp.linalg.solve((z[j]*np.eye(m)-H),ee))*c[:,j]
        
        h = 2*np.real(h)
        
        return sparse.csc_array(h)