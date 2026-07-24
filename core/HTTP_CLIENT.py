from colorama import Fore, init
from core.Cancel_token import CancelToken

init()



class Paginator:

    def __init__(
            self,
            client,
            url,
            headers,
            payloads,
            timeout,
            signals,
            cancel_token,
            log_signal
            ):
        
        """
        Handles API pagination.
        take client,url,
        headers,payloads,timeout

        client : in charge of session and post in one connection.
        url : the api url for send request.
        headers : the headrs for divar.ir to accept the connection.
        payloads : the data's of connection.
        timeout : time for wait if the site did not respond. 
        """
        
        self.client = client

        self.url = url

        self.headers = headers

        self.payloads = payloads

        self.timeout = timeout

        self.pagination = None

        self.finished = False

        self.cancel_token = cancel_token

        self.signals = signals

        self.log_signal = log_signal

    def fetch_page(self) :

        """
        create a session and send requests to site to read
        and return the page in json and status of site in int
        return tuple
        """

        if self.cancel_token.is_cancelled():
            raise StopIteration

        request_payloads = self.payloads.copy()

        request_payloads["pagination_data"] = self.pagination



        page_json,status = self.client.post(
            url = self.url,
            payloads = request_payloads,
            headers = self.headers,
            cancel_token = self.cancel_token,
            timeout = self.timeout,
            logsignal = self.log_signal,
            signal = self.signals
        )
        self.signals.connection.emit(status)
        self.log_signal.connection.emit(status)


        return page_json,status
    
    def has_next(self,pagination_info) -> bool:
        """
        check if site has a next page or not return bool
        """

        return pagination_info.get(
            "has_next_page",
            False
        )
    
    def update_pagination(self,pagination_info) -> None:

        

        self.pagination = pagination_info.get("data")

    def __iter__(self) -> object:
        return self
    
    def __next__(self) -> tuple:
        
        if self.finished:
            raise StopIteration
        if self.cancel_token.is_cancelled():
            raise StopIteration
        
        page_json,status = self.fetch_page()

        if page_json is None:
            print("No response from API")
            raise StopIteration


        pagination_info = page_json.get(
            "pagination"
        )


        if not pagination_info:
            self.finished = True

            raise StopIteration
        
        if not self.has_next(
            pagination_info
        ):
            
            self.finished = True

        else:
            self.update_pagination(pagination_info)


        return page_json,status