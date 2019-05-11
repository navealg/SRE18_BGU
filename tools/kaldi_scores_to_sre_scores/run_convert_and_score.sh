#!/usr/bin/env bash

python /docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/convert_scores_kaldi.py  --input_arb /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_chunk_test_take2/v2/exp/scores/sre16_eval_scores_adapt_2000_v2 \
                                                                                                        --input_afv /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_avf/v2/exp/scores/sre16_eval_scores \
                                                                                                        --reference /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv \
                                                                                                        --output /docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/sre16_eval_scores_adapt_2000_v2.tsv
python /docker_volume/Deployed_projects/SRE18/tools/scoring_software/sre18_submission_scorer.py         -o /docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/sre16_eval_scores_adapt_2000_v2.tsv \
                                                                                                        -l /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_trials.tsv \
                                                                                                        -r /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_trial_key.tsv

#python /docker_volume/Deployed_projects/SRE18/tools/scoring_software/sre18_submission_scorer.py         -o //docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/sre16_eval_scores_all_adap.tsv \
#                                                                                                        -l /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_trials.tsv \
#                                                                                                        -r /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_trial_key.tsv