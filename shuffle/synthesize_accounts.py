import pandas as pd
from sdv.metadata import MultiTableMetadata, SingleTableMetadata
from sdv.single_table import CTGANSynthesizer

from shuffle.utils import parse_list_ints

#load metadata from file
metadata = SingleTableMetadata()
messageData = pd.read_excel('jikeliCorpus.xlsx', header=1)
pro_indices = list()
for row in range(len(messageData['ID'])):
    if messageData['Biased'][row] < 1:
        pro_indices.append(row)
messageData.drop(index=pro_indices, inplace=True)
metadata.detect_from_dataframe(messageData)
for column in ('Username','Text'):
    metadata.update_column(column,pii=False)
print(metadata.columns)
