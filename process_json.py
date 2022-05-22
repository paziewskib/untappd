from utils import load_json, save_to_json


class Beer:

    def __init__(self, beer_name: str, brewery_name: str, user_rating: float):
        """
        :param beer_name: beer name
        :param brewery_name: brewery name
        :param user_rating: user rating
        """
        self.name = beer_name
        self.brewery = brewery_name
        self.rating = user_rating


if __name__ == "__main__":
    data = load_json('<REPLACE_ME>')

    print('Getting beers...')
    all_beers = data.get('beers')
    parsed_beers = []

    print('Processing beers...')
    for beer in all_beers:
        name = beer.get('beer').get('beer_name')
        brewery = beer.get('brewery').get('brewery_name')
        rating = beer.get('rating_score')
        parsed_beers.append(Beer(name, brewery, rating))

