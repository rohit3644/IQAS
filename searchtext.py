import spacy
import en_core_web_lg

import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spacy.lang.en import English

nlp = en_core_web_lg.load()
ps = PorterStemmer()


class SearchText:
    def __init__(self):
        pass

    def searching_text(self, query, file_content, query_ner, ques_tag, list_ques_tag):
        # Splitting the file content into sentences
        list_file_content = self.sentence_split(file_content)
        universal = ""
        # For who question type
        if ((ques_tag == 'who' or ques_tag == 'Who' or ques_tag == 'whom' or ques_tag == 'Whom')):
            l = []
            file_content1 = ""
            l1 = ['current', 'ongoing', 'latest', 'today']
            date = []
            date_flag = False
            for i in query_ner.ents:
                if(i.label_ == 'DATE'):
                    date.append(i.text)
                    date_flag = True
            if(date_flag):
                for i in date:
                    for k in range(len(list_file_content)):
                        if(i in list_file_content[k] and list_file_content[k] not in file_content1):
                            # print("Found in text: ",i)
                            file_content1 += list_file_content[k] + " "
            else:
                for i in l1:
                    for k in range(len(list_file_content)):
                        if((i in list_file_content[k]) or (i.capitalize() in list_file_content[k]) and list_file_content[k] not in file_content1):
                            # print("Found in text: ",i)
                            file_content1 += list_file_content[k] + " "
            k = 0
            if(file_content1 == ""):
                for i in query.split():
                    for k in range(len(list_file_content)):
                        x = i.lower()
                        if ((i in list_file_content[k]) or (x in list_file_content[k]) or (ps.stem(i) in list_file_content[k]) or
                                (ps.stem(x) in list_file_content[k])) and k not in l and list_file_content[k] not in universal:
                            l.append(k)
                            universal += list_file_content[k] + " "
            else:
                for i in query.split():
                    for k in range(len(list_file_content)):
                        x = i.lower()
                        if ((i in list_file_content[k]) or (x in list_file_content[k])) and k not in l and list_file_content[k] not in universal:
                            l.append(k)
                            universal += list_file_content[k] + " "

                list_file_content1 = self.sentence_split(file_content1)

                for i in list_file_content1:
                    if i not in universal:
                        universal += i

        # For when question tags
        elif ((ques_tag == 'when' or ques_tag == 'When')):
            l = []
            relevant_string = ""
            for i in query.split():
                for j in range(len(list_file_content)):
                    if(((i in list_file_content[j]) or (i.lower() in list_file_content[j])) and j not in l and list_file_content[j] not in relevant_string):
                        l.append(j)
                        relevant_string += list_file_content[j] + " "
            # print("relevant string: ", relevantString)
            relevant_string_array = self.sentence_split(relevant_string)

            for i in relevant_string_array:
                x = nlp(i)
                for j in x.ents:
                    if(j.label_ == 'DATE' or j.label_ == 'ORDINAL'):
                        universal += i
                        break

        # For where type of questions
        elif(ques_tag == 'where' or ques_tag == 'Where'):
            l = []
            relevant_string = ""
            for i in query.split():
                for j in range(len(list_file_content)):
                    if(((i in list_file_content[j]) or (i.lower() in list_file_content[j])) and j not in l and list_file_content[j] not in relevant_string):
                        l.append(j)
                        relevant_string += list_file_content[j] + " "

            relevant_string_array = self.sentence_split(relevant_string)

            for i in relevant_string_array:
                x = nlp(i)
                for j in x.ents:
                    if(j.label_ == 'GPE'):
                        universal += i
                        break

        # For which and what type of question
        elif(ques_tag == 'which' or ques_tag == 'Which' or ques_tag == 'What' or ques_tag == 'what'):
            l = []
            for i in query.split():
                for j in range(len(list_file_content)):
                    if(((i in list_file_content[j]) or (i.lower() in list_file_content[j])) and j not in l and list_file_content[j] not in universal):
                        l.append(j)
                        universal += list_file_content[j] + " "

        # For how and default case
        elif(ques_tag == 'how' or ques_tag == "How" or ques_tag not in list_ques_tag):
            l = []
            for i in query.split():
                for j in range(len(list_file_content)):
                    if(((i in list_file_content[j]) or (i.lower() in list_file_content[j])) and j not in l and list_file_content[j] not in universal):
                        l.append(j)
                        universal += list_file_content[j] + " "
        return universal

    def sentence_split(self, sentence):
        nlp_sentence = English()
        nlp_sentence.add_pipe(nlp_sentence.create_pipe('sentencizer'))
        doc = nlp_sentence(sentence)
        sentence_list = [sent.string.strip() for sent in doc.sents]
        return sentence_list

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
            dic.__setitem__(i, count)

        maximum = -1
        for k in dic.values():
            if k > maximum:
                maximum = k
        final_string = ""
        for k in dic:
            if(dic[k] == maximum):
                final_string += string_array[k]+" "
        return final_string
