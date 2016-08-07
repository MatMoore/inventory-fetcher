# Inventory fetcher

This repo contains a number of unmaintained scripts for extracting text data from inventories of GOV.UK content.

The text comes from [https://github.com/alphagov/rummager]()

See also: [https://github.com/alphagov/govuk-lda-tagger](GOV.UK LDA Tagger)

## Data files

- [audits.csv](audits.csv): All content belonging to the education theme
- [audits_with_content.csv](audits_with_content.csv): Link, Content, Rummager indexable text, Is Withdrawn? (withdrawn if true, otherwise not withdrawn)
- dictionary.txt: First column is the link, second column is a word that appears in that document. Any document with text < 1000 characters is skipped. Stop words are ignored.

## Generate dictionary.txt

```
pip install -r requirements.txt
python make_dictionary.py
```
