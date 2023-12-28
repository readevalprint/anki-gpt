import argparse
import csv
import random

import genanki
import markdown


def create_anki_deck(input_csv, deck_name, output_file):
    # Create a new Anki deck
    deck = genanki.Deck(89928173198734231, deck_name)  # Randomly generated deck ID

    # Define a model (card type)
    my_model = genanki.Model(
        int(hashlib.sha1(deck_name.encode()).hexdigest(), 16),
        "Simple Model",
        fields=[{"name": "English"}, {"name": "Spanish"}, {"name": "Note"}],
        templates=[
            {
                "name": "English to Spanish",
                "qfmt": "{{English}}",  # Front of card
                "afmt": '{{FrontSide}}<hr id="answer">{{Spanish}}<hr>{{Note}}',  # Back of card
            },
            {
                "name": "Spanish to English",
                "qfmt": "{{Spanish}}",  # Front of card
                "afmt": '{{FrontSide}}<hr id="answer">{{English}}<hr>{{Note}}',  # Back of card
            },
        ],
    )

    # Read the CSV and add notes to the deck
    with open(input_csv, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            english = row[0]
            spanish = row[1]
            card_note = row[2]

            print(english)
            print(spanish)
            print(card_note)
            # convert the card_note from mardown to html
            card_note = markdown.markdown(card_note, extensions=["def_list"])

            note = genanki.Note(model=my_model, fields=[english, spanish, card_note])
            deck.add_note(note)

    # Save the deck to a file
    genanki.Package(deck).write_to_file(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV to Anki Deck")
    parser.add_argument("input_csv", help="Input CSV file path")
    parser.add_argument("deck_name", help="Name of the Anki deck")
    parser.add_argument("output_file", help="Output Anki deck file path (.apkg)")

    args = parser.parse_args()

    create_anki_deck(args.input_csv, args.deck_name, args.output_file)
