import re

# TextPreprocessing class contains a constructor, question_tag function
# and stop_word function, question_tag function detects the type of question
# tag present in the query and stop_word function is used to remove stop words
# from the user query


class TextPreprocessing:
    def __init__(self):
        pass

    # user-defined question_tag function
    # used to detect type of question tag
    # in user query and returns the question tag
    # along with a list containing all possible question tags
    def question_tag(self, query):
        ques_tag = ""
        list_ques_tag = ['what', 'What', 'who', 'Who', 'when', 'When',
                         'where', 'Where', 'which', 'Which', 'how', 'How', 'Whom', 'whom']
        # finding the words starting with 'w' or 'W' in the query
        regex = re.findall(r"\b[wW]h\w+|how|How", query)
        for i in regex:
            ques_tag += i
        return ques_tag, list_ques_tag

    # user-defined stop_word function
    # This function is used for punctuation removal,
    # Wh-question removal, stop-word removal and,
    # capitalizing words in the user query
    # returns a refined query containing no stop words
    def stop_word(self, query):
        # importing third-party libraries
        import string
        import nltk
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from spacy.lang.en import English
        # Punctuation removal
        query = query.translate(str.maketrans('', '', string.punctuation))
        # Wh-question removal
        query_array = query.split()
        reg = re.findall(
            r"\b[wW]h\w+|how|How|define|Define|Explain|explain", query)
        for i in reg:
            if i in query_array:
                query_array.remove(i)
        query = ""
        for i in query_array:
            query += i+" "

        # stop word removal
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(query)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        string_text = ""
        for i in filtered_sentence:
            string_text += i+" "

        # capitalize the words
        query_array = string_text.split()
        output = ""
        for i in query_array:
            i = i.capitalize()
            output += i+" "
        return output
