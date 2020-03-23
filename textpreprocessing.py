class TextPreprocessing:
    def __init__(self):
        pass

    def question_tag(self, query):
        ques_tag = ""
        list_ques_tag = ['what', 'What', 'who', 'Who', 'when', 'When',
                         'where', 'Where', 'which', 'Which', 'how', 'How', 'Whom', 'whom']
        regex = re.findall(r"\b[wW]h\w+|how|How", query)
        for i in regex:
            ques_tag += i
        return ques_tag, list_ques_tag

    # This function is used for punctuation removal,
    # Wh-question removal, stop-word removal and,
    # capitalizing words in the user query

    def stop_word(self, query):
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
