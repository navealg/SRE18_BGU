path_to_scores=`pwd`/exp/scores
subdir_scores=${4:-thr}
chunk_size=${5:-30000}
thr=-2
stage=0
start=-11.2
interval=0.5
end=$start
for j in `seq $start $interval $end`; do
subdir_scores=grid_newnet/thr_$j
thr=$j
stage=0





current_dir=`pwd`

org_data_dir=/docker_volume/LDC2018E512

#cd /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_avf_diarization_eval/v2/
#/docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_avf_diarization_eval/v2/run_without_training.sh $thr
#
#cd $org_data_dir/data
#for i in $(find . -type f -name 'test_diarization*'); do rm $i; done
#for i in $(find ./test -type f -name '*sph'); do rm $i; done
#python /docker_volume/Deployed_projects/SRE18/tools/split_audio_files_by_rttn.py --rttn /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_avf_diarization_eval/v2/exp/xvector_nnet_1a/xvectors_sre16_eval_test/plda_scores/rttm --org-data-dir $org_data_dir
#for i in $(find . -type f -name 'test_diarization*'); do sudo chmod 777 $i; done


cd $current_dir

idx=0
if [ $stage -le 0 ]; then
    cd $org_data_dir/data
    for i in $(find . -type f -name 'test_diarization*'); do
        idx=$((idx + 1))
        echo $i;
#        cd $org_data_dir/data
#        $i

        cd $current_dir
        ./run_without_training.sh $chunk_size
        mkdir -p $path_to_scores/$subdir_scores
        python /docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/convert_scores_kaldi.py \
                    --input_arb /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_plda_adap/v2/exp/scores/sre16_eval_scores_adapt \
                    --input_afv $path_to_scores/sre16_eval_scores \
                    --reference /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv \
                    --output $path_to_scores/$subdir_scores/sre16_eval_scores_adapt_$idx.tsv
#        echo "        python /docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/convert_scores_kaldi.py \
#                    --input_arb /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_plda_adap/v2/exp/scores/sre16_eval_scores_adapt \
#                    --input_afv $path_to_scores/sre16_eval_scores \
#                    --reference /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv \
#                    --output $path_to_scores/$subdir_scores/sre16_eval_scores_adapt_$idx.tsv"
    done
fi

#if [ $stage -le 1 ]; then
#    mkdir $path_to_scores/$subdir_scores/fused
#    echo **********`date +%R`   fusing**********
#    python /docker_volume/Deployed_projects/SRE18/tools/fuse_scores_kaldi.py \
#                            --scores_dir $path_to_scores/$subdir_scores \
#                            --max_num $idx \
#                            -all_range \
#                            --output $path_to_scores/$subdir_scores/fused/sre16_eval_scores_adapt
#
#fi

if [ $stage -le 2 ]; then
    sh /docker_volume/Deployed_projects/SRE18/tools/scoring_software/score_all_dir.sh $path_to_scores/$subdir_scores >> $path_to_scores/results.txt &
fi

done