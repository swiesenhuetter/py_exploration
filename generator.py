def rotate_call(*args):
    """
    This function executes three function calls in round robin fashion.
    """
    def generator():
        while True:
            for func in args:
                func()
                yield None

    return generator()
    

if __name__ == "__main__":
    def f1():
        print("Function 1 executed")

    def f2():
        print("Function 2 executed")

    def f3():
        print("Function 3 executed")


    gen = rotate_call(f1, f2, f3)
    
    for _ in range(20):
        next(gen)

