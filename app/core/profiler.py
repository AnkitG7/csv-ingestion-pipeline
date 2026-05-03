# app/core/profiler.py

import inspect
import time
from functools import wraps


def profile_step(label: str):
    """
    Timing decorator that supports both async and sync callables.
    Always logs execution time.
    """

    def decorator(func):
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    print(f"[PROFILE] {label}={elapsed_ms:.2f}ms")

            return async_wrapper

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000
                print(f"[PROFILE] {label}={elapsed_ms:.2f}ms")

        return sync_wrapper

    return decorator

# # app/core/profiler.py
# import inspect
# import time
# from functools import wraps


# def profile_step(label: str):
#     """
#     Async timing decorator for profiling service-layer functions.
#     """

#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             start = time.perf_counter()
#             result = await func(*args, **kwargs)
#             elapsed_ms = (time.perf_counter() - start) * 1000
#             print(f"[PROFILE] {label}={elapsed_ms:.2f}ms")
#             return result

#         return wrapper

#     return decorator
