#TASK 1
import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        logger.log(logging.INFO, f"Function {func.__name__} called with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.log(logging.INFO, f"Function {func.__name__} returned {result}")
        return result
    return wrapper

@logger_decorator
def say_hello():
    print(f"Hello, World!")

@logger_decorator
def task_four(*args):
    return True

@logger_decorator
def task_five(**kwargs):
    return logger_decorator

#Calling fns

say_hello()
task_four(1,3,5)
task_five(name="Marina", age = 39)






