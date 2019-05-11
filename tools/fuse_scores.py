import  numpy as np
# import tools.scoring_software.sre18_submission_scorer as scorer
import tools.scoring_software.scoring_utils as st
import tools.score_prep as prep

def score_me(system_output_file, trial_key_file,
             configuration, partitions, sub_partition):
    trial_key = st.read_tsv_file(trial_key_file)
    sys_out = st.read_tsv_file(system_output_file)
    scores = sys_out['LLR']
    tar_nontar_labs = st.compute_numeric_labels(trial_key)
    results = {}
    for ds, p_target in configuration.items():
        dataset_mask = trial_key['data_source'] == ds
        ds_trial_key = trial_key[dataset_mask]
        ds_scores = scores[dataset_mask]
        ds_trial_labs = tar_nontar_labs[dataset_mask]
        if ds == 'cmn2':
            partition_masks = st.compute_partition_masks(ds_trial_key,
                                                         partitions,
                                                         sub_partition)
        else:
            partition_masks = [dataset_mask[dataset_mask]]
        act_c = st.compute_equalized_act_cost(ds_scores, partition_masks,
                                              ds_trial_labs, p_target)
        eer, min_c = st.compute_equalized_min_cost(ds_scores,
                                                   partition_masks,
                                                   ds_trial_labs, p_target)
        results[ds] = [eer, min_c, act_c]
    return results


path = "/Users/navealgarici/Documents/GitHub/SRE18/temp/nist18_split_test/scores/plda_old/ztnorm/scores-dev"
target_path = "/Users/navealgarici/Documents/GitHub/SRE18/temp/nist18_split_test/scores/plda_old/ztnorm/scores-dev-fused"
lines = open(path).readlines()
# trials = [l.split("_sre18")[0].split('/')[-1] for l in lines]
# trial_names = list(set(trials))
# trial_names.sort()
# sorted_trials = dict()
# for g in trial_names:
#     sorted_trials[g] = []
num_trials = int(len(lines) / 7)
trial_scores = [[] for i in range(num_trials)]
for i, l in enumerate(lines):
    trial_scores[int(i / 7)].append(float(l.split(" ")[-1].split('\n')[0]))

# trial_scores = [np.array(t) for t in trial_scores]
trial_scores = np.array(trial_scores)
# groups = [l.split("_sre18")[1].split(' ')[0].split('_')[-1] for l in lines]
# group_names = list(set(groups))
# group_names.sort()
# sorted_groups = dict()
# for g in group_names:
#     sorted_groups[g] = []
# for l, g in zip(lines, groups):
#     sorted_groups[g].append(float(l.split(" ")[-1].split('\n')[0]))

# weights = np.array([1/7] * 7)
# weights = np.array([4,2,2,1,1,1,1]) / 12
# weights = np.array([1, 0,0,0,0,0,0])

num_exp = 100
weights_for_weigts = np.array([30,2,2,1,1,1,1]) / 12
weights_list = np.random.uniform(size=[num_exp, 7])
weights_list = weights_list * weights_for_weigts
weights_list = weights_list / np.expand_dims(np.sum(weights_list, 1), 1)
# weights_list = [np.array([1,0,0,0,0,0,0]),
#                 np.array([0,1,0,0,0,0,0]),
#                 np.array([0,0,1,0,0,0,0]),
#                 np.array([0,0,0,1,0,0,0]),
#                 np.array([0,0,0,0,1,0,0]),
#                 np.array([0,0,0,0,0,1,0]),
#                 np.array([0,0,0,0,0,0,1]),
#                 ]

min_eer = 1000
min_actc = 1000
for weights in weights_list:
    test_scores = np.sum(trial_scores * weights, 1)
    test_lines = []
    for i in range(num_trials):
        split_line = lines[i * 7].split(" ")
        split_line[-1] = str(test_scores[i]) + "\n"
        split_line[-2] = "_".join(split_line[-2].split("_")[:-1])
        l = " ".join(split_line)
        test_lines.append(l)

    target = open(target_path, 'w')
    target.writelines(test_lines)
    target.close()
    prep.convert_scores(target_path, "/Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv")

    configuration = {'cmn2': [0.01, 0.005] }#  , 'vast': [0.05]}
    partitions = {'num_enroll_segs': ['1', '3'],
                  'phone_num_match': ['Y', 'N'],
                  'gender': ['male', 'female'],
                  'source_type': ['pstn', 'voip']}
    results = score_me('/Users/navealgarici/Documents/GitHub/SRE18/temp/nist18_split_test/scores/plda_old/ztnorm/scores-dev-fused-out.tsv', '/Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trial_key.tsv', configuration, partitions, sub_partition=None)
    cprimary, cnt = 0., 0.
    for ds, res in results.items():
        eer, minc, actc = res
        cprimary += actc
        cnt += 1
        if eer < min_eer or actc < min_actc:
            print('EER: {:05.2f}\tmin_C: {:.3f}\tact_C: {:.3f}\t{} ****improvement****'.format(eer * 100,
                                                                           minc, actc, weights))
            min_eer = min(eer, min_eer)
            min_actc = min(actc, min_actc)
        # print('{}\t{:05.2f}\t{:.3f}\t{:.3f}'.format(ds.upper(), eer*100,
        #       minc, actc))
        else:
            print('EER: {:05.2f}\tmin_C: {:.3f}\tact_C: {:.3f}\t{}'.format(eer * 100,
                                                    minc, actc, weights))
# "/docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output"

# python scoring_software/sre18_submission_scorer.py -o /Users/navealgarici/Documents/GitHub/SRE18/temp/nist18_baseline_e2e_all_swb_ubm_mix_and_swb_ivector/scores/plda/ztnorm/scores-dev-out.tsv -l /Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trials.tsv -r /Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trial_key.tsv