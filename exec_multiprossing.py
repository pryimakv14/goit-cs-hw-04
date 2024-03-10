import os
from multiprocessing import Manager, Process
import time

def search_words_in_file(filename, words, results):
    with open(filename, "r") as file:
        for line_number, line in enumerate(file, start=1):
            for word in words:
                if word in line:
                    results[word].append("File {0}: found on line {1}".format(filename, str(line_number)))

def search_words_in_directory(directory, words):
    with Manager() as manager:
        keys = {}
        for word in words:
            keys[word] = manager.list([])

        results = manager.dict(keys)
        processes = []

        txt_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".txt")]
        for file in txt_files:
            process = Process(target=search_words_in_file, args=(file, words, results))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        return dict(map(lambda item: (item[0], list(item[1])), results.items()))
    

if __name__ == "__main__":
    directory = "fls"
    words = ["Vivamus", "test"]
    start_time = time.time()
    results = search_words_in_directory(directory, words)
    execution_time = time.time() - start_time
    print("Executed for ", execution_time, " ms. Results : ", results)
