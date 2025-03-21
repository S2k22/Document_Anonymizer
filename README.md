# Document Anonymizer

## About the tool
This program is a POC for the document anonymizer tool. It labels sensitive/confidential data according to the category and switches the value of it to a category label. It consist of two pre trained models in English and Hungarian.  
The Hungarian version of a tool uses a community pretrained model, to use it u need to instal it first, more information can be found in the instalation part.

## Try it out right now !

https://document-anonymizer.streamlit.app/


## Installation
To get started using the tool, first, we need to download one of the models. The easiest way to achieve this is to install huspacy (from PyPI) and then fetch a model through its API. 
````
Pip install huspacy
import hu_core_news_lg
nlp = hu_core_news_lg.load(
````
We also need to instal SpaCy, an open-source Natural Language Processing (NLP) library used for advanced tasks in the NLP field.
````
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
````
And lastly we need python-docx, it is a Python library for reading, creating, and updating Microsoft Word 2007+ (.docx) files.
````
pip install python-docx
````
## How it works
The tool uses pretrained SpaCy model, it includes pre-trained components (like tokenization, POS tagging, and standard named entity recognition) in combination with entite rules that allows it to define custom patterns for entity recognition. Patterns are a sequence of token specifications using regular expressions. It is used to match necesary patterns for country codes(phone numbers), separators (bank card numbers), and digit groups(ID numbers), etc.. 
> [!NOTE]
> By placing it before the built-in NER, custom patterns are prioritized over the model’s default entity recognition.

The text is processed to create a doc object containing recognized entities. For every entity in doc.ents, the function checks if the entity’s label is in allowed_labels. It appends the text between the previous entity and the current one and replaces the entity text with a placeholder in the form [ENTITY_LABEL] (for example, [EMAIL]). After processing all entities, any remaining text is appended, and the segments are joined back together. The paragraph text is replaced with its anonymized version and the modified document is saved to the specified output path.

# Results
## Original Text 
![image](https://github.com/user-attachments/assets/ca33ed5d-e17d-4b48-9e49-591d2153047d)

## Anonymized Text

![image](https://github.com/user-attachments/assets/e51bc683-a437-4267-a904-8e3b8efb97a7)










