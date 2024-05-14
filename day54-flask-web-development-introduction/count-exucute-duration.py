
import time

current_time = time.time()

def count_time(func):
  def wrapper_func():
    start_time = time.time()
    func()
    end_time = time.time()
    # print(end_time - start_time)
    return end_time - start_time
  return wrapper_func

@count_time
def fast_function():
  for i in range(10000000):
    i*i

@count_time
def slow_function():
  for i in range(100000000):
    i*i
  
total_time = float(fast_function()) + float(slow_function())
print(total_time)