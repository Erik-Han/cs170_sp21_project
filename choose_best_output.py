import os
from shutil import copyfile
from parse import read_input_file, read_output_file, write_output_file
if __name__ == "__main__":
    test_to_files = {}
    inputs_to_graphs = {}
    sizes = ('small', 'medium', 'large')
    input_dir = "./all_inputs/"
    output_dir = "./best_outputs/"
    for size in sizes:
        for i in range(1,301):
            test = size+"-"+str(i)
            test_to_files[test] = []
            inputs_to_graphs[test] = read_input_file(input_dir+test+".in")
    for root, dirs, files in os.walk("./"):
        for file in files:
            filepath = root+os.sep+file
            if filepath.endswith(".out"):
                test = file.split(".")[0]
                print(filepath,test)
                test_to_files[test].append((filepath, read_output_file(inputs_to_graphs[test], filepath)))

    for test in test_to_files:
        best_output = max(test_to_files[test], key = lambda item: item[1])
        copyfile(best_output[0], output_dir+test+".out")
