from api.models.item import Item


def get_items():
    """
    Gets all items from the database.

    :return: A list of items.
    """
    return Item.query.all()