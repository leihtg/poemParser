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


import random


def rand(per) -> bool:
    return random.random() < per


c = 0
t, f = 0, 0
while c < 2000:
    if rand(0.95):
        t += 1
    else:
        f += 1
    c += 1

print("true:", t)
print("fals:", f)
print("per :", t / (t + f))
