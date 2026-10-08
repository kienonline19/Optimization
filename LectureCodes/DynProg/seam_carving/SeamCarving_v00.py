import numpy as np

## Some test cases

img_test = np.array([
    [1.0, 2.0, 1.0, 1.0],
    [2.0, 0.0, 0.0, 3.0],
    [1.0, 1.0, 2.0, 0.0],
    [2.0, 2.0, 0.5, 1.0],
    [2.0, 1.0, 1.0, 0.0]
    ])

g_test = np.array([
    [1.0, 1.0 , 0.5,  0.0],
    [2.0, 1.0 , 1.5,  3.0],
    [0.0, 0.5 , 1.5,  2.0],
    [0.0, 0.75, 1.0,  0.5],
    [1.0, 0.5 , 0.5,  1.0]
    ])

seam_test = np.array([2, 1, 0, 0, 1])

img_reduced_test = np.array([
    [1.0, 2.0, 1.0],
    [2.0, 0.0, 3.0],
    [1.0, 2.0, 0.0],
    [2.0, 0.5, 1.0],
    [2.0, 1.0, 0.0]
    ])

#########################
### Gradient function ###
#########################

def xgrad(img):
    if not isinstance(img, np.ndarray) or img.ndim != 2:
        raise Exception("input must be a 2-d array")
    n, m = img.shape
    if m < 2:
        raise Exception("input width must be at least 2")
    
    # TODO
    g = np.zeros((n, m))
    
    return g

## Test for the xgrad function
def test_xgrad(img = img_test, exp_g = g_test):
    g = xgrad(img)
    assert np.array_equal(g, exp_g)
    print("xgrad ok")

## This runs the gradient tests
# test_xgrad()


######################
### Carve function ###
######################

def carve(img, seam):
    if not isinstance(img, np.ndarray) or img.ndim != 2:
        raise Exception("img input must be a 2-d array")
    if not isinstance(seam, np.ndarray) or seam.ndim != 1:
        raise Exception("seam input must be a 1-d array")
    n, m = img.shape

    if len(seam) != n:
        raise Exception("seam length must match img rows")
        
    pass

## Test for the carve function
def test_carve(img = img_test, seam = seam_test, exp_img_reduced = img_reduced_test):
    img_reduced = carve(img, seam)
    assert np.array_equal(img_reduced, exp_img_reduced)
    print("carve ok")

## This runs the carve test
# test_carve()


######################
### Find best seam ###
######################

## The dynamic programming function that computes the best seam
def get_seam(g):
    # should return the optimal seam as an array of column indices,
    # with the same length as the number of rows in the image
    pass

## Test for the get_seam function
def test_get_seam(g = g_test, exp_seam = seam_test):
    seam = get_seam(g)
    assert np.array_equal(seam, exp_seam)
    print("get_seam ok")

## This runs the seam test
# test_get_seam()


###################
### Seamn Carve ###
###################

## putting all of it together
def seam_carve(img):
    g = xgrad(img)
    seam = get_seam(g)
    img_reduced = carve(img, seam)
    return img_reduced

## Test the seam carve function
def test_seam_carve(img = img_test, exp_img_reduced = img_reduced_test):
    img_reduced = seam_carve(img)
    assert np.array_equal(img_reduced, exp_img_reduced)
    print("seam_carve ok")

## This runs the seam_carve test
# test_seam_carve()
