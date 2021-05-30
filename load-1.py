#import runpy

#import loadNVDR-1
#import loadShortSell-1
#exec(compile(open('loadPrice.py').read(), file, 'exec'))
exec(open("./loadNVDR-1.py").read())
exec(open("./loadShortSell-1.py").read())
exec(open("./loadFutureOI.py").read())
exec(open("./loadPrice-1.py", 'rb').read())