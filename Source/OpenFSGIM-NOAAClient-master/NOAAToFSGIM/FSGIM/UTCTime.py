import time, datetime

#  This function generates a UTC formatted timestamp which is shown formatted
#  as "YYYY-MM-DDTHH:MM:SSZ".  I've added the missing "Z" to the formatting pattern.
#
#  Since this routine is used for more than the <updated> atom tag, please consider
#  renaming it "UTCTime" for clarity.


class UTCTime:

    @staticmethod
    def getTime():
        t = time.time()
        d = datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%dT%H:%M:%SZ")
        return d