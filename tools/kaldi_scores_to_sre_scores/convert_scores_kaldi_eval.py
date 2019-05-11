import argparse
import csv
import copy

parser = argparse.ArgumentParser(description='Convert kaldi output scores to match the SRE format.')
parser.add_argument('--input_arb', metavar='i', type=str,
                    help='path to kaldi score arb file')
parser.add_argument('--input_afv', metavar='j', type=str,
                    help='path to kaldi score avf file')
parser.add_argument('--reference', metavar='r', type=str,
                    help='path to reference sre score file')
parser.add_argument('--output', metavar='o', type=str,
                    help='path to output sre score file')


args = parser.parse_args()


# read kaldi scores
arb_lines = open(args.input_arb).readlines()
arb_lines_parts = [l.split(' ') for l in arb_lines]
for l in arb_lines_parts:
    l[1] += ".sph"
arb_lines = [' '.join(l) for l in arb_lines_parts]
afv_lines = open(args.input_afv).readlines()
afv_lines_parts = [l.split(' ') for l in afv_lines]
for l in afv_lines_parts:
    l[1] += ".flac"
afv_lines = [' '.join(l) for l in afv_lines_parts]

lines = arb_lines + afv_lines

# scores = [l.split(' ')[-1].split('\n')[0] for l in lines]

x = 1
# open files
reference = list(csv.DictReader(open(args.reference, 'r'), delimiter='\t'))
reference_line = reference[0]
dest = open(args.output, 'w')

new_lines = []
for l in lines:
    new_line = copy.copy(reference_line)
    line_parts = l.split(' ')
    new_line['modelid'] = line_parts[0]
    new_line['segmentid'] = line_parts[1]
    new_line['LLR'] = line_parts[2].split('\n')[0]
    new_lines.append(new_line)

# replace scores
# for i, r in enumerate(reference):
#     if i < len(scores):
#         r['LLR'] = scores[i]
# write to output file
fieldnames = ['modelid', 'segmentid', 'side', 'LLR']
writer = csv.DictWriter(dest, fieldnames, delimiter='\t')
writer.writeheader()
for line in new_lines:
    writer.writerow(line)
dest.close()
# --input_arb /Users/navealgarici/Documents/GitHub/SRE18/transfer/kaldi18/sre18/v2/exp/scores/sre16_eval_scores --input_arb /Users/navealgarici/Documents/GitHub/SRE18/transfer/kaldi18/sre18_afv/v2/exp/scores/sre16_eval_scores --reference /Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv --output /Users/navealgarici/Documents/GitHub/SRE18/tools/kaldi_scores_to_sre_scores/sre16_eval_scores_all.tsv
# --input_arb /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_plda_adap/v2/exp/scores/sre16_eval_scores_adapt --input_afv /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_avf/v2/exp/scores/sre16_eval_scores --reference /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv --output /docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/sre16_eval_scores_all_adap.tsv
#         /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_plda_adap/v2/exp/scores/sre16_eval_scores_adapt

# --input_arb /docker_volume/Deployed_projects/SRE18/eval_model_0/sre16_eval_scores --input_afv /docker_volume/Deployed_projects/SRE18/eval_model_0/sre16_eval_scores_afv --reference /docker_volume/Deployed_projects/SRE18/eval_model_1/sre18_eval_scores.tsv --output /docker_volume/Deployed_projects/SRE18/eval_model_0/sre16_eval_scores.tsv
-o
/Users/navealgarici/Documents/GitHub/SRE18/eval_model_1/sre18_eval_scores.tsv
-l
/Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trials.tsv
-r
/Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trial_key.tsv