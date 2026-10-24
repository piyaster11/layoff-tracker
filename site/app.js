const $=s=>document.querySelector(s), fmt=n=>n==null?"–":n.toLocaleString("en-US");
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const FILES=["layoffs","challenger","layoffsfyi","us_youth","china_youth","nyfed","claims","meta"];
const mlabel=k=>{const[y,m]=k.split("-");return new Date(+y,+m-1).toLocaleString("en-US",{month:"short"})+" "+y};
Promise.all(FILES.map(f=>fetch(`data/${f}.json`).then(r=>r.json()))).then(a=>{
  const D=Object.fromEntries(FILES.map((f,i)=>[f,a[i]]));
  Chart.defaults.color="#8b949e";Chart.defaults.borderColor="#30363d";Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,sans-serif";
  render(D);
}).catch(e=>{document.body.insertAdjacentHTML("afterbegin",`<p style="color:#f85149;padding:16px">Failed to load data: ${esc(e)}</p>`)});

function render(D){
  $("#updated").textContent=`Last updated ${D.meta.last_updated}.`;
  const rows=D.layoffs.rows, counted=rows.filter(r=>r.counted);
  const total=counted.reduce((s,r)=>s+r.count,0);
  const us20=D.us_youth.series.find(s=>s.id==="LNS14000036"), us16=D.us_youth.series.find(s=>s.id==="LNS14024887");
  const cn=D.china_youth.series.find(s=>s.id==="16-24"), cn25=D.china_youth.series.find(s=>s.id==="25-29");
  const last=s=>s.data[s.data.length-1];
  const fyi=D.layoffsfyi.years.find(y=>y.year===2026);
  const ch=D.challenger, chm=Object.entries(ch.monthly), chl=chm[chm.length-1];
  const ng=D.nyfed.unemployment.data, ngl=ng[ng.length-1];
  const k=(v,l,s,src)=>`<div class="kpi"><div class="v">${v}</div><div class="l">${l}</div><div class="s">${s}${src?` · <a href="${src}" target="_blank" rel="noopener">source</a>`:""}</div></div>`;
  $("#kpis").innerHTML=[
    k(fmt(total),"Jobs cut, tracked announcements",`${counted.length} announcements, Oct 2024–Oct 2026`,"#layoffs"),
    k(fmt(fyi.employees),"Tech layoffs in 2026 (Layoffs.fyi)",`${fyi.companies} companies · as of ${D.layoffsfyi.asof}`,D.layoffsfyi.src),
    k(fmt(chl[1]),`US announced job cuts, ${mlabel(chl[0])}`,`${fmt(ch.totals["2026_ytd_sep"])} Jan–Sep 2026 (Challenger)`,ch.src[0]),
    k(last(us20)[1].toFixed(1)+"%",`US unemployment, ages 20–24 (${mlabel(last(us20)[0])})`,`ages 16–24: ${last(us16)[1].toFixed(1)}% · BLS`,us20.src),
    k(last(cn)[1].toFixed(1)+"%",`China urban, ages 16–24 excl. students (${mlabel(last(cn)[0])})`,`ages 25–29: ${last(cn25)[1].toFixed(1)}% · NBS`,D.china_youth.src),
    k(ngl[3].toFixed(1)+"%",`US recent college grads 22–27 (${mlabel(ngl[0])})`,`underemployed: ${D.nyfed.underemployment.data.at(-1)[1].toFixed(1)}% · NY Fed`,D.nyfed.src),
  ].join("");

  new Chart($("#cMonth"),{type:"bar",data:{labels:chm.map(e=>mlabel(e[0])),datasets:[{label:"Announced job cuts",data:chm.map(e=>e[1]),backgroundColor:"#f85149aa"}]},
    options:{maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>v>=1000?v/1000+"k":v}}}}});
  const sec={};counted.forEach(r=>sec[r.sector]=(sec[r.sector]||0)+r.count);
  const se=Object.entries(sec).sort((a,b)=>b[1]-a[1]);
  const pal=["#58a6ff","#f85149","#3fb950","#d29922","#bc8cff","#ff7b72","#39c5cf","#e3b341","#8b949e","#ffa657","#7ee787","#a5d6ff","#f778ba"];
  new Chart($("#cSector"),{type:"doughnut",data:{labels:se.map(e=>e[0]),datasets:[{data:se.map(e=>e[1]),backgroundColor:pal,borderWidth:0}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:"right",labels:{boxWidth:12,font:{size:11}}}}}});
  const co={};counted.forEach(r=>co[r.company]=(co[r.company]||0)+r.count);
  const ce=Object.entries(co).sort((a,b)=>b[1]-a[1]).slice(0,12);
  new Chart($("#cTop"),{type:"bar",data:{labels:ce.map(e=>e[0]),datasets:[{data:ce.map(e=>e[1]),backgroundColor:"#58a6ffcc"}]},
    options:{indexAxis:"y",maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{callback:v=>v/1000+"k"}}}}});

  // table
  const fs=$("#fSector");[...new Set(rows.map(r=>r.sector))].sort().forEach(s=>fs.add(new Option(s,s)));
  let sortK="date",asc=false;
  const draw=()=>{
    const q=$("#q").value.toLowerCase(),y=$("#fYear").value,s=fs.value,kb=$("#fKob").checked;
    let r=rows.filter(x=>(!q||(x.company+" "+x.reason).toLowerCase().includes(q))&&(!y||x.date.startsWith(y))&&(!s||x.sector===s)&&(!kb||x.kobeissi));
    r.sort((a,b)=>{let A=a[sortK],B=b[sortK];if(A==null)return 1;if(B==null)return -1;return (A>B?1:A<B?-1:0)*(asc?1:-1)});
    $("#tbl tbody").innerHTML=r.map(x=>`<tr class="${x.counted?"":"excl"}"><td>${x.date}</td><td><b>${esc(x.company)}</b>${x.kobeissi?'<span class="tag k">Kobeissi</span>':""}${x.counted?"":'<span class="tag">not in totals</span>'}</td>
      <td class="num">${esc(x.label)}</td><td>${esc(x.pct)}</td><td>${esc(x.sector)}</td><td>${esc(x.country)}</td><td>${esc(x.reason)}${x.note?`<span class="n">${esc(x.note)}</span>`:""}</td>
      <td><a href="${esc(x.src)}" target="_blank" rel="noopener">${esc(x.srcname)}</a></td></tr>`).join("");
    const t=r.filter(x=>x.counted).reduce((a,x)=>a+x.count,0);
    $("#tblnote").textContent=`${r.length} rows shown · ${fmt(t)} jobs in totals. Announcements, not completed layoffs; some are multi-year plans or include attrition. Figures checked ${D.layoffs.asof}.`;
    document.querySelectorAll("#tbl th").forEach(th=>{th.classList.toggle("sorted",th.dataset.k===sortK);th.classList.toggle("asc",th.dataset.k===sortK&&asc)});
  };
  document.querySelectorAll("#tbl th[data-k]").forEach(th=>th.onclick=()=>{if(sortK===th.dataset.k)asc=!asc;else{sortK=th.dataset.k;asc=sortK!=="count"&&sortK!=="date"?true:false}draw()});
  ["#q","#fYear","#fSector","#fKob"].forEach(s=>$(s).addEventListener("input",draw));draw();

  // youth chart
  const months=[...new Set([...us20.data,...us16.data,...cn.data,...cn25.data].map(p=>p[0]))].sort();
  const map=s=>{const m=Object.fromEntries(s.data);return months.map(k=>m[k]??null)};
  new Chart($("#cYouth"),{type:"line",data:{labels:months.map(mlabel),datasets:[
    {label:"China 16–24 (excl. students)",data:map(cn),borderColor:"#f85149",backgroundColor:"#f85149",tension:.25,pointRadius:2},
    {label:"China 25–29",data:map(cn25),borderColor:"#ffa657",backgroundColor:"#ffa657",borderDash:[5,4],tension:.25,pointRadius:1},
    {label:"US 16–24",data:map(us16),borderColor:"#58a6ff",backgroundColor:"#58a6ff",tension:.25,pointRadius:2},
    {label:"US 20–24",data:map(us20),borderColor:"#3fb950",backgroundColor:"#3fb950",tension:.25,pointRadius:2}]},
    options:{maintainAspectRatio:false,spanGaps:false,interaction:{mode:"index",intersect:false},plugins:{legend:{labels:{boxWidth:12,font:{size:11}}}},scales:{y:{ticks:{callback:v=>v+"%"}}}}});
  $("#youthnote").innerHTML=`US: ${esc(D.us_youth.source)}; ${esc(D.us_youth.note)} China: NBS urban surveyed rate. Definitions differ (China is urban only and excludes students; US includes students who look for work), so compare trends, not levels. As of ${D.us_youth.asof}.`;
  new Chart($("#cGrad"),{type:"line",data:{labels:ng.map(r=>mlabel(r[0])),datasets:[
    {label:"Recent grads 22–27",data:ng.map(r=>r[3]),borderColor:"#bc8cff",tension:.25,pointRadius:2},
    {label:"All young workers 22–27",data:ng.map(r=>r[1]),borderColor:"#39c5cf",tension:.25,pointRadius:2},
    {label:"All workers",data:ng.map(r=>r[2]),borderColor:"#8b949e",tension:.25,pointRadius:1}]},
    options:{maintainAspectRatio:false,plugins:{legend:{labels:{boxWidth:12,font:{size:11}}}},scales:{y:{ticks:{callback:v=>v+"%"}}}}});
  $("#gradnote").innerHTML=`${esc(D.nyfed.note)} <a href="${D.nyfed.src}" target="_blank" rel="noopener">NY Fed</a>, as of ${D.nyfed.asof}.`;
  const vp=Object.entries(D.china_youth.verified_points).map(([m,u])=>`<a href="${u}" target="_blank" rel="noopener">${mlabel(m)}</a>`).join(", ");
  $("#method").innerHTML=`${esc(D.china_youth.method_note)} <a href="${D.china_youth.src}" target="_blank" rel="noopener">NBS explanation (Chinese)</a>.<br><br>Monthly values cross-checked against news reports for ${vp}.`;

  // claims
  const cls=s=>/^Verified$/.test(s)?"ok":/Partly|temporary/i.test(s)?"part":"bad";
  $("#kob").innerHTML=D.claims.kobeissi.map(c=>`<div class="claim"><b>${esc(c.company)}</b>: ${esc(c.claimed)} <span class="st ${cls(c.status)}">${esc(c.status)}</span><div class="note">${esc(c.detail)} · <a href="${esc(c.src)}" target="_blank" rel="noopener">source</a></div></div>`).join("");
  $("#turk").innerHTML=D.claims.turkish.map(c=>`<div class="claim"><b>"${esc(c.claim)}"</b> <span class="st bad">${esc(c.verdict)}</span><div class="note">${esc(c.facts)} ${c.src.map((u,i)=>`<a href="${esc(u)}" target="_blank" rel="noopener">[${i+1}]</a>`).join(" ")}</div></div>`).join("");

  // sources
  const S=[[D.us_youth.source,"https://www.bls.gov/cps/",D.us_youth.asof],[D.china_youth.source,D.china_youth.src,D.china_youth.asof],[D.nyfed.source,D.nyfed.src,D.nyfed.asof],
    [ch.source,ch.src[0],ch.asof],[D.layoffsfyi.source,D.layoffsfyi.src,D.layoffsfyi.asof],["Layoff rows: company releases, Reuters, CNBC, WSJ, AP (link on each row)","#layoffs",D.layoffs.asof]];
  $("#srclist").innerHTML=S.map(s=>`<li><a href="${esc(s[1])}" target="_blank" rel="noopener">${esc(s[0])}</a> <span class="note">as of ${s[2]}</span></li>`).join("");
  $("#missing").innerHTML=D.meta.missing.map(m=>`<li>${esc(m)}</li>`).join("");
  $("#files").innerHTML=FILES.map(f=>`<a href="data/${f}.json">${f}.json</a>`).join(", ");
}
