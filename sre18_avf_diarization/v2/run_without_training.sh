#!/bin/bash
# Copyright 2017-2018  David Snyder
#           2017-2018  Matthew Maciejewski
#
# Apache 2.0.
#
# This recipe demonstrates the use of x-vectors for speaker diarization.
# The scripts are based on the recipe in ../v1/run.sh, but clusters x-vectors
# instead of i-vectors.  It is similar to the x-vector-based diarization system
# described in "Diarization is Hard: Some Experiences and Lessons Learned for
# the JHU Team in the Inaugural DIHARD Challenge" by Sell et al.  The main
# difference is that we haven't implemented the VB resegmentation yet.

. ./cmd.sh
. ./path.sh
set -e
mfccdir=`pwd`/mfcc
vaddir=`pwd`/mfcc
data_location=/docker_volume
stage=0
nnet_dir=exp/xvector_nnet_1a/
thr=$1
# Prepare datasets
if [ $stage -le 0 ]; then
  # Prepare NIST SRE 2016 evaluation data.
  local/make_sre18_eval_afv_eval.pl $data_location/LDC2018E512_org data


fi

# Prepare features
if [ $stage -le 1 ]; then
#  for name in sre16_eval_enroll sre16_eval_test; do
  for name in sre16_eval_test; do
    steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj 30 --cmd "$train_cmd" \
      data/${name} exp/make_mfcc $mfccdir
    utils/fix_data_dir.sh data/${name}
    sid/compute_vad_decision.sh --nj 10 --cmd "$train_cmd" \
      data/${name} exp/make_vad $vaddir
    utils/fix_data_dir.sh data/${name}
  done

#  for name in sre16_eval_enroll sre16_eval_test; do
  for name in sre16_eval_test; do
    local/nnet3/xvector/prepare_feats.sh --nj 30 --cmd "$train_cmd" \
      data/$name data/${name}_cmn exp/${name}_cmn
    cp data/$name/vad.scp data/${name}_cmn/
    if [ -f data/$name/segments ]; then
      cp data/$name/segments data/${name}_cmn/
    fi
    utils/fix_data_dir.sh data/${name}_cmn
  done

    echo "0.01" > data/sre16_eval_test_cmn/frame_shift
  # Create segments to extract x-vectors from for PLDA training data.
  # The segments are created using an energy-based speech activity
  # detection (SAD) system, but this is not necessary.  You can replace
  # this with segments computed from your favorite SAD.
  diarization/vad_to_segments.sh --nj 30 --cmd "$train_cmd" \
    data/sre16_eval_test_cmn data/sre16_eval_test_cmn_segmented

fi


# Extract x-vectors
if [ $stage -le 7 ]; then

  diarization/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 5G" \
    --nj 27 --window 1.5 --period 0.75 --apply-cmn false \
    --min-segment 0.5 $nnet_dir \
    data/sre16_eval_test_cmn_segmented $nnet_dir/xvectors_sre16_eval_test
fi


# Perform PLDA scoring
if [ $stage -le 9 ]; then
  diarization/nnet3/xvector/score_plda.sh --cmd "$train_cmd --mem 4G" \
    --nj 10 $nnet_dir/xvectors_sre_combined $nnet_dir/xvectors_sre16_eval_test \
    $nnet_dir/xvectors_sre16_eval_test/plda_scores
fi


# Cluster the PLDA scores using a stopping threshold.
if [ $stage -le 10 ]; then
#  # First, we find the threshold that minimizes the DER on each partition of
#  # callhome.
#  mkdir -p $nnet_dir/tuning
#  for dataset in sre16_eval_test; do
#    echo "Tuning clustering threshold for $dataset"
#    best_der=100
#    best_threshold=0
#    utils/filter_scp.pl -f 2 data/$dataset/wav.scp \
#      data/callhome/fullref.rttm > data/$dataset/ref.rttm
#
#    # The threshold is in terms of the log likelihood ratio provided by the
#    # PLDA scores.  In a perfectly calibrated system, the threshold is 0.
#    # In the following loop, we evaluate the clustering on a heldout dataset
#    # (callhome1 is heldout for callhome2 and vice-versa) using some reasonable
#    # thresholds for a well-calibrated system.
#    for threshold in -0.3 -0.2 -0.1 -0.05 0 0.05 0.1 0.2 0.3; do
#      diarization/cluster.sh --cmd "$train_cmd --mem 4G" --nj 10 \
#        --threshold $threshold $nnet_dir/xvectors_$dataset/plda_scores \
#        $nnet_dir/xvectors_$dataset/plda_scores_t$threshold
#
#      md-eval.pl -1 -c 0.25 -r data/$dataset/ref.rttm \
#       -s $nnet_dir/xvectors_$dataset/plda_scores_t$threshold/rttm \
#       2> $nnet_dir/tuning/${dataset}_t${threshold}.log \
#       > $nnet_dir/tuning/${dataset}_t${threshold}
#
#      der=$(grep -oP 'DIARIZATION\ ERROR\ =\ \K[0-9]+([.][0-9]+)?' \
#        $nnet_dir/tuning/${dataset}_t${threshold})
#      if [ $(echo $der'<'$best_der | bc -l) -eq 1 ]; then
#        best_der=$der
#        best_threshold=$threshold
#      fi
#    done
#    echo "$best_threshold" > $nnet_dir/tuning/${dataset}_best
#  done

#  # Cluster callhome1 using the best threshold found for callhome2.  This way,
#  # callhome2 is treated as a held-out dataset to discover a reasonable
#  # stopping threshold for callhome1.
#  diarization/cluster.sh --cmd "$train_cmd --mem 4G" --nj 10 \
#    --threshold $(cat $nnet_dir/tuning/callhome2_best) \
#    $nnet_dir/xvectors_sre16_eval_test/plda_scores $nnet_dir/xvectors_sre16_eval_test/plda_scores

  diarization/cluster.sh --cmd "$train_cmd --mem 4G" --nj 10 \
    --threshold $thr \
    $nnet_dir/xvectors_sre16_eval_test/plda_scores $nnet_dir/xvectors_sre16_eval_test/plda_scores

#  counter=1
#  for thr in -5.0 -4.5 -4.0 -3.5 -3.0 -2.5 -2.0 -1.0 -0.7 -0.5 -0.3 -0.2 -0.1 -0.05 0 0.05 0.1 0.2 0.3; do
#    diarization/cluster.sh --cmd "$train_cmd --mem 4G" --nj 10 \
#    --threshold $thr \
#    $nnet_dir/xvectors_sre16_eval_test/plda_scores $nnet_dir/xvectors_sre16_eval_test/plda_scores/thr${thr//./}
#  done

#  mkdir -p $nnet_dir/results
#  # Now combine the results for callhome1 and callhome2 and evaluate it
#  # together.
#  cat $nnet_dir/xvectors_callhome1/plda_scores/rttm \
#    $nnet_dir/xvectors_callhome2/plda_scores/rttm | md-eval.pl -1 -c 0.25 -r \
#    data/callhome/fullref.rttm -s - 2> $nnet_dir/results/threshold.log \
#    > $nnet_dir/results/DER_threshold.txt
#  der=$(grep -oP 'DIARIZATION\ ERROR\ =\ \K[0-9]+([.][0-9]+)?' \
#    $nnet_dir/results/DER_threshold.txt)
#  # Using supervised calibration, DER: 8.39%
#  # Compare to 10.36% in ../v1/run.sh
#  echo "Using supervised calibration, DER: $der%"
fi

## Cluster the PLDA scores using the oracle number of speakers
#if [ $stage -le 11 ]; then
#  # In this section, we show how to do the clustering if the number of speakers
#  # (and therefore, the number of clusters) per recording is known in advance.
#  diarization/cluster.sh --cmd "$train_cmd --mem 4G" \
#    --reco2num-spk data/sre16_eval_test/reco2num_spk \
#    $nnet_dir/xvectors_sre16_eval_test/plda_scores $nnet_dir/xvectors_sre16_eval_test/plda_scores_num_spk
#  mkdir -p $nnet_dir/results
#
##  # Now combine the results for callhome1 and callhome2 and evaluate it together.
##  cat $nnet_dir/xvectors_callhome1/plda_scores_num_spk/rttm \
##  $nnet_dir/xvectors_callhome2/plda_scores_num_spk/rttm \
##    | md-eval.pl -1 -c 0.25 -r data/callhome/fullref.rttm -s - 2> $nnet_dir/results/num_spk.log \
##    > $nnet_dir/results/DER_num_spk.txt
##  der=$(grep -oP 'DIARIZATION\ ERROR\ =\ \K[0-9]+([.][0-9]+)?' \
##    $nnet_dir/results/DER_num_spk.txt)
##  # Using the oracle number of speakers, DER: 7.12%
##  # Compare to 8.69% in ../v1/run.sh
##  echo "Using the oracle number of speakers, DER: $der%"
#fi
