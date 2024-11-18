"""Seed database with sneaker data from CSV Files."""

from csv import DictReader
from app import app, db
from models import Sneaker


def format_price(price):
    """Format price by removing '$' and converting to float."""
    try:
        if price and price.lower() != "not available":
            # Remove '$' and ',' then convert to float
            return float(price.replace('$', '').replace(',', ''))
        return None  # Use None for missing or invalid prices
    except ValueError as e:
        print(f"Error formatting price '{price}': {e}")
        return None


with app.app_context():
    db.drop_all()
    db.create_all()

    # Open the CSV file and read the data
    with open('generator/sneakers.csv') as sneakers:
        reader = DictReader(sneakers)
        
        # Format data before inserting
        data = []
        for row in reader:
            row['retail_price'] = format_price(row['retail_price'])  # Format price as float
            if row['retail_price'] is None:  # Log if the price is empty
                print(f"Price missing for: {row['sneaker_name']}")
            print(f"Inserting: {row}")  # Log each row for debugging
            data.append(row)
        
        # Insert data in bulk
        db.session.bulk_insert_mappings(Sneaker, data)

    db.session.commit()
    print("Data has been successfully seeded!")
