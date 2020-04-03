from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:8111')


class Anaphora:
    def __init__(self):
        pass

    def resolve(self, corenlp_output, text):
        """ Transfer the word form of the antecedent to its associated pronominal anaphor(s) """
        try:
            for coref in corenlp_output['corefs']:
                mentions = corenlp_output['corefs'][coref]
                # the antecedent is the first mention in the coreference chain
                antecedent = mentions[0]
                for j in range(1, len(mentions)):
                    mention = mentions[j]
                    if mention['type'] == 'PRONOMINAL':
                        # get the attributes of the target mention in the corresponding sentence
                        target_sentence = mention['sentNum']
                        target_token = mention['startIndex'] - 1
                        # transfer the antecedent's word form to the appropriate token in the sentence
                        corenlp_output['sentences'][target_sentence -
                                                    1]['tokens'][target_token]['word'] = antecedent['text']
        except TypeError:
            return text

    def print_resolved(self, corenlp_output, text):
        """ Print the "resolved" output """
        try:
            output_sentence = ""
            possessives = ['hers', 'his', 'their', 'theirs']
            for sentence in corenlp_output['sentences']:
                for token in sentence['tokens']:
                    output_word = token['word']
                    # check lemmas as well as tags for possessive pronouns in case of tagging errors
                    if token['lemma'] in possessives or token['pos'] == 'PRP$':
                        output_word += "'s"  # add the possessive morpheme
                    output_word += token['after']
                    output_sentence += output_word
            return(output_sentence)
        except TypeError:
            return text

    def main(self, text):
        output = nlp.annotate(text, properties={
            'annotators': 'dcoref', 'outputFormat': 'json', 'ner.useSUTime': 'false'})

        self.resolve(output, text)
        output_resolved = self.print_resolved(output, text)
        try:
            output_resolved = output_resolved.replace("-LRB-", "(")
            output_resolved = output_resolved.replace("-RRB-", ")")
        except:
            pass
        return output_resolved
