from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand, CommandParser

from ...models import Airports, model_key_map


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
        #TODO: doublecheck large airports

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
        for i in airports_frame.loc[airports_frame.type == "large_airport"].iterrows():
            csv_record = i[1]
            db_record = Airports()
            for csv_key, db_key in model_key_map.items():
                if db_key == "scheduled_service":
                    db_record.__setattr__(
                        db_key, True if csv_record[csv_key] == "yes" else False
                    )
                    continue
                db_record.__setattr__(db_key, csv_record[csv_key])

            db_record.save()

    def handle(self, *args, **options) -> None:
        csv_path = Path(options["path"])
        self.push_records(csv_path)
