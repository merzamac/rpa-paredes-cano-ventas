class FileProcessorError(Exception):
    """Base exception for the file processing module."""

    pass


class InvalidFileNameError(FileProcessorError):
    """Raised when the Excel file name doesn't match the expected 'XX. PLE MONTH YY' format."""

    pass


class InvalidFolderPathError(FileProcessorError):
    """Raised when the folder path doesn't have the expected 'YEAR/MONTH' structure."""

    pass


class DateParsingError(FileProcessorError):
    """Raised when dateparser fails to interpret the provided month/year strings."""

    pass
