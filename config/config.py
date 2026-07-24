from dataclasses import dataclass, field
from typing import Optional
import datetime


@dataclass
class searchConfigs:
    
    topics: Optional[list] = None
    cities: Optional[dict] = None

    filters: Optional[dict] = None


    database_name : Optional[list] = None

    database_type: Optional[int] = None
    

class config_api_data:

    url = "https://api.divar.ir/v8/postlist/w/search"


    headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }
    
    max_retry = 5

    default_database_name = 'ads'

    timeout = 2



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

@ dataclass
class build_config:

    window: Optional[object] = None

    selected_cities: Optional[dict] =None

    minimum: Optional[int] = None
    maximum: Optional[int] = None

    state_value: Optional[str] = None
    name_value: Optional[str] = None
    
@ dataclass

class check_past_search:
    topics: Optional[list] = None

    cities: Optional[dict] = None
    
@dataclass
class c_config:



    selected_cities: Optional[dict] =None

    minimum: Optional[int] = None
    maximum: Optional[int] = None

    state_value: Optional[str] = None
    name_value: Optional[str] = None
    