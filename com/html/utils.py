import os


class Utils:

    @staticmethod
    def urlClean(url: str = '') -> str:
        '''
        清理url
        :return:
        '''
        if not url:
            return url
        if url.startswith('http://'):
            return 'http://' + os.path.relpath(url[7:]).replace(os.sep, '/')
        elif url.startswith('https://'):
            return 'https://' + os.path.relpath(url[8:]).replace(os.sep, '/')
        else:
            return os.path.relpath(url).replace(os.sep, '/')
