import json
from pathlib import Path

import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import TVAESynthesizer
from shuffle import utils, create_accounts


# Function to perform synthesis and save
def synthesize_and_save(metadata, frame: pd.DataFrame, file_path, num_rows=10000):
    metadata.detect_from_dataframe(frame)
    metadata.update_column('Avg_Score', sdtype='numerical')
    metadata.update_column('Density_Score', sdtype='numerical')
    metadata.update_column('Positivity', sdtype='numerical')
    metadata.update_column('Antisemitic', sdtype='boolean')
    metadata.update_column('Age_Score', sdtype='numerical')

    synth = TVAESynthesizer(metadata, enforce_min_max_values=True,enforce_rounding=True)
    synth.fit(frame)
    sampled_data = synth.sample(num_rows=num_rows)
    synth.save(file_path)
    return sampled_data


def train_accounts():
    json_path = Path(__file__).parent.parent / 'has_run.json'
    with open(json_path, 'r') as f:
        flags: dict = json.load(f)
        f.close()
    if 'create_accounts' not in flags.keys() or not flags['create_accounts']:
        create_accounts.create_accounts()
    anti_data, pro_data = SingleTableMetadata(), SingleTableMetadata()
    anti_df = pd.DataFrame(columns=['Avg_Score', 'Age_Score', 'Density_Score', 'Positivity', 'Antisemitic'],
                           dtype=float)
    pro_df = pd.DataFrame(columns=['Avg_Score', 'Age_Score', 'Density_Score', 'Positivity', 'Antisemitic'],
                          dtype=float)

    accounts = list(utils.load_accounts())

    for index, acc in enumerate(accounts):
        acc.set_feature_scores()
        data_frame = anti_df if acc.isAntisemite else pro_df
        data_frame.loc[index] = [acc.average_message_score, acc.score_per_day, acc.score_by_density,
                                 acc.positives_per_tweet, acc.isAntisemite]

    # Synthesize and save data
    path = Path(__file__).parent.parent / 'shuffle'
    path = path.absolute()
    pro_accounts = synthesize_and_save(pro_data, pro_df, path / 'pro_account_synth.pkl',num_rows=10000)
    anti_accounts = synthesize_and_save(anti_data, anti_df, path / 'anti_account_synth.pkl',num_rows=10000)

    training_accounts = pd.concat([pro_accounts, anti_accounts])
    training_accounts.to_csv(path / 'training_accounts.csv', index=False)
    with open(json_path, 'w') as f:
        flags['training_accounts'] = True
        json.dump(flags, f)
        f.close()


if __name__ == '__main__':
    train_accounts()
