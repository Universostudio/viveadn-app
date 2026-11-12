import re, json
t=open('dic.txt').read()
# fix mojibake emoji prefixes: strip non-letters before labels
days=[]
pat=re.compile(r'\n([^\n|]+?) \| (Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo) (\d+) de diciembre\n')
ms=list(pat.finditer(t))
for i,m in enumerate(ms):
    end=ms[i+1].start() if i+1<len(ms) else len(t)
    body=t[m.end():end]
    def sec(label_re, nxt_re):
        mm=re.search(label_re+r'\n\n(.*?)(?=\n\n[^\n]*?(?:'+nxt_re+'))',body,re.S)
        return mm.group(1).strip() if mm else None
    d={'n':int(m.group(3)),'titulo':m.group(1).strip(),'dia':m.group(2)}
    mm=re.search(r'RAÍZ\n\n(«.*?»)\n\n(.*?), RVR1960',body,re.S); d['verso']=mm.group(1); d['ref']=mm.group(2).strip()
    mm=re.search(r'TALLO\n\n(.*?)\n\n[^\n]*Acción diaria',body,re.S); d['tallo']=mm.group(1).strip()
    mm=re.search(r'HOJA\n\n(.*?)\n\n[^\n]*Pregunta de reflexión',body,re.S); d['hoja']=mm.group(1).strip()
    mm=re.search(r'MI TESTIMONIO\n\n(.*?)\n\n[^\n]*Oración del día',body,re.S); d['test']=mm.group(1).strip()
    mm=re.search(r'Oración del día\n\n(.*?)\n\n[^\n]*Frase del día',body,re.S); d['oracion']=mm.group(1).strip()
    mm=re.search(r'FRUTO\n\n(.*?)\n\n[^\n]*Plan de lectura',body,re.S); d['fruto']=mm.group(1).strip()
    mm=re.search(r'Capítulo del día: (.*?)\n',body); d['cap']=mm.group(1).strip()
    mm=re.search(r'Lecturas complementarias: (.*?)(?:\n|$)',body); d['comp']=mm.group(1).strip() if mm else ''
    days.append(d)
json.dump(days,open('dias.json','w'),ensure_ascii=False,indent=1)
print(len(days))
import statistics
for d in days:
    dim=re.match(r'\((\w+)\)',d['hoja']); 
    print(d['n'],d['dia'][:3],d['titulo'][:34].ljust(34),d['ref'].ljust(18),dim.group(1) if dim else '?', 'tallo',len(d['tallo'].split()),'fruto',len(d['fruto']))
print('tallo mean',statistics.mean(len(d['tallo'].split()) for d in days))
print('fruto >150:',sum(len(d['fruto'])>150 for d in days),'of',len(days))
alltext=t
print('cotidian',len(re.findall(r'cotidian',alltext,re.I)),'emdash',alltext.count('—'),'voseo',re.findall(r'\b(podés|escuchás|tenés|sos)\b',alltext))
