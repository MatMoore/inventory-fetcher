import csv
from gensim.corpora import Dictionary, MmCorpus, TextCorpus
from gensim.models import TfidfModel
from gensim.utils import tokenize
from gensim.parsing.preprocessing import STOPWORDS

outp = 'govuk'


class Corpus(TextCorpus):
    def get_texts(self):
        with self.getstream() as stream:
            reader = csv.reader(stream)
            for row in reader:
                text = row[-2]
                if len(text) < 1000:
                    continue

                yield [
                    token for token
                    in tokenize(text, to_lower=True, deacc=True)
                    if token not in STOPWORDS
                ]


DEFAULT_DICT_SIZE = 100000

f = open('audits_with_content.csv')
wiki = Corpus(f)

# only keep the most frequent words (out of total ~8.2m unique tokens)
wiki.dictionary.filter_extremes(no_below=20, no_above=0.1, keep_n=DEFAULT_DICT_SIZE)
# save dictionary and bag-of-words (term-document frequency matrix)
MmCorpus.serialize(outp + '_bow.mm', wiki, progress_cnt=10000)
wiki.dictionary.save_as_text(outp + '_wordids.txt.bz2')
# load back the id->word mapping directly from file
# this seems to save more memory, compared to keeping the wiki.dictionary object from above
dictionary = Dictionary.load_from_text(outp + '_wordids.txt.bz2')

# initialize corpus reader and word->id mapping
mm = MmCorpus(outp + '_bow.mm')

# build tfidf, ~50min
tfidf = TfidfModel(mm, id2word=dictionary, normalize=True)
tfidf.save(outp + '.tfidf_model')

# save tfidf vectors in matrix market format
MmCorpus.serialize(outp + '_tfidf.mm', tfidf[mm], progress_cnt=10000)
