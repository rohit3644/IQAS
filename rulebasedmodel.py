# RuleBasedModel class contains a constructor and rule_based_model function
# rule_based_model function is used to find answer within the search text
# based on the type of question tag present in the user query


class RuleBasedModel:
    # constructor
    def __init__(self):
        pass

    # user-defined rule_based_model function
    def rule_based_model(self, ques_tag, query_ner, search_text_ner, search_text, list_ques_tag, links, query):
        # list to store final answer
        answer_array = []
        answer = ""
        # Case-1: if the query contains 'who' or 'whom' question tag
        if ((ques_tag == 'who' or ques_tag == 'Who' or ques_tag == 'whom' or ques_tag == 'Whom')):
            # if the query contains a person name
            # flag becomes true
            person_flag = False
            for i in query_ner.ents:
                if(i.label_ == 'PERSON'):
                    person_flag = True
            # if query contains a persons name
            # print all the relevant search text
            # sentences as answer
            # Eg, Who is Narendra Modi?
            if(person_flag == True):
                answer = search_text

            else:
                for i in search_text_ner.ents:
                    if(i.label_ == 'PERSON' and i.text not in answer_array):
                        answer_array.append(i.text)
                # if query contains only a single
                # person, organization or gpe
                if(len(answer_array) == 1):
                    answer = answer_array[0]
                else:
                    answer = search_text

        # Case-2: if the query contains 'when' question tag
        elif ((ques_tag == 'when' or ques_tag == 'When')):
            for i in search_text_ner.ents:
                # if there is a sentence containing date
                # and that sentence is not present in answer_array
                if(i.label_ == 'DATE' and i.text not in answer_array):
                    answer_array.append(i.text)
            # if query contains only a single date
            if(len(answer_array) == 1):
                answer = answer_array[0]
            else:
                answer = search_text

        # Case-3: if the query contains 'where' question tag
        elif ((ques_tag == 'where' or ques_tag == 'Where')):
            for i in search_text_ner.ents:
                for j in query_ner.ents:
                    # if there is a sentence containing GPE and
                    # GPE present in query is not same as that present
                    # in the search_text sentence and sentence is not present
                    # in answer_array
                    if(i.label_ == 'GPE' and i.text != j.text and i.text not in answer_array):
                        answer_array.append(i.text)
            # if there is only a single
            # GPE in sentence
            if(len(answer_array) == 1):
                answer = answer_array[0]
            else:
                answer = search_text

        # Case-4: if the query contains 'what' and 'which' question tag
        elif ((ques_tag == 'which' or ques_tag == 'Which' or ques_tag == 'What' or ques_tag == 'what')):
            answer = search_text

        # Case-5: if the query contains 'how' question tag
        elif(ques_tag == 'how' or ques_tag == "How"):
            answer = search_text

        # Case-6: default case
        elif(ques_tag not in list_ques_tag):
            answer = search_text

        # Concating the relevant links
        # along with the answer
        answer += "\n\nNot what you are looking for, try re-framing your question or check these links to know more: "
        for i in links:
            answer += "\n"+i
        # calling the database caching function
        self.database_caching(answer, query)

    # this function is used to store the relevant answer
    # in database according to the user feedback
    def database_caching(self, answer, query):
        # Answers of such query change frequently
        # so no need to store such answers in database
        # Eg-: What is the petrol price today in Bhubaneswar?
        if "Today" in query or "Yesterday" in query or "Price" in query:
            print("Answer: ", answer)
        else:

            # Importing Database class
            from database import Database

            feedback = ""
            # Final Answer(including links)
            print("Answer:", answer)
            print("\n\nAre you satisfied with the answer?\n ")
            response = input("Press Y fo Yes and N for No:")
            if response in ['Yes', 'yes', 'y', 'Y']:
                feedback = "Thank you for your valuable feedback"
                # Find the caching value from the keyword
                value = self.caching_value(query)
                database_object = Database()
                # calling main function in Database class
                database_object.main(value, answer)
            elif response in ['No', 'no', 'n', 'N']:
                feedback = "Please try reframing your query once if you are not satisfied"
            print(feedback)

    # this method is used to generate a
    # unique caching value based on the
    # user query

    def caching_value(self, keyword):
        keyword_list = keyword.split()
        value = 0
        for i in keyword_list:
            for j in i:
                value += ord(j)
        return value
