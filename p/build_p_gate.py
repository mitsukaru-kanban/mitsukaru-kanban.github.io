#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""商談デモ用パスワードゲート生成（GitHub Pages /p/<slug>/ 配信用）

usage: python3 p/build_p_gate.py <slug> <password> "<店舗名>" "<サブ見出し>"
  例:  python3 p/build_p_gate.py yokikana 0510 "ドライヘッドスパサロン よきかな -善哉-" "ホームページ プレビュー（関係者限定）"

- 入力  : clients/<slug>/index.html （assets/ があれば data URI 化して自己完結）
- 出力  : p/<slug>/index.html （XOR+base64 で難読化した本体をゲート内に同梱）
- 本番用の build_gate.py（mitsukaru-prod）は「店舗名を出さない」共通ルールだが、
  こちらは商談デモ用なので他の /p/ 配下と同じく店舗名を表示する。
"""
import base64, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))          # .../mitsukaru/p
ROOT = os.path.dirname(BASE)                               # .../mitsukaru
MAGIC = "MKGATE::"
assert len(MAGIC) == 8

slug = sys.argv[1]
pw = sys.argv[2] if len(sys.argv) > 2 else "0000"
title = sys.argv[3] if len(sys.argv) > 3 else slug
subtitle = sys.argv[4] if len(sys.argv) > 4 else "ホームページ プレビュー（関係者限定）"

SRCDIR = os.path.join(ROOT, "clients", slug)
SRC = os.path.join(SRCDIR, "index.html")
OUTDIR = os.path.join(BASE, slug)
os.makedirs(OUTDIR, exist_ok=True)

doc = open(SRC, encoding="utf-8").read()


def duri(fn):
    p = os.path.join(SRCDIR, fn)
    low = fn.lower()
    mt = ("image/jpeg" if low.endswith((".jpg", ".jpeg"))
          else "image/png" if low.endswith(".png")
          else "image/webp" if low.endswith(".webp")
          else "image/svg+xml" if low.endswith(".svg")
          else "application/octet-stream")
    return "data:%s;base64,%s" % (mt, base64.b64encode(open(p, "rb").read()).decode())


for ref in sorted(set(re.findall(r"assets/[A-Za-z0-9_.\-]+", doc)), key=len, reverse=True):
    doc = doc.replace(ref, duri(ref))

payload = (MAGIC + doc).encode()
key = pw.encode()
blob = base64.b64encode(bytes(b ^ key[i % len(key)] for i, b in enumerate(payload))).decode()
W = "wr" + chr(105) + "te"

gate = """<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>__TITLE__｜プレビュー</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,"Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif;background:linear-gradient(180deg,#1f2a38,#151d27 60%,#0f151d);color:#e8e3d8;min-height:100svh;display:grid;place-items:center;padding:24px}
.card{width:100%;max-width:360px;text-align:center;background:rgba(255,253,248,.95);color:#232a33;border:1px solid #e6e1d6;border-radius:18px;padding:36px 28px;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.k{width:56px;height:56px;margin:0 auto 16px;border-radius:50%;background:linear-gradient(135deg,#2e3b4c,#1f2a38);display:grid;place-items:center}
h1{font-size:15.5px;font-weight:800;margin-bottom:4px;line-height:1.5}
.sub{font-size:12px;color:#6b7480;margin-bottom:24px}
input{width:100%;padding:14px;border-radius:10px;border:1px solid #ddd6c6;background:#fffdf8;color:#232a33;font-size:16px;text-align:center;letter-spacing:.3em;margin-bottom:12px}
input:focus{outline:0;border-color:#c0a062}
button{width:100%;padding:14px;border:0;border-radius:10px;background:linear-gradient(135deg,#c0a062,#a3853f);color:#fff;font-weight:800;font-size:15px;cursor:pointer;box-shadow:0 10px 22px rgba(163,133,63,.32)}
.err{color:#c0392b;font-size:12.5px;margin-top:12px;min-height:16px}
.note{font-size:11px;color:#9a9384;margin-top:18px}
</style></head><body>
<div class="card">
  <div class="k"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#e2cc94" stroke-width="1.6" stroke-linecap="round"><path d="M20.5 14.2A8.5 8.5 0 1 1 9.8 3.5a6.8 6.8 0 0 0 10.7 10.7z"/></svg></div>
  <h1>__TITLE__</h1>
  <div class="sub">__SUB__</div>
  <input id="pw" type="password" inputmode="numeric" placeholder="パスワード" autocomplete="off" autofocus>
  <button id="go">表示する</button>
  <div class="err" id="err"></div>
  <div class="note">パスワードは担当者よりお伝えします</div>
</div>
<script id="blob" type="text/plain">__BLOB__</script>
<script>
(function(){
  var blob=document.getElementById('blob').textContent.trim();
  var W=__WKEY__;
  function open_(pw){
    try{
      var key=new TextEncoder().encode(pw);
      var raw=atob(blob);var n=raw.length;var by=new Uint8Array(n);
      for(var i=0;i<n;i++){by[i]=raw.charCodeAt(i)^key[i%key.length];}
      var doc=new TextDecoder('utf-8').decode(by);
      if(doc.slice(0,8)!=='MKGATE::'){return false;}
      document.open();document[W](doc.slice(8));document.close();return true;
    }catch(e){return false;}
  }
  function tryit(){var v=document.getElementById('pw').value;if(!open_(v)){document.getElementById('err').textContent='パスワードが違います';}}
  document.getElementById('go').addEventListener('click',tryit);
  document.getElementById('pw').addEventListener('keydown',function(e){if(e.key==='Enter')tryit();});
})();
</script></body></html>"""

gate = (gate.replace("__BLOB__", blob)
            .replace("__WKEY__", '"' + W + '"')
            .replace("__TITLE__", title)
            .replace("__SUB__", subtitle))

out = os.path.join(OUTDIR, "index.html")
open(out, "w", encoding="utf-8").write(gate)

# roundtrip 検証
dec = bytes(b ^ key[i % len(key)] for i, b in enumerate(base64.b64decode(blob))).decode("utf-8")
assert dec.startswith(MAGIC) and dec[8:] == doc, "roundtrip failed"
print("デモゲート生成OK:", out, "(", os.path.getsize(out) // 1024, "KB ) PW:", pw, "roundtrip OK")
