# this file is to enable the creation and consolidation of a dictionary that holds a primary and ensuing per-chunk dataframes 
# for the purpose of statistical analysis of the evidence based, extracted information 
# the dataframe will belong to a particular uploaded text/ run


# the generated per-chunk json files will be parsed here, cleaned and loaded into the dataframe

import pandas as pd 


# dataframe has the following structure
# col 0 | col 1 | col 2 | col 3 |
# chunk |themes |chlngs.|exprncs|
# 1     |{Academic:eID, Challenging:eID} | [Stress:eID]| [CS Deadline:eID]


# note that eID == evidenceID, in notation x-XX | chunkSerialNumber | eID from chunk 7, extraction 13, would be 7-13