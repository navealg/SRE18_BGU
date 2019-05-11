## The BGU 2018 NIST Speaker Recognition Evaluation System

This is a repository contains the BGU team speaker recognition system and participation in the 2018 NIST speaker recognition evaluation.


### Requirements
- Install the kaldi tooklit using the instructions [here](http://kaldi-asr.org/doc/install.html).
- Install Sox package `sudo apt-get install sox`.
### Instructions
- Copy directories into the `egs` subfolder in the kaldi directory.
- For each experiment, make sure that the data path in `run_without_training.sh` matches the path to the data on your machine.
- Run `run_without_training.sh` for each experiment.
- Use the diarization and scoring tools inside the `tools` directory.




