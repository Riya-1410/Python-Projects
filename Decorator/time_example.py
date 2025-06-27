# Write a decorator which measures the time a function takes to execute itself
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} ran in {end-start} time")
        return result
    return wrapper

@timer
def example_function(t):
    time.sleep(t)

example_function(2)