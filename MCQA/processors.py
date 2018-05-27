"""
Class that process questionnaires statements
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer

from MCQA.data import Questionnaire


class BasicProcessor:

    def __init__(self, questionnaire):
        """
        :param questionnaire: the Questionnaire to process
        :type questionnaire: Questionnaire
        """
        self.questionnaire = questionnaire

    def process(self):
        """
        Apply processing to Questionnaire
        """
        for question in self.questionnaire.questions:
            # remove non alphanumeric characters
            question.statement = re.sub(r'([^\s\w]|_)+', '', question.statement).strip()

            # replace multiple spaces to one
            question.statement = ' '.join(question.statement.split())


class TfIdfProcessor(BasicProcessor):

    def __init__(self, questionnaire, corpus_frequency_threshold=0.05):
        """
        :param questionnaire: the Questionnaire to process
        :type questionnaire: Questionnaire
        :param corpus_frequency_threshold: all words exceeding this frequency threshold will be discarded
        :type corpus_frequency_threshold: int
        """
        BasicProcessor.__init__(self, questionnaire)
        self.corpus_frequency_threshold = corpus_frequency_threshold
        self.stopwords = None

    def process(self):
        """
        Apply processing to Questionnaire
        """
        # from questionnaire to corpus
        corpus = [q.statement for q in self.questionnaire.questions]

        # count corresponding words
        vectorizer = TfidfVectorizer(use_idf=False, norm=None)
        X = vectorizer.fit_transform(corpus)

        # get stop words (=words exceeding frequency threshold)
        self.stopwords = [word for word, tf in zip(vectorizer.get_feature_names(), X.sum(axis=0).tolist()[0])
                          if tf/len(corpus) > self.corpus_frequency_threshold]

        # reconstruct the corpus
        for question in self.questionnaire.questions:
            question.statement = ' '.join([word for word in question.statement.split(' ')
                                           if word.lower() not in self.stopwords])
