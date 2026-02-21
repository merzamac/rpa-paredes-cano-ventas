from pydantic import BaseModel
from datetime import date
from pathlib import Path
from typing import Optional

from dateparser import parse
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)
from rpa_paredes_cano_ventas.exceptions.file_processor import (
    InvalidFileNameError,
    InvalidFolderPathError,
)


class BasePeriodModel(BaseModel):
    """Base class to handle shared equality and hashing logic."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    period_date: Optional[date] = None

    def __hash__(self) -> int:
        return hash(self.period_date)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BasePeriodModel):
            return False
        return self.period_date == other.period_date


class ProcessableFile(BasePeriodModel):
    file_path: Path
    output_path: Optional[Path] = None
    month: Optional[str] = None
    year: Optional[str] = None

    @field_validator("file_path")
    @classmethod
    def validate_file_path(cls, value: Path) -> Path:
        if not value.exists():
            raise FileNotFoundError(f"File not found: {value}")
        if value.suffix.lower() != ".xlsx":
            raise ValueError(f"Not an Excel file: {value.suffix}")
        return value

    @model_validator(mode="before")
    @classmethod
    def extract_metadata(cls, data: dict) -> dict:
        """Parses the file path to populate fields before the model is frozen."""
        if isinstance(data, dict) and "file_path" in data:
            path = Path(data["file_path"])
            folder_year = path.parent.name

            # Logic: "01. PLE ENERO 26.xlsx" -> ['01.', 'PLE', 'ENERO', '26']
            stem_parts = path.stem.strip().split()
            len_parts = len(stem_parts)
            if len_parts < 4 or not folder_year.isdigit():
                raise InvalidFileNameError(
                    f"Filename format unexpected: '{path.name}' should be 'XX. PLE MONTH YY. len_parts: '{len_parts}' should be 4. folder_year: '{folder_year}' should be 4 digits."
                )

            month_number = stem_parts[0].replace(".", "")
            month = stem_parts[2].upper()
            if not (
                len(month_number) == 2 and len(month) >= 4 and len(folder_year) == 4
            ):
                raise InvalidFileNameError(f"Filename format unexpected: {path.name}")

            # Populate the data dict so Pydantic initializes them normally
            data["year"] = folder_year
            data["month"] = month
            data["period_date"] = date(int(folder_year), int(month_number), 1)
            data["output_path"] = Path(folder_year) / month

        return data


class ProcessedFolder(BasePeriodModel):
    output_path: Path

    @model_validator(mode="before")
    @classmethod
    def parse_folder_date(cls, data: dict) -> dict:
        if isinstance(data, dict) and "output_path" in data:
            path = Path(data["output_path"])
            # parts[-2:] gives (year, month)
            try:
                year, month = path.parts[-2:]
            except ValueError:
                raise InvalidFolderPathError(f"Path too short: {path}")

            parsed = parse(f"1 {month} {year}", languages=["es"])
            if not parsed:
                raise DateParsingError(f"Could not parse date from:  {month}/{year}")

            data["period_date"] = parsed.date()
        return data
