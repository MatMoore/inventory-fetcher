import csv
from gensim.utils import tokenize
from gensim.parsing.preprocessing import STOPWORDS

with open('dictionary.txt', 'w') as outfile:
    with open('audits_with_content.csv') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            text = row[-2]
            if len(text) < 1000:
                continue

            for token in tokenize(text, to_lower=True, deacc=True):
                if token in STOPWORDS:
                    continue

                outfile.write('{} {}\n'.format(row[0], token))
