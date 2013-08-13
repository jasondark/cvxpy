from cvxpy import *
from mixed_integer import *
import cvxopt
import unittest

class TestVars(unittest.TestCase):
    """ Unit tests for the variable types. """
    def setUp(self):
        pass

    # Overriden method to handle lists and lower accuracy.
    def assertAlmostEqual(self, a, b):
        try:
            a = list(a)
            b = list(b)
            for i in range(len(a)):
                self.assertAlmostEqual(a[i], b[i])
        except Exception:
            super(TestVars, self).assertAlmostEqual(a,b,places=3)

    # Test boolean variable.
    def test_boolean(self):
        x = Variable(5,4)
        p = Problem(Minimize(sum(1-x) + sum(x)), [x == boolean(5,4)])
        result = p.solve(method="admm")
        self.assertAlmostEqual(result, 20)
        for v in x.value:
            self.assertAlmostEqual(v*(1-v), 0)

    # Test choose variable.
    def test_choose(self):
        x = Variable(5,4)
        p = Problem(Minimize(sum(1-x) + sum(x)), [x == choose(5,4,k=4)])
        result = p.solve(method="admm")
        self.assertAlmostEqual(result, 20)
        for v in x.value:
            self.assertAlmostEqual(v*(1-v), 0)
        self.assertAlmostEqual(sum(x.value), 4)

    # Test card variable.
    def test_card(self):
        x = Variable(5)
        p = Problem(Maximize(sum(x)),
            [x == card(5,k=3), x <= 1, x >= 0])
        result = p.solve(method="admm")
        self.assertAlmostEqual(result, 3)
        for v in x.value:
            self.assertAlmostEqual(v*(1-v), 0)
        self.assertAlmostEqual(sum(x.value), 3)

        #should be equivalent to x == choose
        x = Variable(5,4)
        c = card(5,4,k=4)
        b = boolean(5,4)
        p = Problem(Minimize(sum(1-x) + sum(x)), 
            [x == c, x == b])
        result = p.solve(method="admm")
        self.assertAlmostEqual(result, 20)
        for v in x.value:
            self.assertAlmostEqual(v*(1-v), 0)

    # Test permutation variable.
    def test_permutation(self):
        x = Variable(1,5)
        c = cvxopt.matrix([1,2,3,4,5]).T
        perm = permutation(5)
        p = Problem(Minimize(sum(x)), [x == c*perm])
        result = p.solve(method="admm")
        print perm.value
        print x.value
        self.assertAlmostEqual(result, 15)
        self.assertAlmostEqual(sorted(x.value), c)