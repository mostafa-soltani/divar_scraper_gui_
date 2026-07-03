
class statistics:

    def __init__(self):
        self.ads_found = 0
        self.ads_saved = 0
        self.page_count= 0




    def pagecount(self):
        """
        count a page that readed 
        """
        self.page_count += 1

    def adsfound(self,ads):
        """
        count ads that founded
        """
        self.ads_found += ads

    def adssaved(self,ads):
        """
        count ads that saved
        """
        self.ads_saved += ads


