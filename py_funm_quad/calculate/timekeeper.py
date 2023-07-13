import time


class Timekeeper():
    """ Timekeeper creates an object, that can measure different 
    time variables during runtime. 
    """

    def __init__(self):
        """ Supported time measurement:
        Complete, multiplication with A, approximation of f, quadrature, 
        arnoldi and inner product.
        """

        self.__start_complete = time.time()
        self.__time_complete = 0
        self.__start_mult_A = 0
        self.__time_mult_A = 0
        self.__start_approx_f = 0
        self.__time_approx_f = 0
        self.__start_quadrature = 0
        self.__time_quadrature = 0
        self.__start_arnoldi = 0
        self.__time_arnoldi = 0
        self.__start_scalar = 0
        self.__time_scalar = 0

    def start_timer(self, measurement):
        """ Starts a timer.
        measurement : mult_A, approx_f, quadrature, arnoldi, scalar
        nesting is supported for different timers. Every start needs a stop
        """
         
        match measurement:
            case 'mult_A':
                self.__start_mult_A = time.time()
            case 'approx_f':
                self.__start_approx_f = time.time()
            case 'quadrature':
                self.__start_quadrature = time.time()
            case 'arnoldi':
                self.__start_arnoldi = time.time()
            case 'scalar':
                self.__start_scalar = time.time()

    def stop_timer(self, measurement):
        """ Stops a timer.
        measurement : mult_A, approx_f, quadrature, arnoldi, scalar
        nesting is supported for different timers. 
        Every start needs a stop.
        """

        match measurement:
            case 'mult_A':
                time_passed = time.time() - self.__start_mult_A
                self.__time_mult_A += time_passed
            case 'approx_f':
                time_passed = time.time() - self.__start_approx_f
                self.__time_approx_f += time_passed
            case 'quadrature':
                time_passed = time.time() - self.__start_quadrature
                self.__time_quadrature += time_passed
            case 'arnoldi':
                time_passed = time.time() - self.__start_arnoldi
                self.__time_arnoldi += time_passed
            case 'scalar':
                time_passed = time.time() - self.__start_scalar
                self.__time_scalar += time_passed
            case 'complete':
                time_passed = time.time() - self.__start_complete
                self.__time_complete = time_passed

    def round_time(self):
        """ Round the values to 4 digits. """
        self.__time_complete = round(self.__time_complete,4)
        self.__time_mult_A = round(self.__time_mult_A,4)
        self.__time_approx_f = round(self.__time_approx_f,4)
        self.__time_quadrature = round(self.__time_quadrature,4)
        self.__time_arnoldi = round(self.__time_arnoldi,4)
        self.__time_scalar = round(self.__time_scalar,4)

    def get_timer(self):
        """ Returns a dictionary with the measurement values. """
        timebook = {
            'Time_complete' : self.__time_complete,
            'Time_arnoldi' : self.__time_arnoldi,
            'Time_mult_A' : self.__time_mult_A,
            'Time_scalar' : self.__time_scalar,
            'Time_quadrature' : self.__time_quadrature,
            'Time_approx_f' : self.__time_approx_f,        
        }

        return timebook