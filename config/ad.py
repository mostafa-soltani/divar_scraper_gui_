from dataclasses import dataclass


@dataclass

class Ad:
    title: str
    address: str
    description: str
    state: str
    token: str
    url: str