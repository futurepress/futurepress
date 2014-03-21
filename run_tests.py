import unittest
from test import suite

def run():
    unittest.TextTestRunner(verbosity=2).run(suite())

if __name__ == '__main__':
    run()