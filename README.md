# Py_funm_quad

Modular implementation of a quadrature-based restart Krylov method for the approximation of f(A)b.
A is a square, large and sparse matrix, b is a vector and f is a function.

When finished py_funm_quad will be based on FUNM_QUAD:
http://www-ai.math.uni-wuppertal.de/SciComp/software/funm_quad.html

In version 1.0 you can approximate the following functions:
- inverse squareroot
- exp
- log(1+A)/A [ where 1 is the identity ]

Conventions:
- At the moment py_funm_quad can read .mat and .npz files. They have to include a matrix named A and a vector 
  named b. A solution named exact is optional.
- To use py_funm_quad in other programs you have to create a .pth file in the directory "site-packages"
  in your python directory. The content of the file has to be the path to the directory of py_funm_quad 
  and its subdirectory.
- The class Solver is the Interface to use py_funm_quad without the GUI [ from calculate.solver import Solver ]
- To import a database it has to be a .csv file but you can export a .csv and .mat file.


Start py_funm_quad with GUI: [ Version 1.0 ] [ may change ]

At the moment you have to be in py_funm_quad directory and start py_funm_quad.py


And without a GUI: [ Version 1.0 ] [ may change ]

The class Solver is the Interface to use py_funm_quad without the GUI [ from calculate.solver import Solver ]
