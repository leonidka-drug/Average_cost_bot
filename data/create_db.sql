BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "google_sheets_info" (
	"id"	INTEGER NOT NULL UNIQUE,
	"season_id"	INTEGER NOT NULL,
	"google_sheet_id"	TEXT,
	"google_sheet_range"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("season_id") REFERENCES "seasons_info"("id")
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
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("hotel_id") REFERENCES "hotels"("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"tg_id"	TEXT NOT NULL,
	"sub_status"	NUMERIC NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
