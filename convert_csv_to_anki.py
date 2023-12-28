import argparse
import csv
import glob
import hashlib
import os
import random

import genanki
import markdown


def create_anki_deck(input_csv, deck_name, output_file):
    # Create a new Anki deck
    deck = genanki.Deck(89928173198734231, deck_name)  # Randomly generated deck ID

    # Define a model (card type)
    my_model = genanki.Model(
        int(hashlib.sha1(deck_name.encode()).hexdigest()[:5], 16),
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


def concatenate_and_convert_to_anki(levels):
    for level in levels:
        print(f"Processing level {level}")
        # Create or open the file for the current level
        with open(f"spanish-lessons/{level}.csv", "w") as outfile:
            print(f"Creating {level}.csv")  
            # Find all .csv files for the current level
            for filename in glob.glob(f"learn-spanis/h{level}-*.csv"):
                print(f"Processing {filename}")
                if os.path.isfile(filename):
                    # Read the contents of the file and append it to the level file
                    with open(filename, "r") as infile:
                        outfile.write(infile.read())

        # After concatenation, convert the CSV to Anki package

        create_anki_deck(
            f"spanish-lessons/{level}.csv",
            f"Spanish {level}",
            f"spanish-lessons/{level}.csv",
        )


# Define the levels
levels = ["A1", "A2", "B1", "B2", "C1", "C2"]


if __name__ == "__main__":
    concatenate_and_convert_to_anki(levels)


