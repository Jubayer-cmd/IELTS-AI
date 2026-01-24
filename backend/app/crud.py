"""
CRUD operations.

Add your database operations here.
"""
from sqlmodel import Session, select

# Example CRUD pattern:
#
# def create_item(*, session: Session, item_create: ItemCreate) -> Item:
#     db_item = Item.model_validate(item_create)
#     session.add(db_item)
#     session.commit()
#     session.refresh(db_item)
#     return db_item
#
# def get_item_by_id(*, session: Session, item_id: int) -> Item | None:
#     return session.get(Item, item_id)
