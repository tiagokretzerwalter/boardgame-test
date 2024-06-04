import csv

def import_deck(deck_file, destination_deck:list, card_type):
    """function to import the data from csv file to compose the decks"""

    with open(deck_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            destination_deck.append(row[card_type])