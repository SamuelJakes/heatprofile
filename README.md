
# HeatProfile

`HeatProfile` is a Python decorator for profiling the execution time of individual lines within a function. It provides a detailed overview of the function's performance by highlighting each line's cumulative execution time, call count, and average time per call. Additionally, it uses color coding to visually represent the relative time spent on each line, making it easy to spot performance bottlenecks.

## Features

- **Line-by-Line Profiling**: Detailed execution time analysis for each line within the function.
- **Color-Coded Output**: Visual representation using colors to indicate lines with higher execution times.
- **Threshold-Based Coloring**: Lines with execution times significantly lower than the maximum are displayed with a white background, ensuring clarity in highlighting performance-critical areas.
- **Dynamic Column Widths**: Adjusts column widths based on the length of the source code lines, ensuring readability.

## Example Output
![image info](https://github.com/SamuelJakes/heatprofile/blob/main/images/example_output.png)
## Installation

To use `HeatProfile`, simply copy the `heatprofile.py` file to your project directory.

## Usage

To profile a function, import `heatprofile` from `heatprofile.py` and use it as a decorator:

```python
from heatprofile import heatprofile

@heatprofile
def your_function(args):
    # function implementation
    pass
```

Run your Python script as usual, and the profiling output will be displayed in the console.

## Output Format

- **Function Name**: Name of the profiled function.
- **Function Location**: File location of the function.
- **Total Function Time**: Total execution time of the function.
- **Line**: Line number in the source code.
- **Source Code**: The actual source code of the line.
- **Cumulative Time(s)**: Total time spent on this line across all calls.
- **Call Count**: Number of times this line was executed.
- **Time/Call(s)**: Average execution time per call for this line.

## Color Coding

- **Red**: Lines with higher relative execution times.
- **White**: Lines with negligible execution times compared to the maximum.

## Compatibility

`HeatProfile` is compatible with Python 3.x. It has been tested on various platforms with standard Python interpreters.

## Contributing

Contributions to `HeatProfile` are welcome. Please feel free to submit pull requests, report bugs, or suggest features through the GitHub issue tracker.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
