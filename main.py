from MCQA.data import Questionnaire
from MCQA.processors import BasicProcessor, TfIdfProcessor
from MCQA.solvers import GoogleSolver


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
if answer == question.correct_answer:
    print('This is the correct answer')
else:
    print('This is NOT the correct answer')
