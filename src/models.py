from sqlalchemy import Table, Column, Integer, String, MetaData

metadata_obj = MetaData()

receipts_table = Table(
    "receipts",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("receipt_number", Integer)
)