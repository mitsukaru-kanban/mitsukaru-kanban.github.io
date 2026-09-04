#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""みつかる看板 診断LP v2（/check2/）ビルド
- 商談4件（受注2/失注1/提出1）の実データを反映した構成
- 画像は data URI で自己完結
"""
# ⚠️ 2026-09-04: check3/index.html は本スクリプトの出力後に直接手修正済み
#   （フォーム2段階化＝1段目 店舗名/氏名/電話・2段目 任意補足／ヒーロー画像・比較スマホ画面タップで診断へ）。
#   このスクリプトを再実行すると手修正が消える。再ビルドが必要な場合は index.html 側を正とすること。
import re, base64, pathlib

M    = pathlib.Path("/Users/fumiya/Desktop/GENERAL LINK_ALL/07_プロジェクト管理/新規事業/mitsukaru")
SP   = pathlib.Path("/private/tmp/claude-501/-Users-fumiya-Desktop-GENERAL-LINK-ALL/0ab78caf-af71-4f83-a957-3ce3046ea63a/scratchpad")
SHOT = SP / "fake"
OUT  = M / "check3" / "index.html"

def b64(p):
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()

# FVは生成画像（店主がスマホで自分の店を見ている画）
hero = b64(SP / "gen" / "fv_owner.jpg")

SHOT_IZAKAYA = b64(SHOT / "izakaya.jpg")
SHOT_SALON   = b64(SHOT / "salon.jpg")
SHOT_ESTE    = b64(SHOT / "este.jpg")

CSS = """
:root{--teal:#0fb5a6;--teal-d:#0a8f83;--ink:#232a2b;--ink-2:#5d6a6b;--paper:#f6f8f7;--orange:#ff7a2f;--orange-d:#e05e17;--yellow:#ffd21e;--line:#e3ebe9}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:"Noto Sans JP",sans-serif;color:var(--ink);background:#fff;line-height:1.95;-webkit-font-smoothing:antialiased;padding-bottom:76px}
img{max-width:100%;display:block}
.wrap{width:100%;max-width:640px;margin:0 auto;padding:0 20px}
.serif{font-family:"Noto Serif JP",serif}
.mark{background:linear-gradient(transparent 60%,var(--yellow) 60%);font-weight:700}
.tealc{color:var(--teal-d)}
.top{border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(255,255,255,.96);backdrop-filter:blur(6px);z-index:40}
.top .row{max-width:640px;margin:0 auto;padding:9px 20px;display:flex;align-items:center;justify-content:space-between}
.top .lg{display:flex;align-items:center;gap:8px;font-weight:900;font-size:14px}
.top .lg .k{background:var(--teal);color:#fff;width:26px;height:26px;border-radius:7px;display:grid;place-items:center;font-size:14px}
.pr{font-size:10px;color:#98a5a3;border:1px solid var(--line);border-radius:4px;padding:2px 7px;letter-spacing:.08em}
.ahead{padding:26px 0 6px}
.cat{color:var(--teal-d);font-weight:900;font-size:12px;letter-spacing:.1em;margin-bottom:12px}
h1{font-family:"Noto Serif JP",serif;font-weight:900;font-size:clamp(24px,6.6vw,33px);line-height:1.5}
.dek{margin-top:16px;font-size:15px;color:#475252;font-weight:500}
.byline{margin-top:16px;font-size:12px;color:#98a5a3;display:flex;gap:10px;align-items:center;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:10px 0}
.hero-img{margin:20px 0 6px;border-radius:12px;overflow:hidden}
.cap{font-size:11.5px;color:#98a5a3;margin-top:7px;text-align:center}
.body{padding:8px 0 10px}
.body p{margin:18px 0;font-size:16px;line-height:2.05}
.lead-p{font-size:16.5px;font-weight:500}
.h2{font-family:"Noto Serif JP",serif;font-weight:900;font-size:clamp(20px,5.2vw,25px);line-height:1.6;margin:40px 0 6px;padding-left:14px;border-left:5px solid var(--teal)}
.pull{margin:26px 0;padding:20px 22px;background:var(--paper);border-radius:12px;border-left:4px solid var(--orange);font-weight:700;font-size:16.5px;line-height:1.9}

/* 検索の瞬間 */
.cmp{margin:26px 0}
.cmp .lead{text-align:center;font-size:13px;font-weight:800;color:var(--teal-d);margin-bottom:14px}
.phone{max-width:330px;margin:0 auto;background:#eef3f2;border:7px solid #20302f;border-radius:30px;padding:12px 12px 16px}
.psearch{display:flex;align-items:center;gap:8px;background:#fff;border-radius:999px;padding:9px 14px;font-size:13px;font-weight:700;color:#48555a;margin-bottom:12px}
.psearch .mg{margin-left:auto;color:#9aa7a6}
.pcard{position:relative;display:flex;gap:11px;background:#fff;border-radius:14px;padding:11px;margin-bottom:11px;align-items:center}
.pcard.skip{border:1.5px dashed #d4a3a0}
.pcard.pick{border:2px solid var(--teal);box-shadow:0 8px 20px rgba(15,181,166,.2)}
.pthumb{flex:0 0 auto;width:62px;height:62px;border-radius:10px;background:linear-gradient(135deg,#12b3a4,#0a8f83);display:grid;place-items:center;font-size:26px}
.pthumb.none{background:repeating-linear-gradient(45deg,#eceff0,#eceff0 6px,#e2e6e7 6px,#e2e6e7 12px);color:#a7b1b1;font-size:10px;font-weight:800;text-align:center;line-height:1.3}
.pinfo{flex:1;min-width:0}
.pname{font-size:14.5px;font-weight:900}
.pmeta{font-size:12px;font-weight:700;margin-top:3px}.pmeta.gray{color:#a7b1b1}.pmeta .star{color:#ffb300}.pmeta .cnt{color:#5d6a6b}
.pno{font-size:11px;color:#c98c88;font-weight:700;margin-top:4px}
.pbtn{display:inline-block;margin-top:6px;background:var(--teal);color:#fff;font-size:11.5px;font-weight:800;padding:5px 12px;border-radius:999px}
.ptag{position:absolute;top:-9px;right:10px;font-size:11px;font-weight:900;padding:3px 10px;border-radius:999px}
.skiptag{background:#f0d3d1;color:#b4504a}.picktag{background:var(--orange);color:#fff}
.cmpnote{max-width:360px;margin:16px auto 0;font-size:13.5px;line-height:1.9;color:#475252;font-weight:600}
.cmpnote .x{color:#c0392b;font-weight:900}.cmpnote .o{color:var(--teal-d);font-weight:900}

/* 診断 */
.quiz{margin:30px 0;background:linear-gradient(160deg,#effbf9,#e6f7f3);border:2px solid #cdeee9;border-radius:18px;padding:24px 20px}
.quiz .qh{text-align:center;margin-bottom:6px}
.quiz .qh .badge{display:inline-block;background:var(--teal);color:#fff;font-weight:900;font-size:12px;padding:5px 14px;border-radius:999px;margin-bottom:10px}
.quiz .qh h3{font-family:"Noto Serif JP",serif;font-size:20px;color:var(--ink);line-height:1.5}
.quiz .prog{display:flex;gap:5px;justify-content:center;margin:14px 0 18px}
.quiz .prog i{width:26px;height:4px;border-radius:2px;background:#cfe6e1}
.quiz .prog i.on{background:var(--teal)}
.q{display:none}
.q.on{display:block;animation:fade .3s ease}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.q .qn{font-size:12px;font-weight:800;color:var(--teal-d);margin-bottom:6px}
.q .qt{font-size:17px;font-weight:900;line-height:1.5;margin-bottom:14px}
.qopts{display:grid;gap:9px}
.qopt{background:#fff;border:2px solid #d7ece7;border-radius:12px;padding:14px 15px;font-size:15px;font-weight:700;text-align:left;cursor:pointer;display:flex;align-items:center;gap:10px;transition:.15s;font-family:inherit;color:inherit;line-height:1.6}
.qopt::before{content:"";width:18px;height:18px;border-radius:50%;border:2px solid #bcd8d2;flex:0 0 auto}
.qopt:active{transform:scale(.99)}
.qopt.sel{border-color:var(--teal);background:#f0fbf9}
.qopt.sel::before{border-color:var(--teal);background:var(--teal);box-shadow:inset 0 0 0 3px #fff}
.result{display:none;margin-top:18px;background:#fff;border-radius:14px;padding:22px 18px;box-shadow:0 10px 26px rgba(10,90,85,.1)}
.result.on{display:block;animation:fade .4s ease}
.result .rc{font-size:15px;font-weight:800;text-align:center;margin-bottom:12px}
.result .rc b{color:var(--orange);font-size:34px;vertical-align:-4px;font-family:"Noto Serif JP",serif}
.rlist{display:grid;gap:8px;margin-bottom:14px}
.rli{display:flex;gap:9px;align-items:flex-start;background:#fff6f0;border:1px solid #ffdcc6;border-radius:10px;padding:11px 13px;font-size:13.5px;font-weight:700;line-height:1.75;color:#8a4a1e}
.rli.ok{background:#f1faf8;border-color:#cfe9e4;color:#3d6a64}
.rli i{flex:0 0 auto;font-style:normal;font-weight:900}
.result .rmsg{font-size:14.5px;color:#475252;line-height:1.9;margin-bottom:16px;text-align:center}
.result .rgo{display:block;text-align:center;background:linear-gradient(180deg,#ff934f,var(--orange));color:#fff;font-weight:900;font-size:15.5px;padding:15px 20px;border-radius:12px;text-decoration:none;box-shadow:0 4px 0 var(--orange-d);line-height:1.5}
.result .rgo span{display:block;font-size:11.5px;font-weight:800;opacity:.95}

/* 丸投げの中身 */
.todo{display:grid;gap:9px;margin:20px 0 6px}
.ti{display:flex;gap:11px;align-items:flex-start;background:var(--paper);border-radius:11px;padding:13px 15px;font-size:14.5px;font-weight:700;line-height:1.75}
.ti i{flex:0 0 auto;width:22px;height:22px;border-radius:50%;background:var(--teal);color:#fff;font-style:normal;font-size:12px;font-weight:900;display:grid;place-items:center;margin-top:3px}
.ti span{display:block;font-size:12.5px;color:#5d6a6b;font-weight:500;margin-top:2px}

/* 実物Before/After */
.bawrap{margin:24px 0 6px}
.bahint{text-align:center;font-size:11.5px;color:#98a5a3;margin-bottom:12px}
.bacar{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px 2px 12px;scrollbar-width:none}
.bacar::-webkit-scrollbar{display:none}
.baslide{flex:0 0 100%;scroll-snap-align:center;background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:16px 14px}
.bahd{text-align:center;font-size:13px;font-weight:900;margin-bottom:12px}
.bahd span{background:#eafaf7;color:var(--teal-d);border-radius:999px;padding:3px 12px;font-size:12px}
.bapair{display:flex;align-items:center;justify-content:center;gap:8px}
.bacol{flex:1;min-width:0;text-align:center}
.balbl{font-size:11px;font-weight:900;border-radius:6px;padding:3px 0;margin-bottom:6px}
.balbl.now{background:#eef1f1;color:#8a9694}.balbl.aft{background:var(--teal);color:#fff}
.baarw{flex:0 0 auto;color:var(--orange);font-weight:900;font-size:22px}
.pmlink{display:block;text-decoration:none;color:inherit}
.pm2{position:relative;border:4px solid #15181a;border-radius:16px;overflow:hidden;background:#fff;aspect-ratio:9/17;display:flex;flex-direction:column;box-shadow:0 10px 24px rgba(0,20,18,.22);text-align:left}
.pm2 .notch{position:absolute;top:3px;left:50%;transform:translateX(-50%);width:30%;height:7px;background:#15181a;border-radius:5px;z-index:4}
.pm2 .sb{display:flex;justify-content:space-between;padding:4px 8px 2px;font-size:6.5px;font-weight:800;color:#20302e;position:relative;z-index:3}
.pm2.shot{background:#111}
.pm2.shot img{width:100%;height:100%;object-fit:cover;object-position:top center;position:absolute;inset:0}
.pm2.sad{background:#fbfbf9;filter:grayscale(.3)}
.pm2.sad .ob{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:10px;gap:5px}
.pm2.sad .onm{font-family:"Noto Serif JP",serif;font-size:10px;color:#6a6a6a}
.pm2.sad .ohr{width:44%;height:1px;background:#d5d5d2}
.pm2.sad .otx{font-size:6.5px;color:#9a9a97;line-height:1.7;font-weight:600}
.pm2.sad .onote{font-size:6.5px;color:#b0736a;font-weight:800;margin-top:3px}
.baimgnote{text-align:center;font-size:11.5px;color:#98a5a3;margin-top:10px;line-height:1.8}

/* 約束しないこと */
.honest{margin:26px 0 6px;background:#fffdf5;border:2px solid #f2e3b8;border-radius:16px;padding:22px 20px}
.honest .ht{font-family:"Noto Serif JP",serif;font-weight:900;font-size:18px;margin-bottom:14px;line-height:1.6}
.honest ul{list-style:none;display:grid;gap:11px}
.honest li{display:flex;gap:10px;font-size:14.5px;font-weight:600;line-height:1.8;color:#4a4636}
.honest li i{flex:0 0 auto;font-style:normal;color:#c98a12;font-weight:900}
.honest .hf{margin-top:14px;padding-top:13px;border-top:1px dashed #e6d5a8;font-size:14.5px;font-weight:800;line-height:1.85;color:#7a5c10}

/* レポート */
.rep{display:flex;gap:14px;align-items:center;background:var(--paper);border-radius:14px;padding:18px 18px;margin:20px 0 6px}
.rep .rn{flex:0 0 auto;width:52px;height:52px;border-radius:13px;background:var(--teal);color:#fff;display:grid;place-items:center;font-size:24px}
.rep b{font-size:15.5px;display:block}
.rep span{font-size:13px;color:#5d6a6b;font-weight:500;line-height:1.8;display:block;margin-top:3px}

.whys{display:grid;gap:11px;max-width:560px;margin:16px auto 0}
.wc{display:flex;gap:13px;align-items:flex-start;background:var(--paper);border-radius:12px;padding:15px 16px}
.wc .wn{flex:0 0 auto;width:34px;height:34px;border-radius:9px;background:var(--orange);color:#fff;font-weight:900;display:grid;place-items:center;font-family:"Noto Serif JP",serif}
.wc b{font-size:15px}.wc span{display:block;font-size:13px;color:#5d6a6b;font-weight:500;margin-top:3px;line-height:1.75}
.qa{margin:30px 0 6px}.qs{display:grid;gap:10px;margin-top:16px}
.qbox{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:15px 16px}
.qbox .q2{font-size:15px;font-weight:900;display:flex;gap:8px;line-height:1.6}.qbox .q2 .mk{color:var(--teal-d)}
.qbox .a{font-size:14px;color:#475252;margin-top:8px;display:flex;gap:8px;line-height:1.85}.qbox .a .mk{color:var(--orange);font-weight:900}

.offer{margin:34px 0 8px;background:linear-gradient(160deg,#16c3b4,var(--teal-d));color:#fff;border-radius:18px;padding:30px 22px;text-align:center;box-shadow:0 16px 40px rgba(10,120,110,.28)}
.offer .t{font-family:"Noto Serif JP",serif;font-weight:900;font-size:20px;margin-bottom:6px;line-height:1.6}
.offer .t2{font-size:13.5px;font-weight:600;opacity:.95;margin-bottom:16px}
.offer .price{display:inline-flex;align-items:baseline;gap:6px;background:#fff;color:var(--ink);border-radius:14px;padding:14px 24px}
.offer .price .z{font-family:"Noto Serif JP",serif;font-size:40px;font-weight:900;color:var(--orange);line-height:1}
.offer .price .s{font-size:12px;font-weight:800;color:#5d6a6b}.offer .price .m{font-size:17px;font-weight:900}
.offer .sub{margin-top:12px;font-size:14px;line-height:1.8}.offer .chips{margin-top:16px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.offer .chips span{background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.5);border-radius:999px;font-size:12.5px;font-weight:800;padding:6px 13px}

.formsec{margin:30px 0 10px;background:var(--paper);border-radius:18px;padding:26px 20px}
.formsec h2{font-family:"Noto Serif JP",serif;font-weight:900;font-size:20px;text-align:center;line-height:1.6;margin-bottom:6px;border:0;padding:0}
.formsec .fl{text-align:center;font-size:14px;color:#475252;margin-bottom:20px;line-height:1.85}
.af{margin-bottom:14px}.af label{display:block;font-size:13.5px;font-weight:800;margin-bottom:6px}
.af .req{color:#fff;background:var(--orange);font-size:10.5px;font-weight:800;border-radius:4px;padding:2px 7px;margin-left:6px}
.af input{width:100%;padding:14px;border:1.5px solid var(--line);border-radius:10px;font-size:16px;background:#fff;font-family:inherit}
.af input:focus{outline:0;border-color:var(--teal)}
.af select{width:100%;padding:14px 38px 14px 14px;border:1.5px solid var(--line);border-radius:10px;font-size:16px;background:#fff url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='9' viewBox='0 0 14 9'><path d='M1 1l6 6 6-6' stroke='%235d6a6b' stroke-width='2' fill='none' stroke-linecap='round'/></svg>") no-repeat right 14px center;color:var(--ink);-webkit-appearance:none;appearance:none;font-family:inherit}
.af select:focus{outline:0;border-color:var(--teal)}.af select:invalid{color:#9aa7a6}
.agree{display:flex;gap:9px;align-items:flex-start;font-size:13px;color:#475252;margin:6px 0 16px;line-height:1.6}
.agree input{margin-top:3px;transform:scale(1.2)}.agree a{color:var(--teal-d);text-decoration:underline}
.submit{width:100%;border:0;border-radius:12px;padding:17px;background:linear-gradient(180deg,#ff924f,var(--orange));color:#fff;font-weight:900;font-size:17px;cursor:pointer;box-shadow:0 6px 0 var(--orange-d);font-family:inherit;line-height:1.5}
.submit .s{display:block;font-size:12px;font-weight:800;opacity:.95;margin-bottom:2px}
.aor{text-align:center;font-size:12.5px;color:#7d8887;margin-top:12px;line-height:1.8}
.aerr{color:#d33;font-size:13px;margin-top:10px;text-align:center}
.thanks{display:none;text-align:center;padding:14px 0}
.thanks .ic{width:60px;height:60px;border-radius:50%;background:var(--teal);color:#fff;font-size:32px;display:grid;place-items:center;margin:0 auto 14px}
.thanks h3{font-size:20px;font-weight:900;margin-bottom:8px}.thanks p{font-size:14.5px;color:#475252}
.tbook{display:block;margin:18px auto 10px;max-width:420px;background:linear-gradient(180deg,#ff934f,var(--orange));color:#fff;font-weight:900;font-size:16.5px;padding:16px 20px;border-radius:12px;text-decoration:none;box-shadow:0 5px 0 var(--orange-d);line-height:1.45}
.tbook span{display:block;font-size:11.5px;font-weight:800;opacity:.95}
.tnote{font-size:12.5px!important;color:#7d8887!important;line-height:1.8}
footer{margin-top:36px;background:#1b2726;color:#c6d3d1;text-align:center;padding:28px 20px;font-size:12px;line-height:1.9}
footer .fl{font-weight:900;color:#fff;font-size:15px;margin-bottom:6px}footer a{color:#8fe0d8;text-decoration:none}
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:50;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border-top:1px solid var(--line);padding:9px 16px;box-shadow:0 -4px 16px rgba(0,0,0,.06)}
.sticky a{display:block;max-width:600px;margin:0 auto;text-align:center;background:linear-gradient(180deg,#ff924f,var(--orange));color:#fff;font-weight:900;font-size:16px;padding:13px;border-radius:12px;text-decoration:none;box-shadow:0 4px 0 var(--orange-d);line-height:1.4}
.sticky a span{display:block;font-size:11px;font-weight:800;opacity:.95}
"""

def slide(label, img, sadname, sadtel, note):
    return f"""<div class="baslide"><div class="bahd"><span>{label}</span></div><div class="bapair">
      <div class="bacol"><div class="balbl now">今</div>
        <div class="pm2 sad"><div class="notch"></div><div class="sb"><span>9:41</span><span>●●● ▮</span></div>
          <div class="ob"><div class="onm">{sadname}</div><div class="ohr"></div><div class="otx">営業中<br>TEL {sadtel}</div><div class="onote">※ホームページは<br>準備中です</div></div></div></div>
      <div class="baarw">→</div>
      <div class="bacol"><div class="balbl aft">みつかる看板なら</div>
        <a href="#cta" class="pmlink"><div class="pm2 shot"><div class="notch"></div><img src="{img}" alt="{note}" loading="lazy"></div></a></div>
    </div></div>"""

HTML = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>30秒セルフチェック｜あなたのお店の"今"、ネットに出ていますか？</title>
<meta name="description" content="3つの質問でわかる、あなたのお店のネットでの見え方。順位ではなく「今のお店の姿」が出ているか。HP・Google・口コミをまるっと丸投げ、初月0円。">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5TNWZ6KWBR"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-5TNWZ6KWBR');</script>
<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','1042398057799719');fbq('track','PageView');</script>
<noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id=1042398057799719&ev=PageView&noscript=1"/></noscript>
<script type="text/javascript">(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)}})(window,document,"clarity","script","xjj6mi73w2");</script>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Noto+Serif+JP:wght@600;700;900&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<div class="top"><div class="row">
  <div class="lg"><span class="k">看</span>みつかる看板</div><span class="pr">PR</span>
</div></div>

<article class="wrap">
  <div class="ahead">
    <div class="cat">30秒セルフチェック</div>
    <h1>あなたのお店の"今"は、<br>ネットに<span class="tealc">出ていますか？</span></h1>
    <p class="dek">検索順位より、大事なこと。——3つの質問で、お店の「見え方のズレ」がわかります。</p>
    <div class="byline"><span>みつかる看板 編集部</span><span>｜</span><span>地域集客のはなし</span></div>
  </div>
  <div class="hero-img"><img src="{hero}" alt="開店前の店内でスマートフォンを見る店主"></div>
  <p class="cap">お客さんが見ているのは、お店ではなく「ネットに出ているお店の姿」。</p>

  <div class="body">
    <p class="lead-p">スマホで「近くの居酒屋」「近くの焼き鳥」と検索する。表示された数店を、お客さんはたった数十秒で見比べて、<b>1店だけ</b>を選びます。</p>
    <p>そのとき見られているのは、順位ではありません。<span class="mark">今のお店の姿</span>——写真は最近のものか、メニューは今のものか、声にちゃんと応えているか。<b>実際のお店は良いのに、ネット上だけ何年も前で止まっている</b>。これが、いちばん多い取りこぼしです。</p>

    <div class="cmp">
      <div class="lead">＜ 検索されたその瞬間に、起きていること ＞</div>
      <div class="phone">
        <div class="psearch"><span>🔍</span>近くの居酒屋<span class="mg">✕</span></div>
        <div class="pcard skip"><div class="pthumb none">写真<br>なし</div><div class="pinfo"><div class="pname">居酒屋 △△△</div><div class="pmeta gray">情報が古い・写真がない</div><div class="pno">予約ボタンなし</div></div><span class="ptag skiptag">スルー →</span></div>
        <div class="pcard pick"><div class="pthumb">🍶</div><div class="pinfo"><div class="pname">炭火焼き ◯◯</div><div class="pmeta"><span class="star">★★★★★</span> <span class="cnt">4.8（62件）</span></div><div class="pbtn">予約する</div></div><span class="ptag picktag">👆 ここにしよ</span></div>
      </div>
      <div class="cmpnote"><span class="x">✕</span> 情報が古いお店は、<b>見られても、そのまま離脱</b>。<br><span class="o">◎</span> 今の姿がちゃんと出ているお店へ、お客さんは静かに流れていきます。</div>
    </div>

    <h2 class="h2">では、あなたのお店は？</h2>
    <p>下の3つの質問に答えるだけ。あなたのお店の「ネット上の見え方」が、その場でわかります。</p>

    <div class="quiz" id="quiz">
      <div class="qh"><span class="badge">SELF CHECK</span><h3>あなたのお店の<br>見え方チェック</h3></div>
      <div class="prog" id="prog"><i class="on"></i><i></i><i></i></div>

      <div class="q on" data-q="q1" data-key="HP">
        <div class="qn">QUESTION 1 / 3</div>
        <div class="qt"><span class="mark">ホームページ</span>の内容は、今のメニュー・サービスと合っていますか？</div>
        <div class="qopts">
          <button class="qopt" type="button" data-weak="0" data-a="HPは最新">合っている（最近直した）</button>
          <button class="qopt" type="button" data-weak="1" data-a="HPが古い">あるけど、何年も直していない</button>
          <button class="qopt" type="button" data-weak="1" data-a="HPなし">そもそもホームページがない</button>
        </div>
      </div>
      <div class="q" data-q="q2" data-key="写真">
        <div class="qn">QUESTION 2 / 3</div>
        <div class="qt">ネットに出ている<span class="mark">お店の写真</span>は、1年以内のものですか？</div>
        <div class="qopts">
          <button class="qopt" type="button" data-weak="0" data-a="写真は最新">最近の写真が何枚もある</button>
          <button class="qopt" type="button" data-weak="1" data-a="写真が古い">数枚だけ・何年か前のもの</button>
          <button class="qopt" type="button" data-weak="1" data-a="写真なし">ほとんど載っていない</button>
        </div>
      </div>
      <div class="q" data-q="q3" data-key="口コミ">
        <div class="qn">QUESTION 3 / 3</div>
        <div class="qt">お客さんからの<span class="mark">評価・口コミ</span>に、返信できていますか？</div>
        <div class="qopts">
          <button class="qopt" type="button" data-weak="0" data-a="口コミ返信できている">できている</button>
          <button class="qopt" type="button" data-weak="1" data-a="低評価を放置">たまに。低い評価は放置してしまう</button>
          <button class="qopt" type="button" data-weak="1" data-a="口コミ未対応">ほとんど見ていない／口コミ自体が少ない</button>
        </div>
      </div>

      <div class="result" id="result">
        <div class="rc">3つのうち <b id="rcount">0</b> つ、ネットとお店にズレがありました</div>
        <div class="rlist" id="rlist"></div>
        <div class="rmsg" id="rmsg"></div>
        <a class="rgo" href="#cta"><span>＼ 見てから決めてOK ／</span>無料で、お店のHP案をつくってもらう →</a>
      </div>
    </div>

    <h2 class="h2">直すのは「順位」じゃなく、「見え方」。</h2>
    <p>やることは派手ではありません。<b>お店の"今"を、ネット上にそのまま出す</b>。それだけです。ただ、本業の合間に全部やるのは無理なので——<span class="mark">ぜんぶ、こちらでやります。</span></p>

    <div class="todo">
      <div class="ti"><i>1</i><div><b>ホームページを1枚つくります</b><span>写真えらび・文章づくりまで。スマホで見やすい形に。</span></div></div>
      <div class="ti"><i>2</i><div><b>Googleマップの情報を整えます</b><span>営業時間・写真・メニュー・予約ボタンまで設定します。</span></div></div>
      <div class="ti"><i>3</i><div><b>写真を、今のお店の状態に差し替えます</b><span>お手元の写真をLINEやメールで送ってもらうだけでOK。</span></div></div>
      <div class="ti"><i>4</i><div><b>口コミが自然に増える仕組みを置きます</b><span>来店したお客様が、その場で書きやすい形にします。</span></div></div>
      <div class="ti"><i>5</i><div><b>予約は、今お使いのものにつなぎます</b><span>食べログ・ホットペッパー・電話。乗り換えは不要です。</span></div></div>
      <div class="ti"><i>6</i><div><b>毎月、簡単なレポートをお送りします</b><span>何人に見られたか、電話が何回押されたか。</span></div></div>
    </div>

    <h2 class="h2">たとえば、こんな形に。</h2>
    <p>デザインは、お店の雰囲気に合わせて一軒ずつ変えています。下は制作イメージです。</p>
    <div class="bawrap"><div class="bahint">← スワイプで他の業種も見られます →</div><div class="bacar">
      {slide("居酒屋・飲食店", SHOT_IZAKAYA, "居酒屋 △△", "075-XXX-XXXX", "居酒屋のホームページ例")}
      {slide("美容室・サロン", SHOT_SALON, "hair △△", "092-XXX-XXXX", "美容室のホームページ例")}
      {slide("エステ・整体", SHOT_ESTE, "△△サロン", "088-XXX-XXXX", "サロンのホームページ例")}
    </div>
    <p class="baimgnote">※制作イメージです。掲載している店名・写真・電話番号はすべて架空のもので、実在の店舗ではありません。<br>タップすると、無料のHP案づくりのお申し込みへ進みます。</p></div>

    <div class="honest">
      <div class="ht">先に、お約束できないことを<br>書いておきます。</div>
      <ul>
        <li><i>×</i><span>検索で1位になることは、保証できません。順位はGoogleが決めるものだからです。</span></li>
        <li><i>×</i><span>口コミを買ったり、良い評価の人にだけ声をかける仕組みは使いません。<b>Googleの規約違反で、お店のアカウントが止まるリスクがある</b>からです。</span></li>
        <li><i>×</i><span>「すぐにお客様が増えます」とは言いません。</span></li>
      </ul>
      <div class="hf">やるのは、<b>見つけてもらえた時に、選ばれる状態を整えること</b>。それだけを、月々の金額の中で続けます。</div>
    </div>

    <h2 class="h2">続けるかどうかは、毎月の数字で。</h2>
    <div class="rep"><div class="rn">📈</div><div><b>毎月、1枚のレポートをお送りします</b><span>ホームページが何人に見られたか、Googleマップから何回電話が押されたか。実際に測れた数字だけをお出しします。効果を大きく見せるための計算はしません。</span></div></div>
  </div>

  <div class="offer">
    <div class="t">まずは、あなたのお店のHPを<br>1枚、無料でおつくりします。</div>
    <div class="t2">見てから、続けるかどうか決めてください。</div>
    <div class="price"><span class="s">初月</span><span class="z">0</span><span class="m">円</span></div>
    <div class="sub">2ヶ月目〜 月9,000円（税抜）／税込9,900円<br>初期費用0円</div>
    <div class="chips"><span>初期費用0円</span><span>しばりなし</span><span>設定ぜんぶおまかせ</span></div>
  </div>

  <section class="wrap" style="padding:0">
    <div class="h2" style="margin-top:34px">なぜ、この価格でできるの？</div>
    <div class="whys">
      <div class="wc"><span class="wn">1</span><div><b>ぜんぶ自社で内製</b><span>制作も運用も外注しないから、中間マージンがのりません。</span></div></div>
      <div class="wc"><span class="wn">2</span><div><b>決まった型で効率化</b><span>ムダをなくし、浮いたコストを価格に還元しています。</span></div></div>
      <div class="wc"><span class="wn">3</span><div><b>初月0円は自信の裏返し</b><span>まず使って納得してもらえれば、続けてもらえるから。</span></div></div>
    </div>
  </section>

  <section class="qa">
    <div class="h2">よくあるご質問</div>
    <div class="qs">
      <div class="qbox"><div class="q2"><span class="mk">Q.</span>今のホームページは、作り直しになりますか？</div><div class="a"><span class="mk">A.</span>作り直します（無料の試作をご覧いただいてから判断でOK）。今のページを活かしたい場合は、そのまま整えることもできます。</div></div>
      <div class="qbox"><div class="q2"><span class="mk">Q.</span>予約は食べログ／ホットペッパーのままで大丈夫？</div><div class="a"><span class="mk">A.</span>そのままで大丈夫です。今お使いの予約や電話に、ボタンでつなぐだけ。乗り換えはお願いしません。</div></div>
      <div class="qbox"><div class="q2"><span class="mk">Q.</span>パソコンが苦手なのですが。</div><div class="a"><span class="mk">A.</span>お店の写真とメニューを送っていただくだけで大丈夫です。設定も更新も、こちらで行います。</div></div>
      <div class="qbox"><div class="q2"><span class="mk">Q.</span>しつこく営業されませんか？</div><div class="a"><span class="mk">A.</span>しません。無理な勧誘は一切いたしません。</div></div>
      <div class="qbox"><div class="q2"><span class="mk">Q.</span>途中でやめられますか？</div><div class="a"><span class="mk">A.</span>はい、しばりなし。いつでも解約OK（違約金なし）。</div></div>
      <div class="qbox"><div class="q2"><span class="mk">Q.</span>初月0円のあとは？</div><div class="a"><span class="mk">A.</span>2ヶ月目から 月9,000円（税抜／税込9,900円）。初期費用0円です。</div></div>
    </div>
  </section>

  <div class="formsec" id="cta">
    <h2>まずは、無料のHP案から。</h2>
    <p class="fl">お店の情報をいただければ、こちらでHPの下書きを1枚おつくりしてお見せします。<br><b>見てから、続けるかどうかを決めてください。</b>無理な勧誘・しつこい営業はしません。</p>
    <form id="f" action="https://docs.google.com/forms/d/e/1FAIpQLSfLGuCYqNFj9br0vH36ohGWwiwXDo-ADk1X47Nq7dhaSzbR4w/formResponse" method="POST" target="gsink" novalidate>
      <div class="af"><label for="s1">店舗名<span class="req">必須</span></label><input id="s1" name="entry.1032007495" type="text" required placeholder="例）〇〇整体院／〇〇食堂"></div>
      <div class="af"><label for="biz">業種<span class="req">必須</span></label><select id="biz" required>
        <option value="" disabled selected>選択してください</option>
        <option>居酒屋・飲食店</option><option>美容室・ネイル・まつげ</option><option>エステ・リラクゼーション</option>
        <option>整体・整骨院・鍼灸</option><option>学習塾・教室・スクール</option><option>クリニック・歯科</option>
        <option>士業・専門サービス</option><option>物販・小売</option><option>その他</option></select></div>
      <div class="af"><label for="area">お店のエリア<span class="req">必須</span></label><input id="area" type="text" required placeholder="例）大阪市／世田谷区／福岡市中央区"></div>
      <div class="af"><label for="s2">お名前<span class="req">必須</span></label><input id="s2" name="entry.1182576338" type="text" required placeholder="例）山田 太郎"></div>
      <div class="af"><label for="s3">お電話番号<span class="req">必須</span></label><input id="s3" name="entry.1616360026" type="tel" inputmode="tel" required placeholder="例）090-1234-5678"></div>
      <div class="af"><label for="s4">メールアドレス<span class="req">必須</span></label><input id="s4" name="entry.1218551347" type="email" inputmode="email" required placeholder="例）info@example.com"></div>
      <div class="af"><label for="s5">連絡がつきやすい時間帯<span class="req">必須</span></label><select id="s5" name="entry.1420388143" required><option value="" disabled selected>選択してください</option><option>平日 午前（9〜12時）</option><option>平日 午後（12〜17時）</option><option>平日 夜（17〜20時）</option><option>土日祝</option><option>いつでもOK</option></select></div>
      <input type="hidden" id="srcmemo" name="entry.1202707729" value="みつかる看板_診断LP3">
      <input type="hidden" name="entry.1561297601" value="上記に同意します">
      <input type="hidden" name="fvv" value="1"><input type="hidden" name="pageHistory" value="0">
      <label class="agree"><input id="agree" type="checkbox" required><span><a href="../privacy.html" target="_blank" rel="noopener">プライバシーポリシー</a>・<a href="../terms.html" target="_blank" rel="noopener">利用規約</a>に同意のうえ送信します（必須）</span></label>
      <button type="submit" class="submit"><span class="s">＼ 無料・見てから決めてOK ／</span>お店のHP案をつくってもらう →</button>
      <div class="aerr" id="err" hidden>未入力の必須項目があります。ご確認ください。</div>
      <p class="aor">無料の試作をご覧いただいてからのご判断でOKです。<br>しつこい営業はしません。</p>
    </form>
    <div class="thanks" id="thanks"><div class="ic">✓</div><h3>ありがとうございます！</h3>
      <p>このまま、打ち合わせの日程を<br>押さえていただけます。</p>
      <a class="tbook" id="tbook" href="https://timerex.net/s/s-sudo_482b/4cc88797/" target="_blank" rel="noopener"><span>＼ 空いている時間から選ぶだけ ／</span>日程を選ぶ →</a>
      <p class="tnote">お急ぎでなければ、担当より折り返しご連絡いたします。<br>お店のHP案づくりについて、詳しくご案内します。</p></div>
  </div>
  <iframe name="gsink" style="display:none" title="送信先" tabindex="-1" aria-hidden="true"></iframe>
</article>

<footer>
  <div class="fl">みつかる看板</div>
  お店がネットで見つかる・選ばれる、まるっとおまかせパック<br>
  初月0円／2ヶ月目〜 月9,000円（税抜・税込9,900円）／初期費用0円<br><br>提供：株式会社XseedLab<br>
  <a href="../privacy.html" target="_blank" rel="noopener">プライバシーポリシー</a>　｜　<a href="../terms.html" target="_blank" rel="noopener">利用規約</a>
</footer>

<div class="sticky"><a href="#cta"><span>＼ 見てから決めてOK ／</span>無料でHP案をつくる →</a></div>

<script>
(function(){{
  var VARIANT='check3';
  var WEAKTXT={{'HP':'ホームページが、今のお店と合っていません','写真':'写真が古い／少ない状態です','口コミ':'お客様の声に、応えきれていません'}};
  var OKTXT={{'HP':'ホームページは最新の状態です','写真':'写真は新しいものが載っています','口コミ':'口コミにきちんと応えられています'}};
  var answers={{}},labels=[],idx=0;
  var qs=document.querySelectorAll('.q'),segs=document.querySelectorAll('#prog i');
  document.querySelectorAll('.q').forEach(function(q){{
    q.querySelectorAll('.qopt').forEach(function(btn){{
      btn.addEventListener('click',function(){{
        q.querySelectorAll('.qopt').forEach(function(b){{b.classList.remove('sel');}});
        btn.classList.add('sel');
        answers[q.dataset.q]={{weak:btn.dataset.weak==='1',a:btn.dataset.a,key:q.dataset.key}};
        setTimeout(next,240);
      }});
    }});
  }});
  function next(){{
    qs[idx].classList.remove('on'); idx++;
    if(idx<qs.length){{ qs[idx].classList.add('on'); if(segs[idx])segs[idx].classList.add('on'); qs[idx].scrollIntoView({{behavior:'smooth',block:'center'}}); }}
    else {{ showResult(); }}
  }}
  function row(isWeak,key){{
    var d=document.createElement('div');
    d.className='rli'+(isWeak?'':' ok');
    var i=document.createElement('i'); i.textContent=isWeak?'!':'✓';
    var s=document.createElement('span'); s.textContent=(isWeak?WEAKTXT:OKTXT)[key]||'';
    d.appendChild(i); d.appendChild(s);
    return d;
  }}
  function showResult(){{
    var weak=0,list=document.getElementById('rlist');
    while(list.firstChild){{list.removeChild(list.firstChild);}}
    labels=[];
    ['q1','q2','q3'].forEach(function(k){{
      var a=answers[k];if(!a)return;
      labels.push(a.a);
      if(a.weak)weak++;
      list.appendChild(row(a.weak,a.key));
    }});
    document.getElementById('rcount').textContent=weak;
    var msg;
    if(weak>=2)msg='実際のお店は変わっているのに、ネット上だけ昔のまま——という状態です。お店を変える必要はありません。ネット側を、今に合わせるだけです。';
    else if(weak===1)msg='おおむね整っています。あと1つ、ここを今の状態に合わせるだけで、見え方が変わります。';
    else msg='よく整っています。この状態を保つ（写真とメニューを新しいままにする）ところを、こちらで引き受けることもできます。';
    document.getElementById('rmsg').textContent=msg;
    document.getElementById('srcmemo').value='みつかる看板_診断LP3 / ズレ'+weak+'件 / '+labels.join('・');
    var r=document.getElementById('result');r.classList.add('on');r.scrollIntoView({{behavior:'smooth',block:'center'}});
    if(typeof gtag==='function'){{gtag('event','quiz_complete',{{weak:weak,variant:VARIANT}});}}
    if(typeof fbq==='function'){{try{{fbq('trackCustom','QuizComplete',{{weak:weak,variant:VARIANT}});}}catch(e){{}}}}
  }}
  var f=document.getElementById('f'),err=document.getElementById('err'),thanks=document.getElementById('thanks');
  var sink=document.querySelector('iframe[name="gsink"]'),submitted=false;
  function compose(){{
    var memo=document.getElementById('srcmemo');
    var biz=document.getElementById('biz').value||'業種未選択';
    var area=document.getElementById('area').value||'エリア未入力';
    var base=memo.value.indexOf('ズレ')>=0?memo.value:'みつかる看板_診断LP3 / 診断未回答';
    memo.value=base+' / 業種:'+biz+' / エリア:'+area;
  }}
  function fire(){{
    if(typeof gtag==='function'){{gtag('event','generate_lead',{{method:'check_form',value:1,variant:VARIANT}});}}
    if(typeof fbq==='function'){{try{{fbq('track','Lead',{{content_name:'mitsukaru_check3',variant:VARIANT}});}}catch(e){{}}}}
    if(typeof clarity==='function'){{try{{clarity('set','lead','mitsukaru_check3');}}catch(e){{}}}}
  }}
  function show(){{if(!submitted)return;f.style.display='none';thanks.style.display='block';try{{thanks.scrollIntoView({{behavior:'smooth',block:'center'}});}}catch(e){{}}}}
  f.addEventListener('submit',function(ev){{
    if(!f.checkValidity()){{ev.preventDefault();err.hidden=false;var b=f.querySelector(':invalid');if(b){{try{{b.focus();}}catch(e){{}}}}return;}}
    err.hidden=true;submitted=true;compose();
    var b=f.querySelector('.submit');if(b){{b.disabled=true;b.textContent='送信中…';}}
    fire();setTimeout(show,1600);
  }});
  var tb=document.getElementById('tbook');
  if(tb){{tb.addEventListener('click',function(){{
    if(typeof gtag==='function'){{gtag('event','schedule_click',{{variant:VARIANT}});}}
    if(typeof fbq==='function'){{try{{fbq('trackCustom','ScheduleClick',{{variant:VARIANT}});}}catch(e){{}}}}
  }});}}
  if(sink){{sink.addEventListener('load',function(){{if(submitted)show();}});}}
}})();
</script>
</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print("written:", OUT, len(HTML), "bytes")
