import re
import openai
import json

# openai.api_key = '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' # free acc
openai.api_key = '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'
 
def get_list_of_words(text):
    list_of_words = re.split(r'[^a-zA-Z0-9]+', text.lower())
    return list_of_words
    
 
def chat_with_gpt(user_input, model="gpt-3.5-turbo-1106", temperature=0.2):
    conversation = [{"role": "user", "content": user_input}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation,
        temperature=temperature
    )
    assistant_reply = response.choices[0].message["content"]
    return assistant_reply


def get_plain_phrases(text):
    user_input = f"""
I want to break a text into phrases. Please read the requirements, example and the text respectively below carefully:

Requirements:
1. Your reply MUST BE in JSON FORMAT and DIRECTLY CONVERTIBLE into a DICTIONARY (in PYTHON) through an AUTOMATED PROCESS. It MUST CONTAIN EXACTLY (NEITHER MORE NOR LESS) ONE ARRAY named 'phrases' as follows: {{"phrases": ["phrase1", "phrase2", "phrase3", ...]}}
2. Try to include ALL POSSIBLE, POTENTIAL phrases including one-word phrases, full-sentence phrases, and everything in between. These phrases can overlap, share one or more word(s) with each other.

Example:
Sample text: "The cat sat on the mat"
THE CORRECT sample reply: {{"phrases": ["cat", "sat", "mat", "The cat", "cat sat", "sat on", "the mat", "The cat sat", "on the mat", "sat on the mat", "The cat sat on the mat"]}}
A WRONG sample reply: Absolutely, here's the answer: {{"phrases": ["The cat", "on the mat"]}}. It has two phrases.

Text:
{text}
"""
    plain_phrases = chat_with_gpt(user_input).lower()
    return plain_phrases
    
    
def get_list_of_phrases_gpt(text):
    plain_phrases = get_plain_phrases(text)
    # Find all sequences starting with '{' and ending with '}'
    pattern = r'{[^{}]*}'
    matches = re.findall(pattern, plain_phrases)
    # Sort matches by length (longest first)
    matches.sort(key=len, reverse=True)
    # Attempt to convert each match to a dictionary
    for match in matches:
        try:
            json_dict = json.loads(match)
            for item in json_dict.values():
                if isinstance(item, list):
                    return item # Return the parsed dictionary if successful
        except json.JSONDecodeError:
            pass  # Continue if parsing fails

    return []  # Return None if no valid JSON dictionary found


def process_and_enrich(job_post_list):
    for i in range(len(job_post_list)):
        print(f"Processing & enriching job post {i+1}")
        title = job_post_list[i]["title"]
        description = job_post_list[i]["description"]
        
        job_post_list[i]["title_words"] = get_list_of_words(title)
        job_post_list[i]["description_words"] = get_list_of_words(description)
        
        # job_post_list[i]["title_phrases_gpt"] = get_list_of_phrases_gpt(title)
        # job_post_list[i]["description_phrases_gpt"] = get_list_of_phrases_gpt(description)
        
        if "employer_questions" in job_post_list[i]:            
            job_post_list[i]["employer_questions"] = [question["question"] for question in job_post_list[i]["employer_questions"]]
            employer_questions = " ".join(job_post_list[i]["employer_questions"])
            
            job_post_list[i]["employer_questions_words"] = get_list_of_words(employer_questions)
        #     job_post_list[i]["employer_questions_phrases_gpt"] = get_list_of_phrases_gpt(employer_questions)
        


# import re

# def break_into_sentences(text):
#     # Define the regex pattern for splitting sentences based on punctuation marks and line breaks
#     sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n)\s'
#     # sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\,|\:|\;|\n)\s'
#     # sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\:|\n|\-|\"|\'|\(|\)|\[|\]|\{|\})\s'
    
#     # Split the text into sentences using the pattern
#     list_of_sentences = re.split(sentence_pattern, text.lower())
#     a
#     for i in range(len(list_of_sentences)):
#         # Replace non-alphabetic characters with a space
#         list_of_sentences[i] = re.sub(r'[^a-zA-Z]', ' ', list_of_sentences[i])
#         # Collapse multiple spaces into a single space
#         list_of_sentences[i] = re.sub(r'\s+', ' ', list_of_sentences[i])
#     return list_of_sentences


# def get_n_word_phrase(list_of_words, n):
#     # Create sublists of size 'n' using list comprehension
#     consecutive_groups = [list_of_words[i:i+n] for i in range(len(list_of_words) - n + 1)]
    
#     # Join the inner elements of each sublist with a space
#     list_of_phrases = [' '.join(map(str, group)) for group in consecutive_groups]
    
#     return list_of_phrases


# def get_list_of_phrases(list_of_sentences):
#     list_of_phrases = list_of_sentences
#     for sentence in list_of_sentences:
#         list_of_words = sentence.split()
#         for i in range(len(list_of_words)-1):
#             list_of_phrases += get_n_word_phrase(list_of_words, i+1)

# # n + n-1 + n-2 + ... + 1 = n(n+1)/2


# def extract_list_string(input_text):
#     pattern = r'\[[^\[\]]*\]'
#     matches = re.findall(pattern, input_text)
    
#     # Sort matches by length (longest first)
#     matches.sort(key=len, reverse=True)
    
#     # Filter and return the first valid list-like string
#     for match in matches:
#         try:
#             eval_result = eval(match)  # Try evaluating the match
#             if isinstance(eval_result, list):
#                 return eval_result
#         except Exception:
#             pass  # Continue if evaluation fails or not a list

#     return None  # Return None if no valid list-like string found
