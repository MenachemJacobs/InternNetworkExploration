from utils import *

jikeliCorpus = pd.read_excel('jikeliCorpus.xlsx', header=1)
name_set = set(jikeliCorpus['Username'])
antisemitic_tweets = store_indices(jikeliCorpus['Biased'], 1)
ok_tweets = store_indices(jikeliCorpus['Biased'], 0)
antisemites = list()
normal = list()
indexes = numpy.random.choice(range(0, len(jikeliCorpus['Username'])), 2500)
for i in indexes:
    if jikeliCorpus['Biased'][i] == 1:
        antisemites.append(jikeliCorpus['Username'][i])
    else:
        normal.append(jikeliCorpus['Username'][i])
antisemite_network = follower_network(antisemites, antisemites)
distinct_names = normal
distinct_names.extend(antisemites)
normal_network = follower_network(normal, distinct_names)
all_network = dict()
for key in antisemite_network.keys():
    all_network[str(key)] = antisemite_network[key]
for key in normal_network.keys():
    all_network[str(key)] = normal_network[key]
for index in ok_tweets:
    jikeliCorpus.at[index, 'Username'] = numpy.random.choice(normal)
for index in antisemitic_tweets:
    jikeliCorpus.at[index, 'Username'] = numpy.random.choice(antisemites)
follow_list = list()
for name in jikeliCorpus['Username']:
    follow_list.append(all_network[str(name)])
new_dates = clustered_random_dates(datetime(2012, 11, 28, 12, minute=38, second=57), cluster_size=10,
                                   num_cluster=1130, remainder=11, years=1)
newData = pd.DataFrame({'Timestamp': new_dates, 'Biased': jikeliCorpus['Biased'], 'Username': jikeliCorpus['Username'],
                        'Tweet': jikeliCorpus['Text'], 'Users Followed': follow_list})
newData.sort_values(by='Username', inplace=True)
print(len(set(newData['Username'])))
newData.to_csv('newData.csv', index=False)
