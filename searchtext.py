import nltk
from nltk.stem import PorterStemmer
from spacy.lang.en import English
ps = PorterStemmer()
# SearchText class contains a constructor and searching_text function,
# sentence_split function and relevant sentence function
# searching_text function is used to search relevant sentences
# based on keywords in the query, sentence_split function splits the
# sentence to make a list pf sentences and relevant_sentence function
# is used to search sentences with maximum keyword density


class SearchText:
    # constructor
    def __init__(self):
        pass

    # this function is used to search all the relevant sentence
    # atleast a keyword in query
    def search_all_keyword(self, length, query_array, list_file_content, l, universal):
        for i in range(length):
            for k in query_array:
                x = k.lower()
                y = ps.stem(k)
                if((k in list_file_content[i]) or (x in list_file_content[i]) or (y in list_file_content[i]) or
                        (y.capitalize() in list_file_content[i])) and i not in l and list_file_content[i] not in universal:
                    l.append(i)
                    universal += list_file_content[i] + " "
        return universal

    # user-defined searching_text function
    # used to search relevant text based on user query
    # returns a string of relevant sentences
    def searching_text(self, query, file_content, query_ner, ques_tag, list_ques_tag):
        # importing third-party libraries
        import spacy
        import en_core_web_lg
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        nlp = en_core_web_lg.load()

        # Anaphora/Reference resolution
        from anaphora import Anaphora
        anaphora_object = Anaphora()
        file_content = anaphora_object.main(file_content)

        # Splitting the file content into sentences
        list_file_content = self.sentence_split(file_content)
        length = len(list_file_content)
        query_array = query.split()
        l = []
        # final string of relevant sentences
        universal = ""
        # For who question type
        if ((ques_tag == 'who' or ques_tag == 'Who' or ques_tag == 'whom' or ques_tag == 'Whom')):
            relevant_string = ""
            relevant_string = self.search_all_keyword(
                length, query_array, list_file_content, l, relevant_string)

            relevant_string_array = self.sentence_split(relevant_string)

            for i in relevant_string_array:
                x = nlp(i)
                for j in x.ents:
                    # getting the sentences containing date or ordinal
                    if(j.label_ == 'PERSON'):
                        universal += i
                        break

            if universal == "":
                universal = relevant_string

        # For when question tags
        elif ((ques_tag == 'when' or ques_tag == 'When')):
            relevant_string = ""
            relevant_string = self.search_all_keyword(
                length, query_array, list_file_content, l, relevant_string)

            relevant_string_array = self.sentence_split(relevant_string)

            for i in relevant_string_array:
                x = nlp(i)
                for j in x.ents:
                    # getting the sentences containing date or ordinal
                    if(j.label_ == 'DATE'):
                        universal += i
                        break

            if universal == "":
                universal = relevant_string

        # For where type of questions
        elif(ques_tag == 'where' or ques_tag == 'Where'):
            relevant_string = ""
            relevant_string = self.search_all_keyword(
                length, query_array, list_file_content, l, relevant_string)

            relevant_string_array = self.sentence_split(relevant_string)

            # getting the sentences containing GPE
            for i in relevant_string_array:
                x = nlp(i)
                for j in x.ents:
                    if(j.label_ == 'GPE'):
                        universal += i
                        break
            if universal == "":
                universal = relevant_string

        # For which and what type of question
        elif(ques_tag == 'which' or ques_tag == 'Which' or ques_tag == 'What' or ques_tag == 'what'):
            universal = self.search_all_keyword(
                length, query_array, list_file_content, l, universal)

        # For how and default case
        elif(ques_tag == 'how' or ques_tag == "How" or ques_tag not in list_ques_tag):
            universal = self.search_all_keyword(
                length, query_array, list_file_content, l, universal)

        return universal

    # user-defined sentence_split function
    # used to split sentences
    # return a list of sentences
    def sentence_split(self, sentence):
        nlp_sentence = English()
        nlp_sentence.add_pipe(nlp_sentence.create_pipe('sentencizer'))
        doc = nlp_sentence(sentence)
        sentence_list = [sent.string.strip() for sent in doc.sents]
        return sentence_list

    # user-defined relevant_sentence function
    # used to search sentences with highest density
    # of keywords, returns sentences with maximum keywords
    def relevant_sentence(self, keywords, string):
        keywords_array = keywords.split()
        string_array = self.sentence_split(string)
        dic = {}
        length = len(string_array)
        for i in range(length):
            count = 0
            for j in keywords_array:
                if(j.lower() in string_array[i] or j in string_array[i] or j.upper() in string_array[i] or ps.stem(j) in string_array[i]):
                    count += 1
            # insert index and count of keywords in each sentence
            dic.__setitem__(i, count)

        maximum = -1
        # getting the maximum value from the dictionary
        for k in dic.values():
            if k > maximum:
                maximum = k
        final_string = ""
        for k in dic:
            # getting the sentence with maximum keywords
            if(dic[k] == maximum):
                final_string += string_array[k]+" "
        return final_string
