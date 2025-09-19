import pandas as pd
from utils import normalize_label
import requests
import json

OLLAMA_URL = "http://localhost:11434"


class QAEngine:
    def __init__(self, model_name='mistral'):
        self.model = model_name
        self.docs = {}
        self.embeddings_index = []

    def reinit_model(self, model_name):
        self.model = model_name

    def index_document(self, raw_text, tables, doc_name='doc'):
        self.docs[doc_name] = {'raw_text': raw_text, 'tables': tables}
        chunks = [raw_text[i:i+1000] for i in range(0, len(raw_text), 1000)]
        for c in chunks:
            self.embeddings_index.append({'doc': doc_name, 'text': c})

    def _structured_lookup(self, query):
        q_norm = normalize_label(query)
        for payload in self.docs.values():
            for tbl in payload['tables']:
                try:
                    df_cols = [normalize_label(str(c)) for c in tbl.columns]
                    for i, col in enumerate(df_cols):
                        if q_norm in col:
                            colvals = pd.to_numeric(tbl.iloc[:, i], errors='coerce').dropna()
                            if len(colvals) > 0:
                                return str(colvals.iloc[-1])
                    firstcol = [normalize_label(str(x)) for x in tbl.iloc[:, 0].astype(str).tolist()]
                    for ridx, lab in enumerate(firstcol):
                        if q_norm in lab:
                            row = pd.to_numeric(tbl.iloc[ridx, :], errors='coerce').dropna()
                            if len(row) > 0:
                                return str(row.iloc[-1])
                except Exception:
                    continue
        return None

    def _ollama_complete(self, prompt):
        url = OLLAMA_URL + "/api/generate"
        payload = {"model": self.model, "prompt": prompt, "max_tokens": 300, "stream": True}
        try:
            with requests.post(url, json=payload, stream=True, timeout=300) as r:
                r.raise_for_status()
                response_text = ""
                for line in r.iter_lines():
                    if line:
                        try:
                            obj = json.loads(line.decode("utf-8"))
                            if "response" in obj:
                                response_text += obj["response"]
                            if obj.get("done", False):
                                break
                        except Exception:
                            continue
                return response_text.strip()
        except Exception as e:
            return f"Ollama error: {e}"

    def answer_query(self, query):
        s = self._structured_lookup(query)
        if s:
            return f"Answer from table: {s}"
        context = '\n'.join([item['text'] for item in self.embeddings_index[-5:]])
        prompt = f"Context:\n{context}\nQuestion: {query}\nAnswer concisely."
        return self._ollama_complete(prompt)
