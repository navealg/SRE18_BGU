tests=${1:-1}
# method=$3
# max_num=${4:-$tests}
stage=${2:-0}
start=${3:-1}
path_to_scores=`pwd`/exp/scores
subdir_scores=${4:-tests}
chunk_size=${5:-15000}
#subdir_scores=tests
#    for i in `seq $start 500 $tests`;

if [ $stage -le 0 ]; then
    mkdir $path_to_scores/$subdir_scores
    for i in `seq -f '%04g' $start $tests`;
        do
            echo **********`date +%R`   Run number: $i**********
            ./run_without_training.sh $chunk_size
            python /docker_volume/Deployed_projects/SRE18/tools/kaldi_scores_to_sre_scores/convert_scores_kaldi.py \
                        --input_arb /docker_volume/Deployed_projects/SRE18/transfer/kaldi18/sre18_plda_adap_eval/v2/exp/scores/sre16_eval_scores_adapt \
                        --input_afv $path_to_scores/sre16_eval_scores \
                        --reference /docker_volume/Deployed_projects/SRE18/tools/scoring_software/system_output/sre18_dev_system_output.tsv \
                        --output $path_to_scores/$subdir_scores/sre16_eval_scores_adapt_$i.tsv
        done
fi

if [ $stage -le 1 ]; then
    mkdir $path_to_scores/$subdir_scores/fused
    echo **********`date +%R`   fusing**********
    python /docker_volume/Deployed_projects/SRE18/tools/fuse_scores_kaldi.py \
                            --scores_dir $path_to_scores/$subdir_scores \
                            --max_num $tests \
                            -all_range \
                            --output $path_to_scores/$subdir_scores/fused/sre16_eval_scores_adapt

fi

if [ $stage -le 2 ]; then
    sh /docker_volume/Deployed_projects/SRE18/tools/scoring_software/score_all_dir.sh $path_to_scores/$subdir_scores >> $path_to_scores/$subdir_scores/results.txt &
fi
