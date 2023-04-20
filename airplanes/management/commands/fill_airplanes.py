from django.core.management.base import BaseCommand, CommandParser
from typing import Optional, Any
import pandas as pd
from ...models import AirplaneModel
from pathlib import Path

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "path", type=str, help="Path to the csv file with airports data"
        )

    def push_records(self, file_path: Path) -> None:

        if not file_path.exists():
            raise FileNotFoundError("File not exist")
        if not file_path.suffix == ".csv":
            raise TypeError("File must be of type csv")
        airplanes = pd.read_csv(
            file_path,
            usecols=AirplaneModel.get_fields_names()[1:],
        )
        airplanes.categoryDescription=airplanes.categoryDescription.astype("category")
        airplanes.manufacturername=airplanes.manufacturername.astype("category")
        airplanes.operator=airplanes.operator.astype("category")
        airplanes.owner=airplanes.owner.astype("category")  
        
        for airplane in airplanes.iterrows():
            try:
                airplane=airplane[1]
                db_record=AirplaneModel()
                for field in AirplaneModel.get_fields_names()[1:]:
                    db_record.__setattr__(field, airplane[field])
                db_record.save()
            except TypeError:
                continue
        
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        csv_path = Path(options["path"])
        self.push_records(csv_path)
