import csv
import os
import random
import sys
from retry import retry

from openai import OpenAI, APIConnectionError


def write_csv_row(strings):
    writer = csv.writer(
        sys.stdout, delimiter="\t"
    )
    writer.writerow(strings)
    # flush stdout to prevent buffering
    sys.stdout.flush()


# Get OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    )

client = OpenAI(api_key=api_key, timeout=600)


@retry(APIConnectionError, tries=3, delay=5, backoff=2)
def generate(topic, language_1):
    completion = client.chat.completions.create(
        model="gpt-4",
        timeout=600,

        messages=[
            {
                "role": "system",
                "content": f"""
Generate a unique, intellegent {language_1} phrase on the topic: "{topic}" along with its English translation. Ensure that the phrase includes at least one of the top 1000 frequent {language_1} words.

For each significant {language_1} word in the phrase, provide a single sentence description that includes:
- Part of Speech (e.g., noun, verb, adjective)
- Gender (masculine, feminine, or neuter) for nouns and adjectives, if applicable in {language_1}. Omit this info if the word is not gendered.
- Definition of the {language_1} word
- Root Verb, if applicable
- Concise etymology. From Latin, Greek, or whatever parent language. If applicable or omit this line if the word is not derived from another language.

Description notes should be concise, and focus primarily on the {language_1} word's meaning and usage. The response should be written in English, but may include {language_1} words if necessary. 

==Begin Spanish Example==
I always eat before sleeping.
Siempre como antes de dormir.

**Siempre**: Adverb; meaning "always" or "ever"; from Latin "semper."

**Como**: Verb, 1st person singular present; meaning "I eat"; root "Comer," from Latin "comedere."

**Antes de**: Preposition; meaning "before"; combination of "Antes" (from Latin "ante") and "de" (from Latin "de," indicating origin, separation, or derivation).

**Dormir**: Verb; meaning "to sleep"; from Latin "dormire."
==End Example==

Include the {language_1} root if applicable, specify gender for gendered words, and add interesting etymological details about the word. Avoid including etymology for overly simple words like "and", "the" or common verbs like "to be" or "to have".
""",
            },
            {
                "role": "user",
                "content": f"Return a single result in the format:\n<English phrase>\n<{language_1} translation>\n<multiline grammer note>",
            },
        ],
        temperature=1,
        seed=random.randint(0, 100000),
    )

    response = completion.choices[0].message.content.strip()
    
    # Split response into English phrase,  translation, and grammar note
    response = response.split("\n")
    try:
        english_phrase = response[0]
        translation = response[1]
        grammar_note = "\n".join(response[2:])
        return [english_phrase, translation, grammar_note]
    except IndexError:
        print(response)
        raise


if __name__ == "__main__":
    import logging
    logging.basicConfig()

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--topic",
        help="Topic you want to generate questions and answers for",
    )
    parser.add_argument(
        "-l",
        "--language",
        help="Language you want to generate questions and answers for",
    )

    parser.add_argument(
        "-s", "--size", help="The number of questions and answers you want to generate"
    )
    args = parser.parse_args()

    topic = args.topic
    size = args.size
    language = args.language
    for i in range(int(size)):
        phrase_info = generate(topic, language)
        write_csv_row(phrase_info)
