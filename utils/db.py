from utils.db_object import db

async def execute(query, is_many, values=None):
	if is_many:
		await db.execute_many(query=query, values=values)
	else:
		await db.execute(query=query, values=values)
