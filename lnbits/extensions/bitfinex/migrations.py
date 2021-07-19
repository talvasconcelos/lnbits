async def m001_initial(db):
   await db.execute(
       f"""
       CREATE TABLE bitfinex.connections (
           id {db.serial_primary_key},
           "user" TEXT,
           wallet TEXT NOT NULL,
           bfx_key TEXT NOT NULL,
           bfx_secret TEXT NOT NULL
       );
   """
   )
