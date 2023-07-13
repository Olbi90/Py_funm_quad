from abc import ABC, abstractmethod

from scipy import sparse


class Algorithm(ABC):
    """ Algorithm is an abstract class, wich gives you the arnoldi and
    lanczos Algorithm. You have to implement your own inner product in the
    method inner_product(self, vector_v, vector_w)
    """

    @abstractmethod
    def inner_product(self, vector_v, vector_w):
        """ Here you have to implement your own scalar product."""
        return

    def arnoldi(
            self, A:sparse.csc_array, b:sparse.csc_array, m:int, timekeeper):
        """ A simple arnoldi algorithm with gram-schmidt."""
        # Parameter
        measure_mxA = 0
        measure_scalar = 0

        # Create V to store Basis and H for Hessenberg
        dim_A = A.get_shape()[0]
        V = sparse.csc_array((dim_A,m+1))
        H = sparse.csc_array((m+1,m))
        
        b = b/sparse.linalg.norm(b)

        V[:,[0]] = b
        ### Start loop ###
        for j in range(m):
            timekeeper.start_timer('mult_A')
            w = A@V[:,[j]]
            timekeeper.stop_timer('mult_A')
            measure_mxA += 1

            # Gram Schmidt
            timekeeper.start_timer('scalar')
            for i in range(j+1):
                H[i,j] = self.inner_product(V[:,[i]],w)
                measure_scalar += 1
                w = w - H[i,j]*V[:,[i]]
            timekeeper.stop_timer('scalar')

            H[j+1,j] = sparse.linalg.norm(w)
            if H[j+1,j] == 0:
                break
            V[:,[j+1]] = w/H[j+1,j]
        
        return V,H, measure_mxA, measure_scalar
    
    def lanczos(
            self, A:sparse.csc_array, b:sparse.csc_array, m:int, timekeeper):
        """ A simple lanczos algorithm for hermitian matrices."""
        # Parameter
        measure_mxA = 0
        measure_scalar = 0

        dim_A = A.get_shape()[0]
        V = sparse.csc_array((dim_A,m+1))
        H = sparse.csc_array((m+1,m))

        b = b/sparse.linalg.norm(b)

        V[:,[0]] = b

        ### First initial Step
        #H[1,0] = 0
        timekeeper.start_timer('mult_A')
        w = A@V[:,[0]]
        timekeeper.stop_timer('mult_A')
        measure_mxA += 1
        timekeeper.start_timer('scalar')
        H[0,0] = self.inner_product(V[:,[0]],w)
        timekeeper.stop_timer('scalar')
        measure_scalar += 1
        w = w - H[0,0]*V[:,[0]]
        H[1,0] = sparse.linalg.norm(w)
        H[0,1] = H[1,0]
        V[:,[1]] = w/H[1,0]

        #### Steps 1 to m
        for j in range(1,m):
            timekeeper.start_timer('mult_A')
            w = A@V[:,[j]]-H[j,j-1]*V[:,[j-1]]
            timekeeper.stop_timer('mult_A')
            measure_mxA += 1

            timekeeper.start_timer('scalar')
            H[j,j] = self.inner_product(V[:,[j]],w)
            timekeeper.stop_timer('scalar')
            measure_scalar += 1
            w = w - H[j,j]*V[:,[j]]
            H[j+1,j] = sparse.linalg.norm(w)
            if j < m-1:
                H[j,j+1] = H[j+1,j]
            if H[j+1,j] == 0:
                break
            V[:,[j+1]] = w/H[j+1,j]
        
        return V,H, measure_mxA, measure_scalar