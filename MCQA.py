"""
Data structure that handle questions
"""


class Questionnaire:

    """
    A list of parsed Questions
    """

    def __init__(self, questions=None):
        self.questions = questions

    def parse(self, path, format='open_trivia'):
        """
        :param path: file path
        :type path: str
        :param format: file format (possible values: 'open_trivia')
        :type format: str
        :return:
        """
        self.questions = []
        if format == 'open_trivia':
            # open trivia format - url: https://github.com/uberspot/OpenTriviaQA

            # read input file
            with open(path, 'r', encoding='latin-1') as f:
                lines = f.readlines()

            # format parameters
            d = {'A': 2, 'B': 3, 'C': 4, 'D': 5}
            current_question_data = ['', None, None, None, None, None]
            mode = None

            # parsing
            for line in lines:
                if line != '\n':

                    # mode
                    if line[:2] == '#Q':
                        if mode == 'A':
                            # previously was collecting an answer
                            current_question = Question(statement=current_question_data[0],
                                                        answers=current_question_data[2:],
                                                        correct_answer=current_question_data[1])
                            self.questions.append(current_question)
                            current_question_data = ['', None, None, None, None, None]
                        mode = 'Q'
                    elif line[:2] in ['^ ', 'A ', 'B ', 'C ', 'D ']:
                        mode = 'A'

                    # action
                    if mode == 'Q':
                        # questions
                        current_question_data[0] += line.replace('#Q', '').replace('\n', '')
                    elif mode == 'A':
                        if line[:2] == '^ ':
                            # correct answer
                            current_question_data[1] = line[2:].replace('^ ', '').replace('\n', '')
                        else:
                            # answer
                            current_question_data[d[line[0]]] = line[2:].replace('\n', '')
        else:
            raise ValueError('Unknown format %s' % format)


class Question:

    """
    A Multiple choice question
    """

    def __init__(self, statement, answers, correct_answer):
        """
        :param statement: question statement
        :type statement: str
        :param answers: questions answers
        :type answers: list
        :param correct_answer: correct question answer
        :type correct_answer: str
        """

        # checks on data
        assert correct_answer in answers

        # data fill
        self.statement = statement
        self.answers = answers
        self.correct_answer = correct_answer

    def __str__(self):
        str_ = '\n'.join(["[QUESTION]", self.statement] + ["[ANSWERS]"] +
                         [q if q != self.correct_answer else q + " (CORRECT)" for q in self.answers if q is not None])
        return str_ + '\n'

    def as_text(self):
        """
        Returns the full text of the question (statement and answers) in a single string

        :return: str
        """
        return ' '.join([self.statement] + self.answers)
