#!/usr/bin/env bash
#python sre18_submission_scorer.py -o /Users/navealgarici/Documents/GitHub/SRE18/temp/nist18_baseline_e2e_all_swb_ubm_mix_and_swb_ivector/scores/plda/ztnorm/scores-dev-out.tsv \
#-l /Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trials.tsv -r /Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trial_key.tsv

python sre18_submission_scorer.py -o /Users/navealgarici/Documents/GitHub/SRE18/tools/kaldi_scores_to_sre_scores/sre16_eval_scores_all_adap.tsv \
-l /Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trials.tsv -r /Users/navealgarici/Documents/GitHub/SRE18/tools/scoring_software/system_output/sre18_dev_trial_key.tsv


