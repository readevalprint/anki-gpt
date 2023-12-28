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
def generate(topic):
    completion = client.chat.completions.create(
        model="gpt-4",
        timeout=600,

        messages=[
            {
                "role": "system",
                "content": f"""
Generate a unique, simple, and intelligent Spanish phrase on the topic: "{topic}" along with its English translation. Ensure that the phrase includes at least one of the top 1000 frequent Spanish words.

For each significant Spanish word in the phrase, provide a single sentence description that includes:
- Part of Speech (e.g., noun, verb, adjective)
- Gender (masculine or feminine) for nouns and adjectives, if applicable
- Definition of the Spanish word
- Root Verb, if applicable
- Minimal etymology, if applicable

The response should be concise, educational, and focus primarily on the Spanish word's meaning and usage.

==Begin Example==
I always eat before sleeping.
Siempre como antes de dormir.

**Siempre**: Adverb; meaning "always" or "ever"; from Latin "semper."

**Como**: Verb, 1st person singular present; meaning "I eat"; root "Comer," from Latin "comedere."

**Antes de**: Preposition; meaning "before"; combination of "Antes" (from Latin "ante") and "de" (from Latin "de," indicating origin, separation, or derivation).

**Dormir**: Verb; meaning "to sleep"; from Latin "dormire."
==End Example==

Include the Spanish root if applicable, specify gender for gendered words, and add interesting etymological details about the word. Avoid including etymology for overly simple words like "y" (and) or "el" (the), or common verbs like "ser" (to be) or "tener" (to have).
""",
            },
            {
                "role": "user",
                "content": "Return a single result in the format:\n<English phrase>\n<Spanish translation>\n<multiline grammer note>",
            },
        ],
        temperature=1.2,
        seed=random.randint(0, 100000),
    )

    response = completion.choices[0].message.content.strip()
    
    # Split response into English phrase, Spanish translation, and grammar note
    response = response.split("\n")
    try:
        english_phrase = response[0]
        spanish_translation = response[1]
        grammar_note = "\n".join(response[2:])
        return [english_phrase, spanish_translation, grammar_note]
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
        "-s", "--size", help="The number of questions and answers you want to generate"
    )
    args = parser.parse_args()

    topic = args.topic
    size = args.size
    for i in range(int(size)):
        phrase_info = generate(topic)
        write_csv_row(phrase_info)
