BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "hotel_data" (
	"id"	INTEGER,
	"user_id"	INTEGER,
	"address"	TEXT,
	"name"	TEXT NOT NULL,
	"num_of_rooms"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "season_data" (
	"id"	INTEGER,
	"user_id"	INTEGER,
	"hotel_id"	INTEGER,
	"desired_total_profit"	REAL,
	"gsheet_range"	TEXT,
	"gsheet_id"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	FOREIGN KEY("hotel_id") REFERENCES "hotel_data"("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"tg_id"	TEXT NOT NULL,
	"sub_status"	NUMERIC NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
