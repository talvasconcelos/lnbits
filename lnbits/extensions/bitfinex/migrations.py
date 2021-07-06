async def m001_initial(db):
   await db.execute(
       f"""
       CREATE TABLE bitfinex.bitfinex (
           id {db.serial_primary_key},
           wallet TEXT NOT NULL,
           currency TEXT NOT NULL,
           bfx_key TEXT NOT NULL,
           bfx_secret TEXT NOT NULL
       );
   """
   )
