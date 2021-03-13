import numpy as np
from typing import List


def solve_lin(matrix_u,vector_d):
    """
    Solve matrix_u*hom=vector_d to find hom
    
    matrix_u = 
        |x0 y0 1  0  0  0  0  0  0  0  0  0|
        |0  0  0  x0 y0 1  0  0  0  0  0  0|
        |              ...                 |
        |0  0  0  x3 y3 1  0  0  0  0 y'3 0|
        |0  0  0  0  0  0  x3 y3 1  0  0  1|
    """
    m_np = np.array(matrix_u)
    v_np = np.array(vector_d)
    return np.linalg.solve(m_np, v_np)


def find_h_inv(picture_pixels, decal_pixels):
    """
    Calculates the inverse of Homography matrix by building and solving
    the linear system of 12x12.
    
    matrix_u*hom = vector_d

        Parameters:
            image_pixel (list): list of 4 points describing the border 
                of the original picture
            decal_pixel (list): list of 4 points describing the border 
                of the decal
        Returns:
            h_inv (np.array): the 3x3 matrix representing 
                the inverse of homography
    """
    # Transform the points into RP2 points
    p_pixels = [[x,y,1] for (x,y) in picture_pixels]
    d_pixels = [[x,y,1] for (x,y) in decal_pixels]

    # Build the right side of linear system
    vector_d = p_pixels[0]+[0]*9
    # Build 12x12 matrix
    aux_list = [[0,0,0]]+p_pixels[1:]
    matrix_u = []
    for idx, pixel in enumerate(d_pixels):
        for i in range(3):
            # coefficients for lambdas to complete each row 
            lambdas = [0,0,0]
            lambdas[i] = -aux_list[idx][i]
            # Build each row by adding 0's and the lambdas coefficients
            matrix_u.append([0]*(i*3)+pixel+[0]*(6-i*3)+lambdas)
    # Solve the linear system
    sol = solve_lin(matrix_u, vector_d)
    # The Homography is built with the first 9 elements
    # of the solution, the remaining 3 are the lambdas
    hom = [sol[i*3:(i+1)*3] for i in range(3)]
    h_inv = np.linalg.inv(hom)
    print(np.dot(hom, [499,499,1]))
    return h_inv


def find_decal_point(h_inv, p, limit):
    # Transpose the vector
    vec = [[p[0]],[p[1]],[1]]
    # Multiply matrix by vector
    d_vec = np.dot(h_inv, vec)
    # Bound point to decal limit (for error correction)
    x = min(max(d_vec[0][0], 0),limit[0])
    y = min(max(d_vec[1][0], 0),limit[1])
    return (int(x),int(y))
