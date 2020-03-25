from __future__ import unicode_literals, print_function
from webscrape import WebScraping
from rulebasedmodel import RuleBasedModel
from searchtext import SearchText
from textpreprocessing import TextPreprocessing
from weather import Weather

import spacy
import en_core_web_lg

nlp = en_core_web_lg.load()


class Main:
    # constructor
    def __init__(self):
        pass

    # main function
    def main(self):
        # objects
        web_scrape_object = WebScraping()
        text_preprocess_object = TextPreprocessing()
        weather_object = Weather()
        search_text_object = SearchText()
        rule_based_object = RuleBasedModel()
        # User query
        query = input("Ask me a Question: ")

        # list of contents from different webpages
        text_list, links = web_scrape_object.fetch_text_results(query)

        if not text_list:
            print("Sorry. No data available!")
            return
        list_query = query.split()

        # Getting question tag from the query
        ques_tag, list_ques_tag = text_preprocess_object.question_tag(query)

        # Removing stopwords and punctuations from query
        query = text_preprocess_object.stop_word(query)

        query_ner = nlp(query)
        weather_location = ""
        # if any keyword is present in query
        if "Weather" in query or "Temperature" in query or "Humidity" in query or "Pressure" in query or "Climate" in query:
            for i in query_ner.ents:
                if(i.label_ == 'GPE'):
                    weather_location = i.text

        if weather_location != "":
            weather_object.weather(weather_location)
        else:
            search_text = ""
            for i in text_list:
                # search text
                text = search_text_object.searching_text(
                    query, i, query_ner, ques_tag, list_ques_tag) + "\n"
                if(text not in search_text):
                    search_text += text

            search_text = search_text_object.relevant_sentence(
                query, search_text)

            search_text_ner = nlp(search_text)

            rule_based_object.rule_based_model(ques_tag, query_ner, search_text_ner,
                                               search_text, list_ques_tag, links)


main_object = Main()
main_object.main()
