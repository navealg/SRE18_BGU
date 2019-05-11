import csv
import os

path = "/docker_volume/Deployed_projects/SRE18/test"

def lookup(reader, lookup_atr, lookup_val, return_atr):
    for r in reader:
        if r[lookup_atr] == lookup_val:
            return r[return_atr]
    return

def merge_column_from_lookup(base_reader, lookup_reader, lookup_atr, return_atr, return_atr_new_name=None):
    if return_atr_new_name == None:
        return_atr_new_name = return_atr
    for base in base_reader:
        base[return_atr_new_name] = lookup(lookup_reader, lookup_atr, base[lookup_atr], return_atr)
    return base_reader

def remove_atrs(reader, atr_list):
    for r in reader:
        [r.pop(atr) for atr in atr_list]
    return reader

def gen_model_list(reader, path):
    for_models_file = open(path + '/for_models.lst', 'w')
    for r in reader:
        # if r['gender'] == 'female':
        line = f"{path.split('transfer/')[-1]}/data/enrollment/{r['segmentid'].split('.')[0]} {r['modelid']} {r['subjectid']}\n"
        for_models_file.write(line)
    for_models_file.close()
    return

def gen_score_list(reader, path):
    for_models_file = open(path + '/for_scores.lst', 'w')
    for r in reader:
        # if r['gender'] == 'female':
        line = f"{path.split('transfer/')[-1]}/data/test/{r['segmentid'].split('.')[0]} {r['modelid']} {r['subject_id_model']} {r['subject_id_test']}\n"
        for_models_file.write(line)
    for_models_file.close()
    return

def gen_unlabeled_list(reader, path):
    for_models_file = open(path + '/for_scores.lst', 'w')
    for r in reader:
        line = f"{path.split('transfer/')[-1]}/data/unlabeled/{r['segment']} XXX\n"
        for_models_file.write(line)
    for_models_file.close()
    return


# call_sides_reader = list(csv.DictReader(open(path + "/metadata/call_sides.tsv", 'r'), delimiter='\t'))
# calls_reader = list(csv.DictReader(open(path + "/metadata/calls.tsv", 'r'), delimiter='\t'))
# subjects_reader = list(csv.DictReader(open(path + "/metadata/subjects.tsv", 'r'), delimiter='\t'))
# enrollment_reader = list(csv.DictReader(open(path + "/docs/sre18_dev_enrollment.tsv", 'r'), delimiter='\t'))
# segment_key_reader = list(csv.DictReader(open(path + "/docs/sre18_dev_segment_key.tsv", 'r'), delimiter='\t'))
# trial_reader = list(csv.DictReader(open(path + "/docs/sre18_dev_trial_key.tsv", 'r'), delimiter='\t'))
enrollment_reader = list(csv.DictReader(open(path + "/sre18_dev_enrollment.tsv", 'r'), delimiter='\t'))
segment_key_reader = list(csv.DictReader(open(path + "/sre18_dev_segment_key.tsv", 'r'), delimiter='\t'))
trial_reader = list(csv.DictReader(open(path + "/sre18_dev_trial_key.tsv", 'r'), delimiter='\t'))

# unlabeled_major_reader = list(csv.DictReader(open(path + "/docs/sre16_dev_unlabeled_major.tsv", 'r'), delimiter='\t'))
# gen_unlabeled_list(unlabeled_major_reader, path)
# unlabeled_minor_reader = list(csv.DictReader(open(path + "/docs/sre16_dev_unlabeled_minor.tsv", 'r'), delimiter='\t'))
# gen_unlabeled_list(unlabeled_minor_reader, path)
# unlabeled_list = [dict({'segment': u.split('.')[0]}) for u in os.listdir(path + "/data/unlabeled")]
# gen_unlabeled_list(unlabeled_list, path)

def get_model_list(enrollment_reader=enrollment_reader, segment_key_reader=segment_key_reader):
    # segment_key_reader = merge_column_from_lookup(segment_key_reader, call_sides_reader, 'call_id', 'subject_id')
    # segment_key_reader = merge_column_from_lookup(segment_key_reader, subjects_reader, 'subject_id', 'sex')
    # segment_key_reader = merge_column_from_lookup(segment_key_reader, calls_reader, 'call_id', 'language_id')
    segment_key_reader = remove_atrs(segment_key_reader, ['partition'])
    segment_key_reader = remove_atrs(segment_key_reader, ['phone_number'])
    segment_key_reader = remove_atrs(segment_key_reader, ['speech_duration'])
    segment_key_reader = remove_atrs(segment_key_reader, ['data_source'])

    enrollment_reader = remove_atrs(enrollment_reader, ['side'])
    enrollment_reader = merge_column_from_lookup(enrollment_reader, segment_key_reader, 'segmentid', 'gender')
    enrollment_reader = merge_column_from_lookup(enrollment_reader, segment_key_reader, 'segmentid', 'subjectid')

    return enrollment_reader

# gen_model_list(enrollment_reader, path)

# trial_reader = remove_atrs(trial_reader, ['side'])
# trial_reader = merge_column_from_lookup(trial_reader, segment_key_reader, 'segmentid', 'gender')
# trial_reader = merge_column_from_lookup(trial_reader, enrollment_reader, 'modelid', 'subjectid', 'subject_id_model')
# trial_reader = merge_column_from_lookup(trial_reader, segment_key_reader, 'segmentid', 'subjectid', 'subject_id_test')
#
# gen_score_list(trial_reader, path)

x = 1