"""Update only extension navigation and the documentation index; preserve root README."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'evidence-workbench/README.md'
s=p.read_text()
s=s.replace('[pilot protocol 0.2.0](../PROTOCOL.md)','[archived pilot protocol 0.2.0](../archive/v0.2/PROTOCOL.md)').replace('[original visual study](../study-report.html)','[original visual study](../archive/v0.2/study-report.html)')
line='\n**Current reading edition:** [Catholic study 0.4.0-dev](../README.md). This workbench is a retained methodological companion. Its historical byte checks now use `archive/v0.2`.\n'
if line not in s:s=s.replace('# Evidence workbench 0.3.0','# Evidence workbench 0.3.0\n'+line,1)
p.write_text(s)
p=ROOT/'EVIDENCE_INDEX.md';s=p.read_text()
line='\n**Current study:** [Reading package 0.4.0-dev and source-verification pilot](README.md).\n'
if line not in s:s=s.replace('# Follow the evidence','# Follow the evidence\n'+line,1)
s=s.replace('[protocol 0.2.0](PROTOCOL.md)','[archived protocol 0.2.0](archive/v0.2/PROTOCOL.md)').replace('[original visual study](study-report.html)','[original visual study](archive/v0.2/study-report.html)');p.write_text(s)
p=ROOT.parents[2]/'docs/README.md'
if p.exists():
 s=p.read_text();row='| [Catholic institutional pilot](../research/extensions/catholic-institutions/README.md) | Guided study, scoping, captured source verification and independent-review limits |\n'
 if row not in s:s=s.replace('| [Research brief]',row+'| [Research brief]',1)
 p.write_text(s)
print('Extension navigation updated. Root README untouched.')
