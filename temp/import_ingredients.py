import csv

from models import orm


def import_ingredients():
    with open('ingredients.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            processed_row = [v or 0 for v in row]
            ingredient = orm.Ingredient.objects.filter(
                name=processed_row[0]
            ).first() or orm.Ingredient(None, *processed_row)
            ingredient.save()


if __name__ == '__main__':
    import_ingredients()
