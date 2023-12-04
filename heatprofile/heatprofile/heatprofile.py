import time
import functools
import sys
import inspect
from collections import defaultdict
import psutil
import os

# TODO
# - Add support for profiling multiple functions at once
# - Add support for profiling multiple files at once
# - Add support for saving the profiling data to a file
# - Add support for opening the profiling data in a browser
# - Add support for specifying the call depth to profile

def get_current_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


def heatprofile(func=None, color_focus="time"):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timings = defaultdict(lambda: [0, 0, 0])  # [cumulative_time, call_count, memory_usage]
            
            last_line_no = None
            last_time_started = time.time()
            last_memory_usage = get_current_memory_usage()

            call_depth = [0]  # Track the call depth

            def trace_func(frame, event, arg):
                nonlocal last_line_no, last_time_started, last_memory_usage
                if event == "call":
                    call_depth[0] += 1
                elif event == "return":
                    call_depth[0] -= 1

                if event == "line" and call_depth[0] == 1:
                    line_no = frame.f_lineno
                    now = time.time()
                    current_memory = get_current_memory_usage()
                    # Update timings for the last executed line
                    if last_line_no is not None:

                        elapsed = now - last_time_started
                        memory_increase = current_memory - last_memory_usage
                        timings[last_line_no][0] += elapsed  # Update cumulative time
                        timings[last_line_no][1] += 1        # Increment call count
                        timings[last_line_no][2] += memory_increase  # Update memory usage

                    # Record the start time for the current line
                    last_time_started = now
                    last_memory_usage = current_memory
                    last_line_no = line_no

                return trace_func
            
            sys.settrace(trace_func)
            result = func(*args, **kwargs)
            sys.settrace(None)

            now = time.time()
            current_memory = get_current_memory_usage() 
            if last_line_no is not None:
                elapsed = now - last_time_started
                memory_increase = current_memory - last_memory_usage
                timings[last_line_no][0] += elapsed  # Update cumulative time
                timings[last_line_no][1] += 1        # Increment call count
                timings[last_line_no][2] += memory_increase  # Update memory usage

            # Find the maximum time spent on a single line
            total_time = sum(timing[0] for timing in timings.values())
            max_line_time = max(timing[0] for timing in timings.values()) if timings else 0
            max_memory_usage = max(timing[2] for timing in timings.values()) if timings else 0
            file_name = func.__code__.co_filename
            source_lines = inspect.getsourcelines(func)[0]

            # Calculate the maximum line length
            max_line_length = max(len(line.rstrip()) for line in source_lines)
            source_code_column_width = max(max_line_length, 60)

            print('\n')
            print("-" * 120)
            print("Function name: ", func.__name__)
            print("Function location: ", file_name + ":" + str(func.__code__.co_firstlineno + 1))
            print(f"Total function time: {total_time:.2f}s")
            print("-" * 120)

            header_format = "{:<4} {:<" + str(source_code_column_width) + "} {:>20} {:>15} {:>15} {:>18}"
            print(header_format.format("Line", "Source Code", "Cumulative Time(s)", "Call Count", "Time/Call(s)", "Mem Usage(MB)"))
            print("-" * 120)

            for i, line in enumerate(source_lines, start=func.__code__.co_firstlineno):
                # Escape '{' and '}' in the source line
                escaped_line = line.rstrip().replace("{", "{{").replace("}", "}}")

                time_data = timings.get(i, [0, 0, 0])
                cumulative_time, call_count, mem_usage = time_data
                time_per_call = cumulative_time / call_count if call_count else 0

                # Determine the color intensity based on the maximum line time
                if max_line_time > 0:
                    if color_focus == "time":
                        relative_intensity = cumulative_time / max_line_time
                    elif color_focus == "memory":
                        relative_intensity = mem_usage / max_memory_usage
                    # Define a threshold for starting the red color
                    threshold = 0.05  # Adjust this value as needed
                    if relative_intensity > threshold:
                        scaled_intensity = (relative_intensity - threshold) / (1 - threshold)
                        green_blue_intensity = int(155 * (1 - scaled_intensity))
                    else:
                        green_blue_intensity = 255
                else:
                    green_blue_intensity = 255  # Default value when max_line_time is 0

                if call_count == 0:
                    color_code = "\033[48;2;169;169;169m\033[30m" 
                else:
                    color_code = f"\033[48;2;255;{green_blue_intensity};{green_blue_intensity}m"
                line_format = f"{color_code}{i:4} {escaped_line:<{source_code_column_width}} {cumulative_time:20.6f} {call_count:15} {time_per_call:15.6f} {mem_usage:15.2f} MB\033[0m"
                print(line_format)

            print("-" * 120)
            print('\n')

            return result

        return wrapper
    
    if func is None:
        return decorator
    else:
        return decorator(func)

