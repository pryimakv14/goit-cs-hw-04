import os
import threading
import time

def search_words_in_file(filename, words, results):
    with open(filename, "r") as file:
        for line_number, line in enumerate(file, start=1):
            for word in words:
                if word in line:
                    if not results.get(word, False):
                        results[word] = []
                    results[word].append("File {0} : found on line {1}".format(filename, str(line_number)))


def search_words_in_directory(directory, words):
    results = {}
    threads = []

    txt_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".txt")]
    for file in txt_files:
        thread = threading.Thread(target=search_words_in_file, args=(file, words, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


if __name__ == "__main__":
    directory = "fls"
    words = ["Vivamus", "test"]
    start_time = time.time()
    results = search_words_in_directory(directory, words)
    execution_time = time.time() - start_time

    print("Executed for ", execution_time, " ms. Results : ", results)

