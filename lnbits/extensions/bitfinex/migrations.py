async def m001_initial(db):
   await db.execute(
       f"""
       CREATE TABLE bitfinex.connections (
           id {db.serial_primary_key},
           userd TEXT NOT NULL,
           name TEXT NOT NULL,
           wallet TEXT NOT NULL,
           bfx_key TEXT NOT NULL,
           bfx_secret TEXT NOT NULL
       );
   """
   )
