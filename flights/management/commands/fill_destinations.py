from pathlib import Path
from typing import Any, Optional

import pandas as pd
from django.core.management.base import BaseCommand, CommandParser

from ...models import DestinationsModel


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "path", type=str, help="Path to the csv file with flights destinations data"
        )

    def push_records(self, file_path: Path) -> None:
        """
        Function responsible for filling the initial records of the destinations table in DB from specific csv file.

        Parameters
        ----------
        file_path : Path
            Path to the csv destinations database.

        Raises
        ------
        FileNotFoundError
            Raises when the file was not found.
        TypeError
            Raises when the file is no of type csv.

        """
        if not file_path.exists():
            raise FileNotFoundError("File not exist")
        if not file_path.suffix == ".csv":
            raise TypeError("File must be of type csv")
        destinations = pd.read_csv(file_path)
        
        destinations.to_sql(
            "destinations_db",
            "postgresql://postgres:root@localhost/airscan",
            if_exists="replace",
            index=False,
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        csv_path = Path(options["path"])
        self.push_records(csv_path)