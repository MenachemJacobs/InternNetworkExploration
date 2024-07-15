from shuffle.order_utils import *

jikeliCorpus = pd.read_excel('jikeliCorpus.xlsx', header=1)
nameset = set(jikeliCorpus['Username'])
antisemitic_tweets = store_indices(jikeliCorpus['Biased'], 1)
ok_tweets = store_indices(jikeliCorpus['Biased'], 0)
antisemites = list()
normal = list()
for i in range(0, len(jikeliCorpus['Biased'])):
    if jikeliCorpus['Biased'][i] == 1:
        antisemites.append(jikeliCorpus['Username'][i])
    else:
        normal.append(jikeliCorpus['Username'][i])
for index in ok_tweets:
    jikeliCorpus.at[index, 'Username'] = numpy.random.choice(normal)
for index in antisemitic_tweets:
    jikeliCorpus.at[index, 'Username'] = numpy.random.choice(antisemites)
new_dates = clustered_random_dates(datetime.datetime(2012, 11, 28, 12, minute=38, second=57), cluster_size=10,
                                   num_cluster=1130, remainder=11, years=1)
newData = pd.DataFrame({'Timestamp': new_dates, 'Biased': jikeliCorpus['Biased'], 'Username': jikeliCorpus['Username'],
                        'Tweet': jikeliCorpus['Text']})
newData.to_csv('newData.csv', index=False)
