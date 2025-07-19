# print function name and the values of its arguments everytime the function is called

def debugging(func):
    def wrapper(*args, **kwargs):   
        args_value = ", ".join(str(arg) for arg in args)
        kwargs_value = ", ".join(f'{k} = {v}' for k, v in kwargs.items())
        print(f'calling {func.__name__} with args {args_value} and kwargs {kwargs_value}')
        result = func(*args, **kwargs)
        return result
    return wrapper

@debugging
def hello():
    print('hello!!')

@debugging
def greet(name, greeting = 'Namaste'):
    print(f'{greeting}, {name}')
    
hello()
greet('Riya', greeting='Namaste, happy to see you coding :)')