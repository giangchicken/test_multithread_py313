import pandas as pd
import time
from threading import Thread
from multiprocessing import Process

import pandas as pd
import os
import ast

from tools.crawl import WebScraper 
from tools.preprocessing import preprocessing

#Config
storage_folder = "./crawl/company_information"
os.makedirs(storage_folder, exist_ok=True)

path_data = "./company_1.csv"

storage_folder_contain_subdomain = "./crawl/company_information_subdomain"
os.makedirs(storage_folder_contain_subdomain, exist_ok=True)


# Assuming Worker and time_taken decorator are already defined
# Duplicate Data: Create a sample meta_df with 1000 entries
df_bank = pd.DataFrame({"url": ["https://www.vietcombank.com.vn/"], 
                        "code": ["123"]})
meta_df = pd.read_csv("./business_meta.csv")
# meta_df = pd.concat([df_bank, meta_df], axis=0)


Worker = WebScraper(saving_path=storage_folder_contain_subdomain,
                    get_subdomain=True)

# Function to run task for a single row
def task(row):
    try:
        Worker.process_url_subdomain(row['url'], row['code'])
    except Exception as e:
        print(e)

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

# Sequential Crawling
@time_taken
def sequential_crawl():
    for i in range(len(meta_df)):
        row = meta_df.iloc[i]
        task(row)

# Multi-threaded Crawling
@time_taken
def multi_threaded_crawl():
    threads = []
    for i in range(len(meta_df)):
        row = meta_df.iloc[i]
        thread = Thread(target=task, args=(row,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Multi-processing Crawling
@time_taken
def multi_processing_crawl():
    processes = []
    for i in range(len(meta_df)):
        row = meta_df.iloc[i]
        process = Process(target=task, args=(row,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

# Run each crawl type and compare times
if __name__ == "__main__":
    print("Starting sequential crawl:")
    sequential_crawl()

    print("Starting multi-threaded crawl:")
    multi_threaded_crawl()

    print("Starting multi-processing crawl:")
    multi_processing_crawl()
