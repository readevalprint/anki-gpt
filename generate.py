import csv
import os
import random
import sys
from retry import retry

from openai import OpenAI, APIConnectionError


def write_csv_row(strings):
    writer = csv.writer(
        sys.stdout, delimiter="|"
    )
    writer.writerow(strings)


# Get OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    )

client = OpenAI(api_key=api_key, timeout=60)


@retry(APIConnectionError, tries=3, delay=5, backoff=2)
def generate(topic):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"""Generate a very unique, simple, and intelligent Spanish phrase about the topic: "{topic}"  and its English translation. Pick 1 of the top 1000 frequent Spanish words to include in the phrase. 

For each important spanish part of speech make one single concise line. Must include spanish root verb if needed. Masc or fem. And basic etymology"

==Begin Example==
I always eat before sleeping
Siempre como antes de dormir

**Siempre**: Adverb, Latin "semper," meaning "always" or "ever."

**como**: Verb, 1st person singular, Latin "quomodo," which translates to "in what manner" or "how.

**antes de**: Preposition, from Latin "ante," meaning "before") and "de" (from Latin "de," a preposition indicating origin, separation, or derivation

**dormir**: Verb, Latin "dormire," which also means "to sleep.
==End Example==
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
