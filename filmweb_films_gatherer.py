import io
import sys
import default_logger
from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from copy import copy

DEBUG_FILE_WITH_FILMWEB_SEARCH_RESULT = "netflix_films_from_filmweb.html"
DEFAULT_FILM = {'title': None,
                'year': None,
                'duration': None,
                'director': None,
                'genre': None,
                'country': None,
                'netflix_handling': None}


def netflix_finder(film_name):
    logger = default_logger.logger_creation(name='filmweb')
    try:
        list_of_films = []
        list_of_netflix_films = []
        film_cards = soup_initialization(film_name)

        for single_film_card in film_cards:
            film = copy(DEFAULT_FILM)
            filmweb_debug(single_film_card)
            single_film_card = '''{}'''.format(single_film_card)
            div_soup = BeautifulSoup(single_film_card, 'html.parser')
            film['title'] = finding_no_link_structure(div_soup, 'h2', 'filmPreview__title')
            film['year'] = finding_no_link_structure(div_soup, 'div', 'filmPreview__year')
            film['duration'] = finding_no_link_structure(div_soup, 'div', 'filmPreview__filmTime')
            film['director'] = finding_link_structure(div_soup, 'div', 'filmPreview__info filmPreview__info--directors')
            film['genre'] = finding_link_structure(div_soup, 'div', 'filmPreview__info filmPreview__info--genres')
            film['country'] = finding_link_structure(div_soup, 'div', 'filmPreview__info filmPreview__info--countries')
            film['netflix_handling'] = netflix_verification(div_soup)
            list_of_films.append(film)
            if film['netflix_handling']:
                list_of_netflix_films.append(film)
            else:
                continue
        result_logger(film_name, list_of_films, list_of_netflix_films, logger)
        return list_of_netflix_films
    except Exception as Error:
        logger.error("Error during gathering importaion about netflix_handling films: {}.".format(Error))
        sys.exit(1)


def soup_initialization(film_name):
    try:
        film_name_without_spaces = film_name.replace(' ', '%20')
        film_name_without_spaces = quote(film_name_without_spaces)
        url_to_filmweb_search_results = "http://filmweb.pl/search?q=" + film_name_without_spaces
        request_to_filmweb = Request(url_to_filmweb_search_results, headers={'User-Agent': "Magic Browser"})
        response_from_filmweb = urlopen(request_to_filmweb)
        soup = BeautifulSoup(response_from_filmweb, 'html.parser')
        filmCards = soup.find_all('div', class_='filmPreview__card')
        return filmCards
    except Exception as Error:
        logger.error("Error during soup initialization for netflix_handling purpose: {}.".format(Error))
        sys.exit(1)


def filmweb_debug(single_film_card):
    with io.open(DEBUG_FILE_WITH_FILMWEB_SEARCH_RESULT, 'w', encoding='utf-8') as file:
        file.write(100 * '*')
        file.write(str(single_film_card))


def netflix_verification(div_soup):
    if div_soup.find('div', class_="advertButton advertButton--netflix"):
        netflix = div_soup.find('div', class_="advertButton advertButton--netflix")
        netflix = '''{}'''.format(netflix)
        netflix_soup = BeautifulSoup(netflix, 'html.parser')
        netflix_link = netflix_soup.find('a', href=True)
        if netflix_link:
            return netflix_link['href']
        else:
            return None


def finding_no_link_structure(div_soup, tag, class_name):
    if div_soup.find(tag, class_=class_name):
        return div_soup.find(tag, class_=class_name).text


def finding_link_structure(div_soup, tag, class_name):
    if div_soup.find(tag, class_=class_name):
        finding = div_soup.find(tag, class_=class_name)
        finding = '''{}'''.format(finding)
        soup = BeautifulSoup(finding, 'html.parser')
        return soup.find('a').text


def result_logger(film_name, each_films, films_on_netflix, logger):
    #logger = default_logger.logger_creation(name='filmweb')
    for film in each_films:
        logger.debug('Found in filmweb base match with "{}": {}, {}, {}, {}, {}, {}'.format(
            film_name, film['title'], film['year'], film['duration'], film['director'], film['genre'], film['country']))
    for film in films_on_netflix:
        logger.info('Film in Netflix base match with "{}": {}, {}, {}, {}, {}, {}'.format(
            film_name, film['title'], film['year'], film['duration'], film['director'], film['genre'], film['country']))
