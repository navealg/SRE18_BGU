import argparse
import csv

parser = argparse.ArgumentParser(description='Convert kaldi output scores to match the SRE format.')
parser.add_argument('--input_arb', metavar='i', type=str,
                    help='path to kaldi score arb file')
parser.add_argument('--input_afv', metavar='i', type=str,
                    help='path to kaldi score avf file')
parser.add_argument('--reference', metavar='r', type=str,
                    help='path to reference sre score file')
parser.add_argument('--output', metavar='o', type=str,
                    help='path to output sre score file')


args = parser.parse_args()


# read kaldi scores
lines = open(args.input_arb).readlines()
lines += open(args.input_afv).readlines()

scores = [l.split(' ')[-1].split('\n')[0] for l in lines]

x = 1
# open files
reference = list(csv.DictReader(open(args.reference, 'r'), delimiter='\t'))
dest = open(args.output, 'w')
# replace scores
for i, r in enumerate(reference):
    if i < len(scores):
        r['LLR'] = scores[i]
# write to output file
fieldnames = ['modelid', 'segmentid', 'side', 'LLR']
writer = csv.DictWriter(dest, fieldnames, delimiter='\t')
writer.writeheader()
for line in reference:
    writer.writerow(line)
dest.close()
# --input_arb /Users/navealgarici/Documents/GitHub/SRE18/transfer/kaldi18/sre18/v2/exp/scores/sre16_eval_scores --input_arb /Users/navealgarici/Documents/GitHub/SRE18/transfer/kaldi18/sre18_afv/v2/exp/scores/sre16_eval_scores --reference /Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv --output /Users/navealgarici/Documents/GitHub/SRE18/tools/kaldi_scores_to_sre_scores/sre16_eval_scores_all.tsv
# --input_arb /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_plda_adap/v2/exp/scores/sre16_eval_scores_adapt --input_afv /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_avf/v2/exp/scores/sre16_eval_scores --reference /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv --output /docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/sre16_eval_scores_all_adap.tsv
#         /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_plda_adap/v2/exp/scores/sre16_eval_scores_adapt


# --input_arb /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_plda_adap_eval/v2/exp/scores/sre16_eval_scores_adapt                     --input_afv /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_avf_eval_diar/v2/exp/scores/sre16_eval_scores                     --reference /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv                     --output /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_avf_eval_diar/v2/exp/scores/tests_diar_control/sre16_eval_scores_adapt_1.tsv
