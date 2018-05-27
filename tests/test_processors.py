import unittest

from MCQA.data import Questionnaire, Question
from MCQA import processors


class TestProcessors(unittest.TestCase):

    def setUp(self):
        question1 = Question(statement=' what is THE correct answer???   ',
                             answers=['the First one', 'this one', 'no, its this one!', 'definitely this one'],
                             correct_answer='this one')
        question2 = Question(statement=' and the response to,,  this ONE?',
                             answers=['A  ', ' B', ' C', '   ==D'],
                             correct_answer=' B')
        self.questionnaire = Questionnaire(questions=[question1, question2])

    def test_basic_processors(self):
        processor = processors.BasicProcessor(questionnaire=self.questionnaire)
        processor.process()
        self.assertEqual(self.questionnaire.questions[0].statement, 'what is THE correct answer')
        self.assertEqual(self.questionnaire.questions[1].statement, 'and the response to this ONE')

    def test_tfidf_processor(self):
        processor = processors.TfIdfProcessor(questionnaire=self.questionnaire,
                                              corpus_frequency_threshold=0.66)
        processor.process()
        self.assertEqual(processor.stopwords, ['the'])
        self.assertEqual(self.questionnaire.questions[0].statement, ' what is correct answer???   ')
        self.assertEqual(self.questionnaire.questions[1].statement, ' and response to,,  this ONE?')


if __name__ == '__main__':
    unittest.main()
