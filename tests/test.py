from heatprofile import heatprofile

@heatprofile
def test_func():
    a = 1
    b = 2
    c = 3
    large_string = " " * (10 * 1024 * 1024) # 10 MB line

    for _ in range(2):
        a += 1
        time.sleep(0.1)

    time.sleep(0.1)
    for _ in range(100):
        a += 1
        b += 2
        c += 3
    if a > 100:
        print('a is greater than 100')
    print(a, b, c)
    print(a, b, c)
    time.sleep(0.1)

test_func()