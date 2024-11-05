#!/usr/bin/env python3
# Import necessary modules
import sys
import sysconfig
import math
import time
from threading import Thread
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import pandas as pd
import os
import ast
from tools.crawl import WebScraper 
from tools.preprocessing import preprocessing

#Config
storage_folder_contain_subdomain = "./crawl/company_information_subdomain"
os.makedirs(storage_folder_contain_subdomain, exist_ok=True)

#Data
meta_df = pd.read_csv("./business_meta.csv")
df_bank = pd.DataFrame({"url": ["https://www.vietcombank.com.vn/"],
                        "code": ["123"]})
meta_df = pd.concat([df_bank, meta_df], axis=0)
# meta_df = pd.concat([meta_df, meta_df], axis=0)


#Worker init
Worker = WebScraper(saving_path=storage_folder_contain_subdomain,
                    get_subdomain=True)

# Hàm để crawl URL từ cột list_business
def task(row):
    # print(f"Company: {row['name']}")
    # print(f"Tax Code: {row['code']}")
    tax = row['code']
    url = row['url']

    try:
        Worker.process_url_subdomain(url, tax)
    except Exception as e:
        print(e)

    # print("="*50)

# Define a decorator to measure function execution time
def time_taken(func):
    """
    A decorator to measure the execution time of a function.
    
    Args:
        func: The target function.
    
    Returns:
        A wrapper function that measures and prints the execution time.
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Function {func.__name__!r} took {execution_time:.4f} seconds to execute.")

        return result
    return wrapper


# Define single-threaded task function
@time_taken
def single_threaded_task(meta_df):
    """
    A single-threaded task that performs compute-intensive tasks sequentially.
    
    Args:
        nums: A list of input numbers.
    """
    for i in range(len(meta_df)):
        row = meta_df.iloc[i]
        task(row)

# Define multi-threaded task function
@time_taken
def multi_threaded_task(meta_df):
    """
    A multi-threaded task that creates and runs a thread pool to perform 
    compute-intensive tasks concurrently.
    
    Args:
        nums: A list of input numbers.
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(len(meta_df)):
            row = meta_df.iloc[i]
            executor.submit(task, row)

# Define multi-processing task function
@time_taken
def multi_processing_task(meta_df):
    """
    A multi-processing task that creates and runs a process pool to perform 
    compute-intensive tasks concurrently.
    
    Args:
        nums: A list of input numbers.
    """
    with Pool(processes=5) as pool:
        pool.map(task, [meta_df.iloc[i] for i in range(len(meta_df))])

# Define the main function
def main():
    """
    The main entry point of the program.
    
    It prints the Python version and checks if the GIL is enabled or not.
    Then, it runs single-threaded, multi-threaded, and multi-processing tasks.
    """
    print(f"Python Version: {sys.version}")

    # Check GIL status
    py_version = float(".".join(sys.version.split()[0].split(".")[0:2]))
    status = sysconfig.get_config_var("Py_GIL_DISABLED")

    if py_version >= 3.13:
        status = sys._is_gil_enabled()
    if status is None:
        print("GIL cannot be disabled for Python version <= 3.12")
    if status == 0:
        print("GIL is currently disabled")
    if status == 1:
        print("GIL is currently active")

    # nums = [300001]*100

    # Run single-threaded task
    single_threaded_task(meta_df)

    # Run multi-threaded task
    multi_threaded_task(meta_df)

    # Run multi-processing task
    multi_processing_task(meta_df)


# Call the main function
if __name__ == "__main__":
    main()

