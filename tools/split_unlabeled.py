from bob.io.base import HDF5File as hdf
import os
import numpy as np
import string
import copy

def split_unlabelled():
    min_len = 2000
    root = "/docker_volume/Deployed_projects/SRE18/temp/baseline/extracted/LDC2018E46_2018_NIST_Speaker_Recognition_Evaluation_Development_Set/data/unlabeled"
    target_dir = "/docker_volume/Deployed_projects/SRE18/temp/baseline/extracted/LDC2018E46_2018_NIST_Speaker_Recognition_Evaluation_Development_Set/data/unlabeled_2000"

    all_unlabelled_path = []
    all_unlabelled_name = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            all_unlabelled_path.append(path)
            all_unlabelled_name.append(name)

    try:
        os.makedirs(target_dir)
    except:
        x = 1

    for path, name in zip(all_unlabelled_path, all_unlabelled_name):
        print(name)
        f = hdf(os.path.join(path, name))['/array']
        l = len(f)
        num_split = int(l / min_len)
        for i in range(num_split - 1):
            temp_f = f[i * min_len: (i + 1) * min_len]
            temp_name = name.split('.')[0] + "_" + str(i) + ".hdf5"
            temp_t = hdf(os.path.join(target_dir, name), 'w')
            temp_t['/array'] = temp_f
            temp_t.close()
        temp_f = f[(num_split - 1) * min_len:]
        temp_name = name.split('.')[0] + "_" + str(num_split - 1) + ".hdf5"
        temp_t = hdf(os.path.join(target_dir, name), 'w')
        temp_t['/array'] = temp_f
        temp_t.close()

def split_test():
    root = "/docker_volume/Deployed_projects/SRE18/temp/baseline/extracted/LDC2018E46_2018_NIST_Speaker_Recognition_Evaluation_Development_Set/data/test"
    target_dir = "/docker_volume/Deployed_projects/SRE18/temp/baseline/extracted/LDC2018E46_2018_NIST_Speaker_Recognition_Evaluation_Development_Set/data/test_split"
    # keys = list(string.ascii_lowercase)[:7]
    keys = ['f', 'h1', 'h2', 'q1', 'q2', 'q3', 'q4']
    all_test_path = []
    all_test_name = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            all_test_path.append(path)
            all_test_name.append(name)

    try:
        os.makedirs(target_dir)
    except:
        x = 1

    for path, name in zip(all_test_path, all_test_name):
        print(name)
        f = hdf(os.path.join(path, name))['/array']
        l = len(f)
        quarter = int(l / 4)
        half = int(l / 2)
        slices = [slice(l), slice(0, half), slice(half, l), slice(0, quarter), slice(quarter, 2 * quarter), slice(2 * quarter, 3 * quarter), slice(3 * quarter, l)]
        for k, s in zip(keys, slices):
            temp_f = f[s]
            temp_name = name.split('.')[0] + "_" + k + ".hdf5"
            temp_t = hdf(os.path.join(target_dir, temp_name), 'w')
            temp_t['/array'] = temp_f
            temp_t.close()


def split_list():
    root = "/Users/navealgarici/Documents/GitHub/SRE18/config/database/protocols/e2e_mixer_and_switchboard/test/dev/for_scores.lst"
    target_dir = "/Users/navealgarici/Documents/GitHub/SRE18/config/database/protocols/e2e_mixer_and_switchboard_split/dev/test"

    try:
        os.makedirs(target_dir)
    except:
        x = 1

    keys = ['f', 'h1', 'h2', 'q1', 'q2', 'q3', 'q4']
    lines = open(root).readlines()
    new_list = open(target_dir + "/for_scores.lst", "w")
    length = len(lines)
    for i, l in enumerate(lines):
        org_segments = l.split(" ")
        for k in keys:
            segments = copy.deepcopy(org_segments)
            segments[0] = segments[0] + "_" + k
            segments[0] = segments[0].replace("test", "test_split")
            new_line = " ".join(segments)
            new_list.write(new_line)
        if i % 1000 == 0:
            print(i, "\t line out of ", length)
    new_list.close()
# split_test()
split_list()