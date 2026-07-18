import requests,time
from config.config import config_api_data
from core.services import log
from core.Cancel_token import CancelToken

ask_data = config_api_data()

class RequestClient:

    def __init__(self):

        self.session = requests.Session()

    def post(
            self,
            url,
            payloads,
            headers,
            cancel_token,
            timeout= 10
    ) :
        """
        make a session and post a ongoing rquest until has no nxt page

        take url, payloads,headers,timeout

        url : api url for making a request and a session
        payloads : info for what page and what you search
        headers : what is your name in sites , sending the info of our computer
        timeout : in what time(second) i retry the connection

        return page in json and status code
        """
        for attempt in range(ask_data.max_retry):

            try:
                
               
                if cancel_token.is_cancelled():
                    timeout = 0
                    return

                response = self.session.post(
                    url = url,
                    json=payloads,
                    headers=headers,
                    timeout=timeout
                )


                if response.status_code == 200:

                    try:

                        return response.json(),response.status_code
                    
                    except ValueError:

                        log.error_log(
                            error='invalid JSON',
                            where='RequestClient.post',
                            state = 200
                        )

                        return None, None
                    
                elif response.status_code == 429:
                    wait = 2 ** attempt

                    print(
                        f'rate limit. wait {wait}s'
                    )

                    if cancel_token.is_cancelled():
                        timeout = 0
                        return

                    time.sleep(wait)

                else:

                    log.error_log(
                        error = f'HTTP {response.status_code}',
                        where='RequestClient.post',
                        state = response.status_code
                    )

            except requests.exceptions.RequestException as e:

                log.error_log(
                    error = str(e),
                    where='RequestClient.post',
                    state = None
                )

        return None, None
