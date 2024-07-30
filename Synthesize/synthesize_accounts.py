import pandas as pd
from sdv.metadata import MultiTableMetadata, SingleTableMetadata
from sdv.single_table import TVAESynthesizer

from shuffle import utils
from shuffle.utils import parse_list_ints

anti_data = SingleTableMetadata()
pro_data = SingleTableMetadata()
accounts = utils.load_accounts()
anti_df = pd.DataFrame(columns=['Avg_Score', 'Age_Score', 'Density_Score', 'Positivity', 'Antisemitic'], dtype=float)
pro_df = pd.DataFrame(columns=['Avg_Score', 'Age_Score', 'Density_Score', 'Positivity', 'Antisemitic'], dtype=float)
accounts = list(accounts)
for index in range(len(accounts)):
    acc = accounts[index]
    acc.set_feature_scores()
    if acc.isAntisemite:
        anti_df.loc[index, 'Avg_Score'] = acc.average_message_score
        anti_df.loc[index, 'Age_Score'] = acc.score_per_day
        anti_df.loc[index, 'Density_Score'] = acc.score_by_density
        anti_df.loc[index, 'Positivity'] = acc.positives_per_tweet
        anti_df.loc[index, 'Antisemitic'] = acc.isAntisemite
    else:
        pro_df.loc[index, 'Avg_Score'] = acc.average_message_score
        pro_df.loc[index, 'Age_Score'] = acc.score_per_day
        pro_df.loc[index, 'Density_Score'] = acc.score_by_density
        pro_df.loc[index, 'Positivity'] = acc.positives_per_tweet
        pro_df.loc[index, 'Antisemitic'] = acc.isAntisemite

anti_data.detect_from_dataframe(anti_df)
anti_data.update_column('Avg_Score', sdtype='numerical')
anti_data.update_column('Density_Score', sdtype='numerical')
anti_data.update_column('Positivity', sdtype='numerical')
anti_data.update_column('Antisemitic', sdtype='boolean')
anti_data.update_column('Age_Score', sdtype='numerical')

pro_data.detect_from_dataframe(pro_df)
pro_data.update_column('Avg_Score', sdtype='numerical')
pro_data.update_column('Density_Score', sdtype='numerical')
pro_data.update_column('Positivity', sdtype='numerical')
pro_data.update_column('Antisemitic', sdtype='boolean')
pro_data.update_column('Age_Score', sdtype='numerical')

anti_synthesizer = TVAESynthesizer(anti_data, enforce_min_max_values=True)
anti_synthesizer.fit(anti_df)
anti_accounts = anti_synthesizer.sample(num_rows=10000)
anti_synthesizer.save('shuffle/anti_account_synth.pkl')

pro_synthesizer = TVAESynthesizer(anti_data, enforce_min_max_values=True)
pro_synthesizer.fit(pro_df)
pro_accounts = pro_synthesizer.sample(num_rows=10000)
pro_synthesizer.save('shuffle/pro_account_synth.pkl')
training_accounts = pd.concat([pro_accounts,anti_accounts])
training_accounts.to_csv('shuffle/training_accounts.csv')