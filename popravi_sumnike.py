def slovar():
    """http://www.utf8-chartable.de/unicode-utf8-table.pl?start=256&names=-&utf8=string-literal"""
    s = dict()
    s['č'] = '\\xc4\\x8d'
    s['Č'] = '\\xc4\\x8c'
    s['š'] = '\\xc5\\xa1'
    s['Š'] = '\\xc5\\xa0'
    s['ž'] = '\\xc5\\xbe'
    s['Ž'] = '\\xc5\\xbd'
    return s
    
def popravi(beseda, slovar_sumnikov=slovar()):
    popravljeno = beseda
    for k, v in slovar_sumnikov.items():
        popravljeno = popravljeno.replace(v, k)
    return popravljeno

##se vedno bo problem pri vseh ostalih naglasih
##pri imenu Nina imas se neke bolj eksoticne crke -.-
