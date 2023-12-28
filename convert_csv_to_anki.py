import argparse
import csv

import genanki
import markdown


def create_anki_deck(input_csv, deck_name, output_file):
    # Create a new Anki deck
    deck = genanki.Deck(2059400110, deck_name)  # Randomly generated deck ID

    # Define a model (card type)
    my_model = genanki.Model(
        1607392319,  # Randomly generated model ID
        "Simple Model",
        fields=[{"name": "English"}, {"name": "Spanish"}, {"name": "Note"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{English}}",  # Front of card
                "afmt": '{{FrontSide}}<hr id="answer">{{Spanish}}<hr>{{Note}}',  # Back of card
            },
        ],
    )

    # Read the CSV and add notes to the deck
    with open(input_csv, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="|")
        for row in reader:
            english = row[0]
            spanish = row[1]
            card_note = row[2]

            # convert the card_note from mardown to html
            card_note = markdown.markdown(card_note, extensions=["def_list"])
            print(card_note)

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
