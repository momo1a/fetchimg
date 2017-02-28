def _monkey_patching_HTTPClientParser_statusReceived():
        """
        monkey patching for scrapy.xlib.tx._newclient.HTTPClientParser.statusReceived
        для обхода ошибки, когда статус выдаётся без "OK" в конце
        """
        from twisted.web._newclient import HTTPClientParser, ParseError
        old_sr = HTTPClientParser.statusReceived
    
        def statusReceived(self, status):
            try:
                return old_sr(self, status)
            except ParseError as e:
                if e.args[0] == 'wrong number of parts':
                    return old_sr(self, status + ' OK')
                raise
        statusReceived.__doc__ == old_sr.__doc__
        HTTPClientParser.statusReceived = statusReceived

_monkey_patching_HTTPClientParser_statusReceived()