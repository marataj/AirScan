import os
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from django.core.management.base import BaseCommand, CommandParser

from AirScan.settings import BASE_DIR, DB_CONNECTION_STRING

from ...models import AirplaneModel


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "path",
            type=str,
            help="Path to the csv file with airports data",
            default=Path(BASE_DIR, "airplanes/db_initial/aircrafts_database.csv"),
        )

    def push_records(self, file_path: Path) -> None:
        """
        Function responsible for filling the initial records of the airplanes table in DB from specific csv file.
        https://opensky-network.org/aircraft-database

        Parameters
        ----------
        file_path : Path
            Path to the csv airplanes database.

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
        airplanes = pd.read_csv(
            file_path,
            usecols=["icao24", "registration", "manufacturername", "model", "serialnumber", "operator", "owner", "categoryDescription"],
        )
        airplanes.categoryDescription = airplanes.categoryDescription.astype("category")
        airplanes.manufacturername = airplanes.manufacturername.astype("category")
        airplanes.operator = airplanes.operator.astype("category")
        airplanes.owner = airplanes.owner.astype("category")
        airplanes.dropna(subset=["icao24"], axis=0)

        airplanes.to_sql(
            os.getenv("AIRPLANEMODEL_TABLE_NAME"),
            DB_CONNECTION_STRING,
            if_exists="replace",
            index=False,
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        csv_path = Path(options["path"])
        self.push_records(csv_path)
