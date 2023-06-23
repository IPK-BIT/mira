import os
import pandas as pd
import yaml
from isatools import isatab
from icecream import ic

class MIAPPE:
    def __init__(self, directorypath: str) -> None:
        files       = os.listdir(directorypath)
        investname  = [i for i in files if i.startswith('i_')][0]
        studyname   = [s for s in files if s.startswith('s_')][0]
        assayname   = [a for a in files if a.startswith('a_')][0]
        dataname    = [d for d in files if d.startswith('d')][0]
        traitname   = [t for t in files if t.startswith('tdf')][0]

        self.ISA = None
        with open(os.path.join(directorypath, investname)) as fp:
            self.ISA = isatab.load(fp)       
        self.study                  = pd.read_csv(os.path.join(directorypath, studyname), delimiter='\t')
        self.assay                  = pd.read_csv(os.path.join(directorypath, assayname), delimiter='\t')
        self.datafile               = pd.read_csv(os.path.join(directorypath, dataname ), delimiter="\t")
        self.traitdefinitionfile    = pd.read_csv(os.path.join(directorypath, traitname), delimiter="\t")

def read_miappe(directorypath: str):
    global miappe 
    miappe = MIAPPE(directorypath)

global config
with open(os.path.join('/', 'config.yml')) as config_file:
        config = yaml.safe_load(config_file)