#!/usr/bin/env python3
"""
Build self-contained workbench.html with embedded docs + edit/save support.
Double-click to open, no server needed.

Usage: python3 scripts/build_workbench.py
"""
import json, os, glob

def read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def build():
    config = json.loads(read("workbench-config.json"))
    
    # Collect all docs
    docs = {}
    for pattern in ["docs/**/*.md", "config/*.md", "design/DESIGN.md"]:
        for path in glob.glob(pattern, recursive=True):
            docs[path] = read(path)
    
    config_js = json.dumps(config, ensure_ascii=False)
    docs_js = json.dumps(docs, ensure_ascii=False)
    
    with open("workbench.html", "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE.replace("__CONFIG__", config_js).replace("__DOCS__", docs_js))
    
    sz = os.path.getsize("workbench.html") // 1024
    print(f"Built workbench.html: {len(docs)} docs, {sz} KB")

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>产品工作台 - RICE评估系统</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;height:100vh;overflow:hidden;background:#f5f5f5}

.topbar{height:48px;background:#1a1a2e;color:#fff;display:flex;align-items:center;padding:0 16px;gap:10px}
.topbar .logo{font-weight:700;font-size:15px}
.topbar .bc{font-size:13px;color:#aaa;flex:1}.topbar .bc b{color:#fff;font-weight:400}
.topbar button{padding:5px 12px;border:1px solid #555;background:0 0;color:#ccc;border-radius:4px;cursor:pointer;font-size:12px}
.topbar button:hover{background:#333}
.topbar button.on{background:#7C3AED;border-color:#7C3AED;color:#fff}

.main{display:flex;height:calc(100vh - 48px)}

/* Left */
.lp{min-width:200px;overflow-y:auto;background:#fff;padding:12px}
.lp .gt{font-size:11px;color:#999;font-weight:600;padding:6px 8px;margin-top:12px}
.lp .gt:first-child{margin-top:0}
.lp .pi{padding:7px 12px;font-size:13px;color:#333;cursor:pointer;border-radius:6px;display:flex;align-items:center;gap:6px}
.lp .pi:hover{background:#f5f3ff}
.lp .pi.act{background:#ede9fe;color:#7C3AED;font-weight:500}
.lp .pi .ob{font-size:11px;color:#7C3AED;background:#f5f3ff;border:1px solid #e0d4fc;padding:1px 7px;border-radius:3px;cursor:pointer;margin-left:auto;white-space:nowrap}
.lp .pi .ob:hover{background:#7C3AED;color:#fff}

/* Divider */
.dv{width:6px;background:#e5e5e5;cursor:col-resize;flex-shrink:0;transition:background .15s}
.dv:hover,.dv.drag{background:#7C3AED}

/* Right */
.rp{min-width:200px;display:flex;flex-direction:column;background:#fff;overflow:hidden}
.tabs{display:flex;border-bottom:1px solid #e5e5e5;background:#fafafa;flex-shrink:0;overflow-x:auto}
.tab{padding:8px 14px;font-size:12px;color:#666;cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap;flex-shrink:0}
.tab:hover{color:#333;background:#f0f0f0}
.tab.act{color:#7C3AED;border-bottom-color:#7C3AED;font-weight:500}
.tab .x{margin-left:6px;color:#aaa;cursor:pointer;font-size:14px}
.tab .x:hover{color:#e53e3e}

/* Toolbar */
.toolbar{display:flex;align-items:center;gap:8px;padding:6px 16px;border-bottom:1px solid #eee;background:#fafafa;flex-shrink:0}
.toolbar .path{font-size:12px;color:#aaa;font-family:monospace;flex:1}
.toolbar button{padding:4px 12px;border:1px solid #ddd;background:#fff;border-radius:4px;cursor:pointer;font-size:12px;color:#555}
.toolbar button:hover{background:#f0f0f0}
.toolbar button.primary{background:#7C3AED;color:#fff;border-color:#7C3AED}
.toolbar button.primary:hover{background:#6d28d9}
.toolbar .saved{font-size:11px;color:#22c55e;display:none}

/* Doc */
.dc{flex:1;overflow-y:auto;padding:24px 32px}
.dc textarea{width:100%;height:100%;border:none;outline:none;resize:none;font-family:'SF Mono',Monaco,'Fira Code',monospace;font-size:13px;line-height:1.6;padding:0;color:#333}

/* Markdown */
.md h1{font-size:22px;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #7C3AED;color:#1a1a2e}
.md h2{font-size:18px;margin:24px 0 12px;color:#1a1a2e}
.md h3{font-size:15px;margin:20px 0 8px;color:#333}
.md h4{font-size:14px;margin:16px 0 6px;color:#555}
.md p{margin:8px 0;font-size:14px;line-height:1.7;color:#333}
.md code{background:#f4f4f4;padding:2px 6px;border-radius:3px;font-size:13px;font-family:'SF Mono',Monaco,monospace}
.md pre{background:#f8f8f8;padding:14px 18px;border-radius:6px;overflow-x:auto;margin:12px 0;border:1px solid #eee}
.md pre code{background:none;padding:0;font-size:12px;line-height:1.5}
.md table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13px}
.md th,.md td{border:1px solid #ddd;padding:6px 10px;text-align:left}
.md th{background:#f5f5f5;font-weight:600}
.md blockquote{border-left:3px solid #7C3AED;padding:8px 16px;margin:12px 0;background:#faf8ff;color:#666;font-size:13px}
.md ul,.md ol{padding-left:24px;margin:8px 0}
.md li{margin:4px 0;font-size:14px;line-height:1.6}
.md strong{color:#1a1a2e}
.md hr{border:none;border-top:1px solid #e5e5e5;margin:20px 0}
.md a{color:#7C3AED;text-decoration:none}

.empty{text-align:center;padding:80px 20px;color:#999}
.empty .ei{font-size:48px;margin-bottom:16px}

/* Home */
.home{padding:40px;overflow-y:auto;flex:1}
.home h1{font-size:24px;color:#1a1a2e;margin-bottom:6px}
.home .sub{color:#888;font-size:14px;margin-bottom:32px}
.home .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.home .card{background:#fff;border-radius:12px;padding:24px;border:1px solid #e5e5e5;cursor:pointer;transition:all .2s}
.home .card:hover{border-color:#7C3AED;box-shadow:0 4px 16px rgba(124,58,237,.1);transform:translateY(-2px)}
.home .card .ci{font-size:32px;margin-bottom:12px}
.home .card .ct{font-size:16px;font-weight:600;color:#1a1a2e;margin-bottom:4px}
.home .card .cd{font-size:13px;color:#888;margin-bottom:14px}
.home .card .tags{display:flex;flex-wrap:wrap;gap:4px}
.home .card .tag{font-size:11px;padding:2px 8px;background:#f0f0f0;border-radius:10px;color:#666}
</style>
</head>
<body>
<div class="topbar">
  <div class="logo">📐 产品工作台</div>
  <div class="bc" id="bc"></div>
  <button onclick="goHome()">🏠 首页</button>
  <button id="bP" class="on" onclick="setDev('pad')">💻 Pad</button>
  <button id="bM" onclick="setDev('mobile')">📱 手机</button>
</div>
<div class="main" id="main">
  <div class="lp" id="lp" style="width:35%"></div>
  <div class="dv" id="dv"></div>
  <div class="rp" id="rp" style="width:65%">
    <div class="tabs" id="tabs"></div>
    <div class="toolbar" id="toolbar" style="display:none">
      <span class="path" id="tPath"></span>
      <span class="saved" id="savedMsg">✓ 已保存</span>
      <button id="btnEdit" onclick="toggleEdit()">✏️ 编辑</button>
      <button id="btnSave" class="primary" onclick="saveDoc()" style="display:none">💾 保存</button>
    </div>
    <div class="dc" id="dc"><div class="empty"><div class="ei">📄</div><p>点击左侧页面查看文档</p></div></div>
  </div>
</div>
<script>
const C=__CONFIG__;
const D=__DOCS__;
let dev='pad',curF=null,openT=[],actT=null,editing=false,editContent='',fileHandles={};

// Home
function goHome(){curF=null;renderLeft();actT=null;openT=[];renderTabs();
  document.getElementById('dc').innerHTML='<div class="empty"><div class="ei">📄</div><p>点击左侧页面查看文档</p></div>';
  document.getElementById('toolbar').style.display='none';
  document.getElementById('bc').innerHTML='';}

function renderLeft(){
  const el=document.getElementById('lp');
  if(!curF){
    let h='<div class="home"><h1>RICE 评估系统</h1><p class="sub">选择功能模块浏览原型和需求文档</p><div class="grid">';
    for(const f of C.features)h+=`<div class="card" onclick="openF('${f.id}')"><div class="ci">${f.icon}</div><div class="ct">${f.name}</div><div class="cd">${f.description}</div><div class="tags">${f.pages.map(p=>`<span class="tag">${p.name}</span>`).join('')}</div></div>`;
    h+='</div></div>';el.innerHTML=h;return;
  }
  let h='';
  for(const f of C.features){
    h+=`<div class="gt">${f.icon} ${f.name}</div>`;
    for(const p of f.pages){
      const a=actT===p.doc?'act':'';
      const hp=p.html.replace('{device}',dev);
      h+=`<div class="pi ${a}" onclick="selP('${f.id}','${p.id}')"><span>📄 ${p.name}</span><span class="ob" onclick="event.stopPropagation();window.open('${hp}','_blank')">打开原型</span></div>`;
    }
  }
  h+='<div class="gt">📐 设计与配置</div>';
  const extras=[['design/DESIGN.md','🎨 设计规范'],['config/report-prompt-cpep.md','📊 C-PEP报告'],['config/report-prompt-pep3.md','📊 PEP-3报告'],['config/report-prompt-vbmapp.md','📊 VB-MAPP报告'],['config/iep-prompt-cpep.md','📋 C-PEP IEP'],['config/iep-prompt-pep3.md','📋 PEP-3 IEP'],['config/iep-prompt-vbmapp.md','📋 VB-MAPP IEP'],['config/iep-prompt-common.md','📋 IEP通用规则']];
  for(const[p,n]of extras){const a=actT===p?'act':'';h+=`<div class="pi ${a}" onclick="openDoc('${p}','${n}')"><span>${n}</span></div>`;}
  el.innerHTML=h;
}

function openF(fid){curF=C.features.find(f=>f.id===fid);renderLeft();if(curF.pages.length)selP(curF.id,curF.pages[0].id);}
function selP(fid,pid){curF=C.features.find(f=>f.id===fid);const p=curF.pages.find(x=>x.id===pid);if(!p)return;
  document.getElementById('bc').innerHTML=`${curF.name} / <b>${p.name}</b>`;openDoc(p.doc,p.name);}
function setDev(d){dev=d;document.getElementById('bP').classList.toggle('on',d==='pad');document.getElementById('bM').classList.toggle('on',d==='mobile');renderLeft();}

// Tabs
function openDoc(path,name){
  editing=false;
  if(!openT.find(t=>t.path===path))openT.push({path,name:name||path.split('/').pop()});
  actT=path;renderTabs();renderDoc(path);renderLeft();
}
function renderTabs(){
  let h='';for(const t of openT){const a=t.path===actT?'act':'';
    h+=`<div class="tab ${a}" onclick="openDoc('${t.path}','${t.name}')">${t.name}<span class="x" onclick="event.stopPropagation();closeTab('${t.path}')">&times;</span></div>`;}
  document.getElementById('tabs').innerHTML=h;
}
function closeTab(p){openT=openT.filter(t=>t.path!==p);if(actT===p)actT=openT.length?openT[openT.length-1].path:null;
  renderTabs();if(actT)renderDoc(actT);else{document.getElementById('dc').innerHTML='<div class="empty"><div class="ei">📄</div><p>点击左侧页面查看文档</p></div>';document.getElementById('toolbar').style.display='none';}renderLeft();}

// Render doc
function renderDoc(path){
  const raw=D[path];const el=document.getElementById('dc');const tb=document.getElementById('toolbar');
  tb.style.display='flex';document.getElementById('tPath').textContent=path;
  document.getElementById('btnEdit').style.display='';document.getElementById('btnSave').style.display='none';
  document.getElementById('savedMsg').style.display='none';editing=false;
  if(!raw&&raw!==''){el.innerHTML=`<div class="empty"><div class="ei">📝</div><p>文档尚未创建<br><code>${path}</code></p></div>`;return;}
  el.innerHTML=`<div class="md">${md(raw)}</div>`;editContent=raw;
}

// Edit toggle
function toggleEdit(){
  const el=document.getElementById('dc');
  if(!editing){
    editing=true;
    document.getElementById('btnEdit').textContent='👁 预览';
    document.getElementById('btnSave').style.display='';
    el.innerHTML=`<textarea id="editor">${esc(editContent)}</textarea>`;
    document.getElementById('editor').focus();
    // Sync on input
    document.getElementById('editor').addEventListener('input',e=>{editContent=e.target.value;});
  }else{
    editing=false;
    document.getElementById('btnEdit').textContent='✏️ 编辑';
    document.getElementById('btnSave').style.display='none';
    D[actT]=editContent; // update in-memory
    el.innerHTML=`<div class="md">${md(editContent)}</div>`;
  }
}

// Save
async function saveDoc(){
  if(!actT)return;
  D[actT]=editContent;
  // Try File System Access API (Chrome/Edge)
  if(window.showSaveFilePicker){
    try{
      let handle=fileHandles[actT];
      if(!handle){
        handle=await window.showSaveFilePicker({suggestedName:actT.split('/').pop(),types:[{description:'Markdown',accept:{'text/markdown':['.md']}}]});
        fileHandles[actT]=handle;
      }
      const w=await handle.createWritable();
      await w.write(editContent);await w.close();
      showSaved();return;
    }catch(e){if(e.name==='AbortError')return;}
  }
  // Fallback: download
  const blob=new Blob([editContent],{type:'text/markdown'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download=actT.split('/').pop();a.click();URL.revokeObjectURL(a.href);
  showSaved();
}
function showSaved(){const el=document.getElementById('savedMsg');el.style.display='';setTimeout(()=>el.style.display='none',2000);}

// Markdown
function md(s){
  s=s.replace(/```(\w*)\n([\s\S]*?)```/g,(_,l,c)=>'<pre><code>'+esc(c.trim())+'</code></pre>');
  s=s.replace(/`([^`]+)`/g,'<code>$1</code>');
  s=s.replace(/^#### (.+)$/gm,'<h4>$1</h4>');
  s=s.replace(/^### (.+)$/gm,'<h3>$1</h3>');
  s=s.replace(/^## (.+)$/gm,'<h2>$1</h2>');
  s=s.replace(/^# (.+)$/gm,'<h1>$1</h1>');
  s=s.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
  s=s.replace(/\*(.+?)\*/g,'<em>$1</em>');
  s=s.replace(/^> (.+)$/gm,'<blockquote>$1</blockquote>');
  s=s.replace(/^---$/gm,'<hr>');
  s=s.replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank">$1</a>');
  // Tables
  s=s.replace(/(\|.+\|[\r\n]+\|[-| :]+\|[\r\n]+((\|.+\|[\r\n]*)+))/g,m=>{
    const rows=m.trim().split('\n').filter(r=>r.trim());if(rows.length<2)return m;
    const hc=rows[0].split('|').filter(c=>c.trim());
    let t='<table><thead><tr>'+hc.map(c=>'<th>'+c.trim()+'</th>').join('')+'</tr></thead><tbody>';
    for(let i=2;i<rows.length;i++){const cells=rows[i].split('|').filter(c=>c.trim());t+='<tr>'+cells.map(c=>'<td>'+c.trim()+'</td>').join('')+'</tr>';}
    return t+'</tbody></table>';});
  s=s.replace(/^- (.+)$/gm,'<li>$1</li>');
  s=s.replace(/((?:<li>.*<\/li>\n?)+)/g,m=>'<ul>'+m+'</ul>');
  s=s.replace(/\n\n/g,'</p><p>');s='<p>'+s+'</p>';
  s=s.replace(/<p>\s*(<h[1-4]|<pre|<table|<ul|<blockquote|<hr)/g,'$1');
  s=s.replace(/(<\/h[1-4]>|<\/pre>|<\/table>|<\/ul>|<\/blockquote>|<hr>)\s*<\/p>/g,'$1');
  return s;
}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

// Divider
(function(){const d=document.getElementById('dv'),l=document.getElementById('lp'),r=document.getElementById('rp');let drag=false;
d.addEventListener('mousedown',e=>{drag=true;d.classList.add('drag');document.body.style.cursor='col-resize';document.body.style.userSelect='none';e.preventDefault();});
document.addEventListener('mousemove',e=>{if(!drag)return;const rect=document.getElementById('main').getBoundingClientRect();const pct=Math.max(15,Math.min(85,((e.clientX-rect.left)/rect.width)*100));l.style.width=pct+'%';r.style.width=(100-pct)+'%';});
document.addEventListener('mouseup',()=>{if(!drag)return;drag=false;d.classList.remove('drag');document.body.style.cursor='';document.body.style.userSelect='';});
})();

// Init
renderLeft();
</script>
</body>
</html>'''

if __name__ == "__main__":
    build()
