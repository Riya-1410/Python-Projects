# implement decorator to handle multiple callings with cache logic set cache values so that function need not to execute again
import time 

def cache(func):
    cache_value = {}
    def wrapper(*args):
        start = time.time()
        if args in cache_value:
            return cache_value[args]
        result = func(*args)
        cache_value[args] = result
        end = time.time()
        print(f'time taken {end-start}')
        return result
    return wrapper

@cache
def long_run(a, b):
    time.sleep(5)
    return a + b

print(long_run(89, 50))
print(long_run(89, 50))
print(long_run(89, 50))
print(long_run(89, 50))
print(long_run(3, 57))