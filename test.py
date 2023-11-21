from heatprofiler import *
from insert_after_line_callback import *

@profile_line_execution
def test_function():
    a = 1
    b = 2
    print(a + b)
    for i in range(1000):
        a += i
    print(a)

test_function()