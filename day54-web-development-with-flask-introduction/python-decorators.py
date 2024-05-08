import time
def delay_decorator(func):
  
  # NOTE: we use this wrapper to perform some operations before/after the calling fucntion
  def wrapper_func():
    time.sleep(2)
    func()
    func()
  return wrapper_func

@delay_decorator
def say_hi():
  print("hello")


say_hi()
  
#NOTE
# @delay_decorator
# function_say_hi = delay_decorator(say_hi)
# function_say_hi()
