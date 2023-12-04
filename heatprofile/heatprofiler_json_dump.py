import json
import time
import functools
import sys
from collections import defaultdict

# Global store for profiling data
profiling_data = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))  # [cumulative_time, call_count, last_time_called]

def profile_line_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def trace_func(frame, event, arg):
            if event == "line":
                line_no = frame.f_lineno
                now = time.time()
                file_line = (func.__code__.co_filename, line_no)
                if file_line in profiling_data[func.__name__]:
                    elapsed = now - profiling_data[func.__name__][file_line][2]
                    profiling_data[func.__name__][file_line][0] += elapsed
                    profiling_data[func.__name__][file_line][1] += 1
                profiling_data[func.__name__][file_line][2] = now
            return trace_func

        sys.settrace(trace_func)
        result = func(*args, **kwargs)
        sys.settrace(None)

        return result

    return wrapper

def save_profiling_data_to_json(filename="profiling_data.json"):
    formatted_data = {}
    for func_name, data in profiling_data.items():
        for (file, line), (cumulative_time, calls, _) in data.items():
            if file not in formatted_data:
                formatted_data[file] = {}
            if func_name not in formatted_data[file]:
                formatted_data[file][func_name] = {}
            formatted_data[file][func_name][line] = {
                "cumulative_time": cumulative_time,
                "calls": calls,
                "time_per_call": cumulative_time / calls if calls else 0
            }
    with open(filename, "w") as f:
        json.dump(formatted_data, f, indent=4)

# Example usage and other parts of the code remain the same.


# Example usage
@profile_line_execution
def test_function():
    a = 1
    for i in range(1000):
        a += i
    print(a)

test_function()

@profile_line_execution
def test_function_2():
    a = 2
    for i in range(1000):
        a += i
    print(a)

test_function_2()

# Call this function at the end of your script or when you want to save the data
save_profiling_data_to_json()
