#! /usr/bin/env python

# ENVIRONMENT
import os
import sys
import yaml
import git

ROOT = git.Repo('.', search_parent_directories = True).working_tree_dir
sys.path.append(ROOT)
import lib.gslab_make.gslab_make as gs

PATHS = {
    'config_user'     : '../config_user.yaml',
    'temp_dir'        : 'temp/',
    'output_dir'      : 'output/',
    'pdf_dir'         : 'output/',
    'makelog'         : 'log/make.log',
    'output_statslog' : 'log/output_stats.log',
    'output_headslog' : 'log/output_heads.log', 
    'link_maplog'     : 'log/link_map.log',
    'link_statslog'   : 'log/link_stats.log',
    'link_headslog'   : 'log/link_heads.log'
}

# CONFIG USER
config_user = yaml.load(open(PATHS['config_user'], 'rb'))
gs.private.metadata.default_executables[os.name].update(config_user['local']['executables']) 
path_mappings = dict(config_user['external'], root = ROOT) 

# START
gs.remove_dir(['input', 'external'])
gs.clear_dir(['output', 'log'])
gs.start_makelog(PATHS)

# GET INPUT FILES
inputs    = gs.create_links(dict(PATHS, link_dir = 'input')   , ['inputs.txt']   , path_mappings)
externals = gs.create_links(dict(PATHS, link_dir = 'external'), ['externals.txt'], path_mappings)
gs.write_link_logs(PATHS, inputs + externals)

# RUN SCRIPTS
gs.run_r(PATHS, program = 'code/create_table_data.r')
gs.run_stata(PATHS, program = 'code/create_graph_data.do')

# LOG OUTPUTS
gs.log_files_in_output(PATHS)

# END
gs.end_makelog(PATHS)
raw_input('\n Press <Enter> to exit.')