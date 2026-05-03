# # app/repositories/customer_repository.py

# from sqlalchemy import text
# from sqlalchemy.ext.asyncio import AsyncSession


# class CustomerRepository:
#     """
#     Handles customer promotion queries.
#     """

#     @staticmethod
#     async def promote_from_staging(db: AsyncSession, upload_id: str) -> None:
#         """
#         Move validated rows from staging to final table.

#         SQLAlchemy 2.0 best practice:
#         raw SQL must be wrapped with `text()`
#         so AsyncSession.execute() receives an Executable object.
#         """

#         insert_stmt = text("""
#             INSERT INTO customers (upload_id, name, email, age)
#             SELECT upload_id, name, email, age::int
#             FROM customer_staging
#             WHERE upload_id = :upload_id
#         """)

#         delete_stmt = text("""
#             DELETE FROM customer_staging
#             WHERE upload_id = :upload_id
#         """)

#         await db.execute(insert_stmt, {"upload_id": upload_id})
#         await db.execute(delete_stmt, {"upload_id": upload_id})
#         await db.commit()
