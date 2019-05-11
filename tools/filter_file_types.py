import os
from shutil import copyfile

paths = ['/docker_volume/SRE04',
         '/docker_volume/SRE05',
         '/docker_volume/SRE06',
         '/docker_volume/SRE08',
         '/docker_volume/SRE08_Followup',
         '/docker_volume/SRE10',
         '/docker_volume/SRE10_16K']
path_to_doc_dir = '/docker_volume/Deployed_projects/SRE18/temp/SRE_04_to_10_doc'
# extentions = []
# for root in paths:
#     for path, subdirs, files in os.walk(root):
#         for name in files:
#             extentions.append(name.split(".")[-1])
#
# s = []
# for i in extentions:
#    if i not in s:
#       s.append(i)


all_extentions = ['readme', 'nbest', 'scr', 'ctm', 'trn', 'ndx', 'txt', 'pdf', 'doc', 'tbl', 'cfm', 'sph']
wanted_extentions = ['readme', 'trn', 'ndx', 'txt', 'pdf', 'doc', 'tbl']
not_wanted_extentions = [item for item in all_extentions if item not in wanted_extentions]
wanted_files = []
for root in paths:
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.split(".")[-1] not in not_wanted_extentions:
                wanted_file = os.path.join(path, name)
                wanted_files.append(wanted_file)
                destination = os.path.join(path_to_doc_dir, path.split('docker_volume/')[-1])
                try:
                    os.makedirs(destination)
                except:
                    x = 1
                copyfile(wanted_file, os.path.join(destination, name))
x = 1


