from fastapi import APIRouter
from pydantic import BaseModel
from extract.extract_table import get_time_table, _get_all_daily_tables

router = APIRouter()

class TimeTableRequest(BaseModel):
    """
    Represents a request for a timetable.
    
    Attributes:
    - filename (str): The name of the file for the timetable.
    - class_pattern (str): The pattern for the class.
    """
    filename: str
    class_pattern: str

@router.post("/get_time_table")
async def get_time_table_endpoint(request: TimeTableRequest):
    """
    A function to handle the POST request for getting the time table.
    
    Parameters:
    - request: TimeTableRequest - the request object containing the filename and class pattern
    
    Returns:
    - dict: a dictionary containing the table in JSON format
    """
    table = get_time_table(request.filename, request.class_pattern)
    return table.to_json(orient='records')

@router.post("/get_all_daily_tables")
async def get_all_daily_tables_endpoint(request: TimeTableRequest):
    """
    A function to handle the POST request for getting all daily tables.
    
    Parameters:
    - request: TimeTableRequest - the request object containing the filename and class pattern
    
    Returns:
    - dict: a dictionary containing the tables in JSON format, with sheet names as keys
    """
    tables = _get_all_daily_tables(request.filename, request.class_pattern)
    return {sheet: df.to_json(orient='records') for sheet, df in tables.items()}