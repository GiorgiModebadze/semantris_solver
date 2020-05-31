from argparse import ArgumentParser
from models.custom_model_generator import create_custom_model
from models.model_2 import run_model as run_model_2
from models.model_1 import run_model as run_model_1

'''
    We started with model 1 using the api calls to get synonyms each time
    Model 2 is improvment which utilizes spacy to generate connections between words
'''

parser = ArgumentParser()

# Allow users to choose between
# As the default choosing 1 as it does not require creation of custom model
parser.add_argument("-m", "--model", dest="model", default='1',
                    help="1 or 2. For More Information see README.md")

args = parser.parse_args()

model_name = 'custom_model'
base_score = 0.3

if __name__ == '__main__':

    if args.model == '2':
        create_custom_model(base_score, model_name)
        run_model_2(model_name)
    else:
        run_model_1()
