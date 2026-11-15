"""Run source-based CulturaEval exploratory pilot; no automatic gold scores.

Requires CULTURAEVAL_API_KEY in environment. Use ONLY with explicitly consented API spend.
"""
import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

CONDITIONS = ("passage_only", "relevant", "partial", "misleading")
SYSTEM = """You are evaluating interpretations of culturally situated literary texts.
Do not assume supplied external context is true. Distinguish direct textual claims,
external evidence and conjecture. State what the passage supports, identify up to
two competing plausible interpretations (or explain why the evidence excludes them),
and weigh those interpretations without inventing cultural facts.
Respond with JSON object using keys: main_interpretation, passage_evidence,
context_claims_used, alternative_interpretations, uncertainties, likely_errors.
All keys required. passage_evidence is an exact substring of the supplied PASSAGE;
alternative_interpretations is an array; other fields are strings except
context_claims_used which is an array of strings."""

def request(case, condition, model, key):
    context = "(No external context provided.)" if condition == "passage_only" else case["contexts"][condition]
    body = {"model": model, "temperature": 0, "response_format": {"type": "json_object"},
            "messages": [{"role":"system","content":SYSTEM},
                         {"role":"user","content":f"PASSAGE:\n{case['passage']}\n\nEXTERNAL CONTEXT [{condition}]:\n{context}\n\nInterpret the passage critically."}]}
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
                                  data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                                  headers={"Authorization":f"Bearer {key}", "Content-Type":"application/json"},
                                  method="POST")
    with urllib.request.urlopen(req,timeout=90) as res:
        raw = json.load(res)
    reply = raw["choices"][0]["message"]["content"]
    parsed = json.loads(reply)
    return {"answer":parsed, "usage":raw.get("usage",{}),
            "provider_model":raw.get("model"), "response_id":raw.get("id"),
            "finish_reason":raw["choices"][0].get("finish_reason")}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset",default="data/authentic_pilot_candidates.jsonl")
    p.add_argument("--model",default="gpt-4.1-mini")
    p.add_argument("--limit",type=int,default=2)
    p.add_argument("--output",default="results/authentic-pilot")
    args=p.parse_args()
    key=os.environ.get("CULTURAEVAL_API_KEY")
    if not key:
        p.error("CULTURAEVAL_API_KEY missing")
    cases=[json.loads(line) for line in Path(args.dataset).read_text(encoding="utf-8").splitlines() if line.strip()]
    cases=cases[:args.limit]
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    results=[]; failures=[]
    for case in cases:
        for condition in CONDITIONS:
            try:
                response=request(case,condition,args.model,key)
                results.append({"case_id":case["id"],"model_requested":args.model,
                                "condition":condition,"source_url":case["source_url"],
                                "review_status":case["review_status"],**response})
                print(f"OK: {case['id']} / {condition}",flush=True)
            except urllib.error.HTTPError as exc:
                failure={"case_id":case["id"],"condition":condition,"http_status":exc.code}
                try:
                    error=json.loads(exc.read().decode("utf-8"))
                    failure["message"]=str(error.get("error",{}).get("message",""))[:200]
                except Exception:
                    pass
                failures.append(failure)
                print(f"FAILED: {case['id']} / {condition} (HTTP {exc.code})",flush=True)
            except Exception as exc:
                failures.append({"case_id":case["id"],"condition":condition,"error":str(exc)[:200]})
                print(f"FAILED: {case['id']} / {condition} ({type(exc).__name__})",flush=True)
            time.sleep(0.2)
    with (out/"model_responses.jsonl").open("w",encoding="utf-8") as f:
        for row in results: f.write(json.dumps(row,ensure_ascii=False)+"\n")
    report={"status":"SOURCE-BASED EXPLORATORY PILOT; NOT CULTURALLY VALIDATED",
            "model":args.model,"cases":len(cases),"successful_requests":len(results),
            "failed_requests":len(failures),"failures":failures,
            "human_scores_available":False,
            "limitations":["Primary source passages checked at cited Gutenberg URLs",
                           "Context notes and interpretations not independently expert-validated",
                           "No human judgment of cultural reasoning or interpretive plurality",
                           "No significance claims warranted from pilot size"]}
    (out/"report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":
    main()
