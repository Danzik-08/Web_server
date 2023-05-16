from multiprocessing import Value, cpu_count
import os

cpu_cores = int(os.getenv('NUMBER_OF_CPU'))
cpu_cores_available = cpu_count()
print(type(cpu_cores_available))

if cpu_cores <= cpu_cores_available - 1:
    process_nums = Value('i', cpu_cores)  # оставляем один процессор под сервер
else:
    process_nums = Value('i', cpu_cores_available - 1)
