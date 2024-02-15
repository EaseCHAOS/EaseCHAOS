import os

from fastapi import APIRouter
from pydantic import BaseModel
from extract.extract_table import get_time_table, _get_all_daily_tables
import json
from pathlib import Path

from api.config.redis_config import get_table_from_cache, add_table_to_cache


# Find the path of the drafts
current_script_path = Path(__file__)
project_root_path = current_script_path.parent
DRAFTS_FOLDER = project_root_path / "drafts"

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
    filename = os.path.join(DRAFTS_FOLDER, request.filename)

    table = get_table_from_cache(request.class_pattern, request.filename)

    if table is None:
        table = get_time_table(filename, request.class_pattern).to_json(orient='records')
        add_table_to_cache(
            table=table,
            class_pattern=request.class_pattern,
            filename=request.filename
        )

    return json.loads(table)