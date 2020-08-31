# Emojitracker Historical Data

Poll the [emojitracker REST API][] hourly to collect updated emoji counts.

## Usage

```python
python ./emojihistory.py -v emoji.db
```

```
[2020-08-31 18:54:07 EDT] INFO - Opened database connection to "emoji.db"
[2020-08-31 18:54:07 EDT] INFO - Database is fresh, creating tables
[2020-08-31 18:54:08 EDT] INFO - Updated emoji in 0.00322 s
[2020-08-31 18:54:08 EDT] INFO - Inserted counts in 0.00255 s
[2020-08-31 18:54:08 EDT] INFO - Closed database connection
```

[emojitracker REST API]: https://github.com/emojitracker/emojitrack-rest-api
