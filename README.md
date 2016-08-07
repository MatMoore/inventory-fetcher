# Inventory fetcher

Unmaintained scripts for extracting text data from inventories of GOV.UK content and feeding it into [Gensim](https://radimrehurek.com/gensim/).

The text comes from [Rummager](https://github.com/alphagov/rummager), the GOV.UK search API.

[GOV.UK LDA Tagger](https://github.com/alphagov/govuk-lda-tagger) is a more recent attempt to apply topic modelling to GOV.UK.

## Data files

- [audits.csv](audits.csv): All content belonging to the education theme
- [audits_with_content.csv](audits_with_content.csv): Link, Content, Rummager indexable text, Is Withdrawn? (withdrawn if true, otherwise not withdrawn)
- dictionary.txt: First column is the link, second column is a word that appears in that document. Any document with text < 1000 characters is skipped. Stop words are ignored.

## Generate dictionary.txt

```
pip install -r requirements.txt
python make_dictionary.py
```
