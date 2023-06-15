import os
from sqlalchemy import func
from api.models.item import Item
from api import db
from werkzeug.datastructures import FileStorage

def _upload_image(image: FileStorage, name: str) -> str:
    """
    Uploads an image to the server.

    :param image: An image file to upload.

    :return: The image URL.
    """
    image.filename = name + os.path.splitext(image.filename)[1]
    save_directory = 'resources\\items'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    file_path = os.path.join(save_directory, image.filename)
    image.save(file_path)

    return file_path

def _update_image_name(old_path: str, new_name: str) -> str:
    """
    Updates an image name.

    :param old_path: The old image path.
    :param new_name: The new image name.

    :return: The updated image name.
    """
    if not old_path or not os.path.exists(old_path):
        return None
    
    new_path = os.path.join(os.path.dirname(old_path), new_name + os.path.splitext(old_path)[1])
    os.rename(old_path, new_path)

    return new_path

def _delete_image(image_url: str) -> bool:
    """
    Deletes an image from the server.

    :param image_url: The image URL to delete.
    
    :return: True if the image was deleted, false if the image does not exist.
    """
    if not image_url or not os.path.exists(image_url):
        return False
    
    os.remove(image_url)
    return True

def get_items() -> list[Item]:
    """
    Gets all items from the database.

    :return: A list of items.
    """
    return Item.query.all()

def get_item(id: int) -> Item:
    """
    Gets an item from the database.

    :param id: The ID of the item to get.

    :return: The item, none if the item does not exist.
    """
    return Item.query.filter_by(id=id).first()

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
    item.image_url = _upload_image(image, item.name) if image else None

    max_id = db.session.query(func.max(Item.id)).scalar()
    new_id = int(max_id) + 1 if max_id else 1
    item.id = new_id

    db.session.add(item)
    db.session.commit()

    return item

def update_item(id: int, new_item: Item) -> Item:
    """
    Updates an item in the database.

    :param id: The ID of the item to update.
    :param new_item: An item object with the updated data.

    :return: The updated item, none if the item does not exist.
    """
    item = Item.query.filter_by(id=id).first()
    if not item:
        return None
    
    item.name = new_item.name
    item.description = new_item.description
    item.price = new_item.price
    item.category = new_item.category
    item.size = new_item.size
    item.color = new_item.color
    item.stock = new_item.stock

    new_path = _update_image_name(item.image_url, new_item.name)
    if not new_path:
        item.image_url = None

    db.session.commit()

    return item

def update_item_image(id: int, image: FileStorage) -> Item:
    """
    Updates an item's image in the database.

    :param id: The ID of the item to update.
    :param image: An image file to upload.

    :return: The updated item, none if the item does not exist.
    """
    item = Item.query.filter_by(id=id).first()
    if not item:
        return None
    
    deleted = _delete_image(item.image_url)
    item.image_url = _upload_image(image, item.name)

    db.session.commit()

    return item

def delete_item(id: int) -> bool:
    """
    Deletes an item from the database.

    :param id: The ID of the item to delete.

    :return: True if the item was deleted, false if the item does not exist.
    """
    item = Item.query.filter_by(id=id).first()
    if not item:
        return False
    
    deleted = _delete_image(item.image_url)
    db.session.delete(item)
    db.session.commit()

    return True
