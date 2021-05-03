from parse import read_input_file, read_output_file, write_output_file
if __name__ == "__main__":
    test_to_files = {}
    inputs_to_graphs = {}
    sizes = ('small', 'medium', 'large')
    input_dir = "./all_inputs/"
    output_dir = "./best_outputs/"
    for size in sizes:
        for i in range(1, 301):
            test = size + "-" + str(i)
            test_to_files[test] = []
            inputs_to_graphs[test] = read_input_file(input_dir + test + ".in")
    print(read_output_file(inputs_to_graphs['small-42'], './outputs_set_cover/small-42.out'))
    print(read_output_file(inputs_to_graphs['small-42'], './output_depth_5/small-42.out'))

    # ./ outputs_set_cover / small - 19.
    # out
    # wow
    # ./ outputs_set_cover / small - 24.
    # out
    # wow
    # ./ outputs_set_cover / small - 42.
    # out
    # wow
    # ./ outputs_set_cover / small - 48.
    # out
    # wow
    # ./ outputs_set_cover / small - 49.
    # out
    # wow
    # ./ outputs_set_cover / small - 51.
    # out
    # wow
    # ./ outputs_set_cover / small - 53.
    # out
    # wow
    # ./ outputs_set_cover / small - 56.
    # out
    # wow
    # ./ outputs_set_cover / small - 57.
    # out
    # wow
    # ./ outputs_set_cover / small - 60.
    # out
    # wow
    # ./ outputs_set_cover / small - 67.
    # out
    # wow
    # ./ outputs_set_cover / small - 75.
    # out
    # wow
    # ./ outputs_set_cover / small - 85.
    # out
    # wow
    # ./ outputs_set_cover / small - 89.
    # out
    # wow
    # ./ outputs_set_cover / small - 100.
    # out
    # wow
    # ./ outputs_set_cover / small - 103.
    # out
    # wow
    # ./ outputs_set_cover / small - 120.
    # out
    # wow
    # ./ outputs_set_cover / small - 129.
    # out
    # wow
    # ./ outputs_set_cover / small - 133.
    # out
    # wow
    # ./ outputs_set_cover / small - 139.
    # out
    # wow
    # ./ outputs_set_cover / small - 146.
    # out
    # wow
    # ./ outputs_set_cover / small - 147.
    # out
    # wow
    # ./ outputs_set_cover / small - 151.
    # out
    # wow
    # ./ outputs_set_cover / small - 161.
    # out
    # wow
    # ./ outputs_set_cover / small - 168.
    # out
    # wow
    # ./ outputs_set_cover / small - 174.
    # out
    # wow
    # ./ outputs_set_cover / small - 190.
    # out
    # wow
    # ./ outputs_set_cover / small - 195.
    # out
    # wow
    # ./ outputs_set_cover / small - 196.
    # out
    # wow
    # ./ outputs_set_cover / small - 198.
    # out
    # wow
    # ./ outputs_set_cover / small - 209.
    # out
    # wow
    # ./ outputs_set_cover / small - 210.
    # out
    # wow
    # ./ outputs_set_cover / small - 211.
    # out
    # wow
    # ./ outputs_set_cover / small - 212.
    # out
    # wow
    # ./ outputs_set_cover / small - 213.
    # out
    # wow
    # ./ outputs_set_cover / small - 215.
    # out
    # wow
    # ./ outputs_set_cover / small - 221.
    # out
    # wow
    # ./ outputs_set_cover / small - 224.
    # out
    # wow
    # ./ outputs_set_cover / small - 227.
    # out
    # wow
    # ./ outputs_set_cover / small - 235.
    # out
    # wow
    # ./ outputs_set_cover / small - 246.
    # out
    # wow
    # ./ outputs_set_cover / small - 263.
    # out
    # wow
