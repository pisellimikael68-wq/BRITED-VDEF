#!/usr/bin/env python3
from __future__ import annotations

import argparse, ast, hashlib, json, re, shutil
from pathlib import Path

KEYWORDS=("brited","leveria","studio","contenu","script","tiktok","instagram","youtube","calendrier","vidéo","video","fiscal","jurid","patrimoine","immobilier","finance","source","validation","automatisation")

def messages_master(text: str):
    matches=list(re.finditer(r"(?m)^\[(\d+)\] (user|assistant):\s*",text))
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(text)
        block=re.split(r"(?m)^\[\d+\] tool ",text[m.end():end],maxsplit=1)[0]
        yield "codex",m.group(1),m.group(2),block.strip()

def messages_chatgpt(text: str):
    pattern=re.compile(r"(?m)^=====\s+(\d+)\s+·\s+(USER|ASSISTANT)\s+=====\s*$")
    markers=list(pattern.finditer(text))
    for i,m in enumerate(markers):
        end=markers[i+1].start() if i+1<len(markers) else len(text)
        yield "chatgpt",m.group(1),m.group(2).casefold(),text[m.end():end].strip()

def relevant(text: str) -> bool:
    low=text.casefold()
    return len(text)>1 and any(word in low for word in KEYWORDS)

def subject_bank(path: Path):
    tree=ast.parse(path.read_text(encoding="utf-8")); bank=ast.literal_eval(tree.body[0].value)
    return [{"pillar":pillar,"family":family,"subject":subject,"status":"a_certifier"}
            for pillar,families in bank.items() for family,subjects in families.items() for subject in subjects]

def inventory(root: Path):
    groups={"governance":root/".brited","knowledge_engine":root/"v2/knowledge","corpus":root/"content",
            "scripts":root/"scripts","production":root/"production","video_pipeline":root/"video_pipeline"}
    result=[]
    for kind,folder in groups.items():
        for path in sorted(folder.rglob("*")) if folder.exists() else []:
            if path.is_file() and "__pycache__" not in path.parts:
                result.append({"kind":kind,"path":str(path.relative_to(root)),"size":path.stat().st_size,
                               "extension":path.suffix.casefold()})
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--master",type=Path,required=True);p.add_argument("--chatgpt",type=Path,required=True);a=p.parse_args()
    root=a.root.resolve(); recovered=root/"recovery"; recovered.mkdir(parents=True,exist_ok=True)
    shutil.copy2(a.master,recovered/"BRITED_MASTER_TRANSCRIPT.txt")
    decisions=[]; seen=set()
    for source,seq,role,text in [*messages_master(a.master.read_text(encoding="utf-8",errors="ignore")),*messages_chatgpt(a.chatgpt.read_text(encoding="utf-8",errors="ignore"))]:
        if not relevant(text): continue
        digest=hashlib.sha256(re.sub(r"\s+"," ",text.casefold()).encode()).hexdigest()[:16]
        if digest in seen: continue
        seen.add(digest); decisions.append({"id":digest,"source":source,"sequence":int(seq),"role":role,"text":text})
    subjects=subject_bank(root/"v2/editorial/subject_bank.py")
    files=inventory(root)
    sources=[]
    for label,path in (("codex",a.master),("chatgpt",a.chatgpt)):
        sources.append({"label":label,"path":str(path),"size":path.stat().st_size,
                        "sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    heritage={"version":2,"sources":sources,"conversation_messages":decisions,"subject_bank":subjects,"artifacts":files,
              "summary":{"conversation_messages":len(decisions),"subject_bank":len(subjects),"artifacts":len(files),
                         "governance":sum(x["kind"]=="governance" for x in files),
                         "knowledge_engine":sum(x["kind"]=="knowledge_engine" for x in files),
                         "corpus_files":sum(x["kind"]=="corpus" for x in files)}}
    (root/"data/history.json").write_text(json.dumps(heritage,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    requirements=json.loads((root/"data/requirements.json").read_text(encoding="utf-8"))
    policy=json.loads((root/"data/editorial_policy.json").read_text(encoding="utf-8"))
    ledger={"version":1,"requirements":requirements,"editorial_policy":policy,
            "provenance":{"history":"data/history.json","raw_transcript":"recovery/BRITED_MASTER_TRANSCRIPT.txt","source_hashes":sources}}
    (root/"data/decision_ledger.json").write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(heritage["summary"],ensure_ascii=False))

if __name__=="__main__": main()
