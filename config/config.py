from dataclasses import dataclass, field
from typing import Optional
import datetime


@dataclass
class searchConfigs:
    
    topics: Optional[list] = None
    cities: Optional[dict] = None

    filter_name: Optional[str]  = None
    filter_value: Optional[str] = None

    minimum_price: int | None = None
    maximum_price: int | None = None


    database_name: Optional[str] = None

    database_type: Optional[int] = None
    

class config_api_data:

    url = "https://api.divar.ir/v8/postlist/w/search"


    headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }
    
    max_retry = 5

    default_database_name = 'ads'

    timeout = 10



@dataclass
class info:
    time_start: datetime.datetime = field(
        default_factory=datetime.datetime.now
    )

    topic : str | None = None

    city: str |None = None

@dataclass
class Data_Config:

    filter_name: Optional[str]
    filter_value: Optional[str]

    min_price: Optional[int]
    max_price: Optional[int]

    database_name: Optional[str]
    database_type: Optional[str]

