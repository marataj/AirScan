from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """
    Custom django command responsible for filling the airports database. The database is filled based on .csv file from https://ourairports.com/data/.

    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "path", type=str, help="Path to the csv file with airports data"
        )

    def push_records(self, file_path: Path) -> None:
        """
        Method responsible for filling the `Airports` model with records from airports.csv, downloaded from https://ourairports.com/data/.
        For shorten the process of adding new records, only the large airports are adding to the DB.

        Parameters
        ----------
        file_path : Path
            Path to the csv file.

        Raises
        ------
        FileNotFoundError
            When file doesn't exist
        TypeError
            When is not of type csv

        """
        if not file_path.exists():
            raise FileNotFoundError("File not exist")
        if not file_path.suffix == ".csv":
            raise TypeError("File must be of type csv")
        airports_frame = pd.read_csv(file_path)
        # Due to lot of data, only large airports were chosen to the developing stage.
        # airports_frame=airports_frame.loc[(airports_frame.type == "large_airport") | (airports_frame.type == "medium_airport") ....]
        airports_frame = airports_frame.loc[airports_frame.type == "large_airport"]
        airports_frame.dropna(
            subset=["latitude_deg", "longitude_deg", "ident"], axis=0, inplace=True
        )
        airports_frame.drop(axis=1, labels=["id", "scheduled_service"], inplace=True)
        # TODO: replace hardcoding with global parameters
        airports_frame.to_sql(
            "airports_db",
            "postgresql://postgres:root@localhost/airscan",
            if_exists="replace",
            index=False,
        )

    def handle(self, *args, **options) -> None:
        csv_path = Path(options["path"])
        self.push_records(csv_path)
