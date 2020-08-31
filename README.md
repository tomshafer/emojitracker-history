# Emojitracker Historical Data

Poll the [emojitracker REST API][] hourly to collect updated emoji counts.

## Usage

```bash
$ python ./emojihistory.py -v emoji.db
[2020-08-31 18:54:07 EDT] INFO - Opened database connection to "emoji.db"
[2020-08-31 18:54:07 EDT] INFO - Database is fresh, creating tables
[2020-08-31 18:54:08 EDT] INFO - Updated emoji in 0.00322 s
[2020-08-31 18:54:08 EDT] INFO - Inserted counts in 0.00255 s
[2020-08-31 18:54:08 EDT] INFO - Closed database connection
```

## Schema

```sql
CREATE TABLE emoji (
    id TEXT NOT NULL PRIMARY KEY,
    char TEXT NOT NULL,
    name TEXT NOT NULL,
    updated INTEGER DEFAULT (DATETIME('now'))
);

CREATE TABLE counts (
    id TEXT NOT NULL,
    date INTEGER NOT NULL DEFAULT(DATETIME('now')),
    count INTEGER NOT NULL,
    PRIMARY KEY(id, date)
);
```

[emojitracker REST API]: https://github.com/emojitracker/emojitrack-rest-api
