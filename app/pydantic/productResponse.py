from pydantic import BaseModel
from typing import Optional, List, Dict



class ListMapping(BaseModel):
    id: int
    discount: Optional[float]
    image: Optional[str]
    is_active: bool
    name: Optional[str]
    status: Optional[str]
    type_id: Optional[int]
    unit_price: Optional[float]
    type: Optional[Dict]


class Pagging(BaseModel):
    page_no: str
    total_pages: str
    total_records: str
    display_records: str


class ResponseList(BaseModel):
    code = 'SUCCESS'
    message: str
    message_kh: str
    data: Optional[List[ListMapping]]
    paging: Optional[Pagging]

class ResponseModel(BaseModel):
    code = 'SUCCESS'
    message: str
    message_kh: str
    data: Optional[dict]