import logging
import gensim
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO
)

id2word = gensim.corpora.Dictionary.load_from_text('govuk_wordids.txt')
mm = gensim.corpora.MmCorpus('govuk_tfidf.mm')
print(mm)

lda = gensim.models.ldamodel.LdaModel(
    corpus=mm,
    id2word=id2word,
    num_topics=20,
    update_every=1,
    chunksize=10000,
    passes=2
)

lda.print_topics(20)


#def present_bow(bow):
#    word_frequencies = [
#        (id2word.get(word_id), freq)
#        for word_id, freq in bag_o_words
#    ]
#    top_ten = sorted(word_frequencies, reverse=True, key=lambda x: x[1])[:10]
#    return top_ten
#
#for bag_o_words in mm[:10]:
#    print(present_bow(bag_o_words))
#    print('')
#    topics = lda.get_document_topics(bag_o_words)
#    for topic_id, prob in topics:
#        print('\ttopic {} with prob {}'.format(topic_id, prob))
#        topic_words = lda.get_topic_terms(topic_id, topn=5)
#        print ('\texample words: {}'.format(', '.join(topic_words)))
