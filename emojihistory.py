"""Collect emojitracker data and store in sqlite."""

__version__ = "0.0.1"

import argparse as ap
import json
import logging
import sqlite3
import time
from typing import Dict, List

import requests

logging.basicConfig(
    level=logging.WARNING,
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    format="[%(asctime)s] %(levelname)s - %(message)s ",
)

logger = logging.getLogger()


def parser() -> ap.ArgumentParser:
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-v", dest="VERBOSE", action="store_true", help="show INFO messages"
    )
    parser.add_argument("DATABASE", help="path to the sqlite database")
    return parser


def create_tables(con: sqlite3.Connection) -> None:
    with con:
        con.execute(
            """
            CREATE TABLE emoji (
                id TEXT NOT NULL PRIMARY KEY,
                char TEXT NOT NULL,
                name TEXT NOT NULL,
                updated INTEGER DEFAULT (DATETIME('now'))
            );
            """
        )
        con.execute(
            """
            CREATE TABLE counts (
                id TEXT NOT NULL,
                date INTEGER NOT NULL DEFAULT(DATETIME('now')),
                count INTEGER NOT NULL,
                PRIMARY KEY(id, date)
            );
            """
        )


def is_fresh_db(con: sqlite3.Connection) -> bool:
    tables = con.execute(
        """
        SELECT name
          FROM sqlite_master
         WHERE type = 'table'
           AND name IN ('emoji', 'counts')
        """
    )
    return len(tables.fetchall()) != 2


def poll_emojitracker() -> List[Dict]:
    response = requests.get("https://api.emojitracker.com/v1/rankings")
    return json.loads(response.content)


def collect_emoji_to_db(db_name: str) -> None:
    dbc = sqlite3.connect("%s" % db_name)
    logger.info('Opened database connection to "%s"' % db_name)

    if is_fresh_db(dbc):
        logger.info("Database is fresh, creating tables")
        create_tables(dbc)

    emojidata = poll_emojitracker()
    with dbc:
        timer = time.time()
        dbc.executemany(
            """
            INSERT OR IGNORE INTO emoji (id, char, name)
            VALUES (?,?,?)
            """,
            ((e["id"], e["char"], e["name"]) for e in emojidata),
        )
        logging.info("Updated emoji in %.5f s", time.time() - timer)

        timer = time.time()
        dbc.executemany(
            """
            INSERT INTO counts (id, count)
            VALUES (?,?)
            """,
            ((e["id"], e["score"]) for e in emojidata),
        )
        logging.info("Inserted counts in %.5f s", time.time() - timer)

    dbc.close()
    logger.info("Closed database connection")


if __name__ == "__main__":
    cli = parser().parse_args()
    logger.info(cli)
    if cli.VERBOSE:
        logger.setLevel(logging.INFO)
    collect_emoji_to_db(cli.DATABASE)
