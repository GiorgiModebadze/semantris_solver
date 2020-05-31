import spacy
import json
from tqdm import tqdm

nlp = spacy.load('en_core_web_lg')

base_words = []

# Load words into list
with open("Input words.txt", "rb") as f:
    for i in json.loads(f.read())[5]:
        base_words.append(i[0])


def create_custom_model(min_score = 0.3, file_name = 'custom_model'):
    # List of words with semantically similar words
    word_list = []

    # Words for which semantically similar words cant be found
    missing_words = []

    # How similar words shall be

    # For each word goes through the list once again and using spacy`s simialirty method
    # Creates list of semantically similar words using Word and score structure

    # For better understanding of where the process is
    print(f"There is {len(base_words)} words to be processed")

    # Using tqdm module to show progress bar
    for i in tqdm(base_words):
        main_word = nlp(i)
        similars = []

        for j in base_words:
            compare_word = nlp(j)
            score = main_word.similarity(compare_word)

            if score > min_score and i != j:
                similars.append({
                    "word": j,
                    "score": score
                })

        curr_val = {
            i: similars
        }

        word_list.append(curr_val)

        # If we missed words we save it as we need to find similar words for it nevertheless
        if len(similars) == 0:
            missing_words.append(i)
            print("Nothing Found For", i)

    with open(f'{file_name}.json', 'w') as fout:
        json.dump(word_list, fout)

    print(missing_words)
