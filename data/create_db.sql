BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"tg_id"	TEXT NOT NULL,
	"booking_url" TEXT,
	"sub_status"	NUMERIC NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "hotels" (
	"id"	INTEGER,
	"user_id"	INTEGER,
	"name"	TEXT NOT NULL,
	"num_of_rooms"	INTEGER,
	"address"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "seasons_info" (
	"id"	INTEGER NOT NULL UNIQUE,
	"hotel_id"	INTEGER NOT NULL,
	"desired_total_profit"	REAL,
	"google_sheet_id"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("hotel_id") REFERENCES "hotels"("id")
);
COMMIT;
