import pandas as pd

df_populated = pd.read_csv('newDataClone.csv')
df_messageData = pd.DataFrame(columns=['TweetID', 'Tweet', 'Biased', 'Timestamp', 'Username'])

# Find account data
try:
    df_accountData = pd.read_csv('accountData.csv')
except FileNotFoundError:
    df_accountData = pd.DataFrame(columns=['Username', 'Biased', 'TweetIDs', 'Users Followed'])

# Initialize messageData DataFrame
df_messageData = pd.DataFrame({
    'TweetID': range(1, len(df_populated) + 1),
    'Tweet': df_populated['Tweet'],
    'Biased': df_populated['Biased'],
    'Timestamp': df_populated['Timestamp'],
    'Username': df_populated['Username']
})

# Save messageData.csv
df_messageData.to_csv('messageData.csv', index=False)

for index, row in df_populated.iterrows():
    username = row["Username"]
    bias_score = row["Biased"]
    tweet_id = df_messageData.at[index, 'TweetID']

    if username in df_accountData["Username"].values:
        idx = df_accountData.index[df_accountData["Username"] == username].iloc[0]
        current_tweet_ids = df_accountData.at[idx, "TweetIDs"]
        current_bias_score = df_accountData.at[idx, "Biased"]

        if current_bias_score < 2:
            current_bias_score += bias_score

        update_tweet_ids = f"{current_tweet_ids},{df_messageData.at[index, 'TweetID']}"
        df_accountData.at[idx, "Biased"] = current_bias_score
        df_accountData.at[idx, "TweetIDs"] = update_tweet_ids
    else:
        # Add the following new row to df_accountData
        new_row = {
            "Username": username,
            "Biased": bias_score,
            "TweetIDs": str(df_messageData.at[index, 'TweetID']),
            "Users Followed": row['Users Followed']
        }
        df_accountData = pd.concat([df_accountData, pd.DataFrame([new_row])], ignore_index=True)

# Save updated accountData.csv
df_accountData.to_csv('accountData.csv', index=False)