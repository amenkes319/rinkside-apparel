import os
from sqlalchemy import func
from api.models.item import Item
from api import db
from werkzeug.datastructures import FileStorage

def _upload_image(image: FileStorage) -> str:
    """
    Uploads an image to the server.

    :param image: An image file to upload.

    :return: The image URL.
    """
    save_directory = 'resources\\items'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = image.filename
    file_path = os.path.join(save_directory, image.filename)
    image.save(file_path)

    return file_path

def get_items() -> list[Item]:
    """
    Gets all items from the database.

    :return: A list of items.
    """
    return Item.query.all()

def create_item(item: Item, image: FileStorage) -> Item:
    """
    Creates an item in the database.

    :param item: An item object.

    :return: The created item, none if the item name already exists.
    """
    item_exists = Item.query.filter_by(name=item.name).first()
    if item_exists:
        return None
    # file name is name with file extension
    image.filename = item.name + os.path.splitext(image.filename)[1]
    item.image_url = _upload_image(image) if image else None

    max_id = db.session.query(func.max(Item.id)).scalar()
    new_id = int(max_id) + 1 if max_id else 1
    item.id = new_id

    db.session.add(item)
    db.session.commit()

    return item
