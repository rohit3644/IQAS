from __future__ import unicode_literals, print_function


# Main class contains a constructor and main function
# main function is used to take user query input,
# Get the web-scraped dynamic content, detect the
# type of question tag, and preprocessing the
# user query, it also calls weather api, search text
# function and finally the rule-based model


class Main:
    # constructor
    def __init__(self):
        pass

    # user-defined main function
    def main(self):
        # importing all the classes
        from webscrape import WebScraping
        from rulebasedmodel import RuleBasedModel
        from searchtext import SearchText
        from textpreprocessing import TextPreprocessing
        from weather import Weather
        from database import Database

        # importing the third- party libraries
        import spacy
        import en_core_web_lg
        nlp = en_core_web_lg.load()
        # objects
        web_scrape_object = WebScraping()
        text_preprocess_object = TextPreprocessing()
        weather_object = Weather()
        search_text_object = SearchText()
        rule_based_object = RuleBasedModel()
        database_object = Database()
        # user query
        query = input("Ask me a Question: ")

        # question tag function is used to find the question-tag
        # in the user query and it returns question-tag and list of
        # all possible question tags
        ques_tag, list_ques_tag = text_preprocess_object.question_tag(query)

        # Stopword function is used to remove stop words
        # from user query and returns the refined query
        query = text_preprocess_object.stop_word(query)
        # Getting the cache value from the keyword
        value = rule_based_object.caching_value(query)
        # Checking if the value exist in the database
        result = database_object.select_query(value)
        if result != None:
            print("Answer: ", result[0])
        else:
            # text_list is a list of text from different websites
            # links is a list of website links
            text_list, links = web_scrape_object.fetch_text_results(query)

            # if text_list is empty
            if not text_list:
                print("Sorry. No data available!")
                return

            # applying named entity recogntion on user query
            query_ner = nlp(query)
            weather_location = ""
            # if any of the below keywords are present in query
            # call weather function
            if "Weather" in query or "Temperature" in query or "Humidity" in query or "Pressure" in query or "Climate" in query:
                for i in query_ner.ents:
                    if(i.label_ == 'GPE'):
                        weather_location = i.text

            if weather_location != "":
                # weather function is used to get the weather details
                # for a particular weather_location
                weather_object.weather(weather_location)
            else:
                search_text = ""
                for i in text_list:
                    # searching text function is used to search
                    # relevant sentences in the entire content
                    # and returns only relevant sentence from the
                    # entire content
                    text = search_text_object.searching_text(
                        query, i, query_ner, ques_tag, list_ques_tag)
                    # check for duplication of search text
                    if(text not in search_text):
                        search_text += text

                # Anaphora/Reference resolution
                from anaphora import Anaphora
                anaphora_object = Anaphora()
                search_text = anaphora_object.main(search_text)
                # relevant_ sentence function is used to find the sentences
                # having highest density of keywords, it returns sentences
                # having maximum keywords in them
                search_text = search_text_object.relevant_sentence(
                    query, search_text)

                # applying named entity recognition on search_text
                search_text_ner = nlp(search_text)

                # Rule based model is used to find answer within the search text
                # it is also used to display the answer
                rule_based_object.rule_based_model(ques_tag, query_ner, search_text_ner,
                                                   search_text, list_ques_tag, links, query)


if __name__ == "__main__":
    # object of Main class
    main_object = Main()
    main_object.main()
