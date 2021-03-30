#import runpy

#import loadNVDR-1
#import loadShortSell-1
#exec(compile(open('loadPrice.py').read(), file, 'exec'))
exec(open("./loadPrice.py").read())
exec(open("./loadFutureOI.py").read())