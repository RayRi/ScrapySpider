#-*-coding:utf8-*-
import logging
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.job import job_dir

from ScrapyFrame.utils.base import database

class CustomizeRFPDupeFilter(RFPDupeFilter):
    """Customize Duplicated Request Filter

    Add More term as Duplicated condition. Use the CustomizeRFPDupeFilter object,
    with setup some term in `settings`:
        * DUPEFILTER_CLASS =’ScrapyFrame.dupefilters.CustomizeRFPDupeFilter', 
            which can util the class `CustomizeRFPDupeFilter`
        * DUPEFILTER_DEBUG=True, which can use the log information
        * SPIDER_NAME, it must be set so that can connect the redis cache database
            that is same with spider name
    Anogher information must be set, like `UNIQUE_ID` that is set in request `meta`
        * UNIQUE_ID, it's another information that can filter duplicated request
            in redis cache database
    """

    def __init__(self, path=None, debug=False):
        RFPDupeFilter.__init__(self, path=path, debug=debug)



    @classmethod
    def from_settings(cls, settings):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        # cache database connection that is class property
        cls.db = settings.get("SPIDER_NAME")
        cls.cache_conn = database.RedisConnect()
        return cls(job_dir(settings), debug)


    def request_seen(self, reqeust):
        unique_id = request.meta.get("UNIQUE_ID")
        if unique_id in self.cache_conn.sismember(self.db, unique_id):
            return True
            self.logger.log(logging.INFO, f"Request data {unique_id} is duplicated")
        
        self.fingerprints.add(unique_id)

        if self.file:
            self.file.write(str(unique_id) + "\n")