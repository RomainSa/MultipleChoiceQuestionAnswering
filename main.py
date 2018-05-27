from MCQA import Questionnaire
from processors import BasicProcessor, TfIdfProcessor
from solvers import GoogleSolver


# load our data file as a Questionnaire
questionnaire = Questionnaire()
questionnaire.parse(path='data/general.txt', format='open_trivia')
question = questionnaire.questions[0]
print(question.statement)

# process data by removing stopwords
processor = BasicProcessor(questionnaire=questionnaire)
processor.process()
print(question.statement)
processor = TfIdfProcessor(questionnaire=questionnaire)
processor.process()
print(question.statement)

# solver corresponding Questionnaire and print precision
solver = GoogleSolver(question)
answer = solver.answer()
answer == question.correct_answer
