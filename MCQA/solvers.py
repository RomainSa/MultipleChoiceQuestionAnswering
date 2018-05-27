"""
Question solvers
"""

import pickle
import os
import re
from zlib import adler32

import requests
from bs4 import BeautifulSoup
import numpy as np


class GoogleSolver:

    """
    Solver based on Google search engine results
    """

    def __init__(self, question):
        # static parameters
        self.plus_code = '%2B'
        self.base_url = 'https://www.google.com/search?safe=off&q=%s'
        self.cache_folder = 'data/cache/'

        # data
        self.question = question
        self.search_results = []
        self.n_search_results = []

    @staticmethod
    def _get_n_search_results(soup):
        """
        Extract the number of search results in a result page

        :param soup: html soup
        :type soup: bs4.BeautifulSoup
        :return: number of Google results
        :rtype: int
        """
        return int(re.search('(\d+)', soup.select("#resultStats")[0].text).group(0))

    def _get_search_results(self):
        """
        Scrap Google search results

        :return: Nothing
        """
        # try to retrieve it from cache if it exists
        question_treated = self.question.statement
        question_file = self.cache_folder + str(adler32(str.encode(self.question.statement))) + '.pkl'

        if os.path.isfile(question_file):
            # used cached data
            with open(question_file, 'rb') as f:
                cached = pickle.load(f)
            self.search_results = [BeautifulSoup(s, 'html.parser') for s in cached]

        else:
            # use Google search
            cached = []
            for answer in self.question.answers:
                query = '+'.join(self.plus_code + a for a in (question_treated + ' ' + answer).lower().split(' '))
                url = self.base_url % query
                r = requests.get(url)
                cached.append(r.text)
                soup = BeautifulSoup(r.text, 'html.parser')
                self.search_results.append(soup)

            # save it in cache
            with open(question_file, 'wb') as f:
                pickle.dump(cached, f)

    def answer(self):
        """
        Answer a multiple choice question

        :return:
        :rtype: str
        """
        # crawl Google search results
        self._get_search_results()

        # get number of search results
        for search_result in self.search_results:
            self.n_search_results.append(self._get_n_search_results(search_result))

        # return answer with the most search results
        return self.question.answers[np.argmax(self.n_search_results)]
