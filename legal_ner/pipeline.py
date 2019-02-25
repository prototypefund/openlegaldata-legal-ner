import spacy

from legal_ner.ner.matcher import EntityMatcher
from legal_ner.ner.regexp_matcher import RegexpEntityMatcher
from legal_ner.ner.regexps.dates import GermanDates
from legal_ner.ner.regexps.money import GermanEuros
from legal_ner.ner.regexps.percents import GermanPercentages
from legal_ner.ner.matcher_patterns import party, cause
from legal_ner.tokenization.special_cases import special_cases
from legal_ner.tokenization.tokenizer import create_custom_tokenizer


class Pipeline:

    def __init__(self, model):
        self.model = model

    def run(self, text):
        nlp = spacy.load(self.model)

        nlp.tokenizer = create_custom_tokenizer(nlp)
        for word, special_case in special_cases.items():
            nlp.tokenizer.add_special_case(word, special_case)

        party_matcher = EntityMatcher(nlp, party, 'PARTY')
        nlp.add_pipe(party_matcher, name='party_matcher', after='ner')

        cause_matcher = EntityMatcher(nlp, cause, 'CAUSE')
        nlp.add_pipe(cause_matcher, name='cause_matcher', after='ner')

        date_matcher = RegexpEntityMatcher(nlp, 'DATE', GermanDates())
        nlp.add_pipe(date_matcher, name='regexp_dates_extractor', after='ner')

        percents_matcher = RegexpEntityMatcher(nlp, 'EURO', GermanEuros())
        nlp.add_pipe(percents_matcher, name='regexp_euro_extractor', after='ner')

        percents_matcher = RegexpEntityMatcher(nlp, 'PERCENT', GermanPercentages())
        nlp.add_pipe(percents_matcher, name='regexp_percent_extractor', after='ner')

        doc = nlp(text)

        return doc
