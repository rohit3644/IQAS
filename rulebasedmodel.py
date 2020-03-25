class RuleBasedModel:
    def __init__(self):
        pass

    def rule_based_model(self, ques_tag, query_ner, search_text_ner, search_text, list_ques_tag, links):
        answer_array = []

        # For who and whom type of questions
        if ((ques_tag == 'who' or ques_tag == 'Who' or ques_tag == 'whom' or ques_tag == 'Whom')):
            flag = False
            for i in query_ner.ents:
                if(i.label_ == 'PERSON'):
                    flag = True
            if(flag == True):
                print("Answer: ", search_text)
            else:
                for i in search_text_ner.ents:
                    if(i.label_ == 'PERSON' or i.label_ == "ORG" and i.text not in answer_array):
                        answer_array.append(i.text)
                if(len(answer_array) == 1):
                    print("Answer: ", *answer_array)
                else:
                    print("Answer: ", search_text)

        # For 'When' questions
        elif ((ques_tag == 'when' or ques_tag == 'When')):
            for i in search_text_ner.ents:
                if(i.label_ == 'DATE' and i.text not in answer_array):
                    answer_array.append(i.text)
            if(len(answer_array) == 1):
                print("Answer: ", *answer_array)
            else:
                print("Answer: ", search_text)

        # For 'Where' questions
        elif ((ques_tag == 'where' or ques_tag == 'Where')):
            for i in search_text_ner.ents:
                for j in query_ner.ents:
                    if(i.label_ == 'GPE' and i.text != j.text and i.text not in answer_array):
                        answer_array.append(i.text)
            if(len(answer_array) == 1):
                print("Answer: ", *answer_array)
            else:
                print("Answer: ", search_text)

        # For 'What' and 'Which' questions
        elif ((ques_tag == 'which' or ques_tag == 'Which' or ques_tag == 'What' or ques_tag == 'what')):
            print("Answer: ", search_text)

        # For "How" question tag
        elif(ques_tag == 'how' or ques_tag == "How"):
            print("Answer: ", search_text)

        # For Default case
        elif(ques_tag not in list_ques_tag):
            print("Answer: ", search_text)

        print("\nNot what you are looking for, check these links to know more: ")
        for i in links:
            print(i, end="\n")
