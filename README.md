# Usage

## Generate example phrases

In this case 5 examples will be saved to a tab sperated CSV

```
python generate.py -t "Farm work conversation (level B1)" -s 5 >> ./spanish-lessons/B2-farming-conversations.csv
```

### Example

```
English: It's vital to start the day early for work on the farm.
Spanish: Es esencial empezar el día temprano para el trabajo en la granja.

**Esencial**: Adjective, Feminine/Masculine (matches the gender of the noun it describes); meaning "essential, vital." Its origin is the Latin word "essentialis."

**Empezar**: Verb, infinitive; meaning "to start" or "to begin". Its basic root form is "Empezar". It comes from the Late Latin word "in initiare," meaning to initiate.

**Día**: Noun, Masculine; meaning "day". It stems from the Latin word "dies".

**Temprano**: Adverb; meaning "early". It's derived from the Late Latin "temporanus," meaning timely or early.
 
**Trabajo**: Noun, Masculine; meaning "work." Its root is "trabajar," which is considered of unknown origin although it's possibly from Latin translatus meaning adjusted.

**Granja**: Noun, Feminine; meaning "farm." Originates from the word "gran", indicating large, and traditionally referred to a grand house or a villa. Over time it evolved to mean a farm — an extensive piece of land used for growing crops or raising animals."
```

## Rebuild all decks

This will concat all CSVs grouped by level (A1, A2, B1...) and then generate Anki decks for each level.
```
python convert_csv_to_anki.py
```

