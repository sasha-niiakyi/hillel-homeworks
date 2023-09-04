import time
import asyncio

def timer(func):
    if asyncio.iscoroutinefunction(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            print(f'Time: {end_time - start_time}')
            return result
    else:
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f'Time: {end_time - start_time}')
            return result

    return wrapper

# @timer
# def nothing():
#     time.sleep(2)

# async def async_nothing():
#     await asyncio.sleep(2)

# @timer
# async def main():
#     await async_nothing()
#     await async_nothing()

# nothing()
# asyncio.run(main1()) 