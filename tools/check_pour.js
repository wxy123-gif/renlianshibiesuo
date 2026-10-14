const fs=require('fs');
const lines=fs.readFileSync('_eda_work/epro_new/智慧门锁_100x100.epru','utf8').split(/\r?\n/);
let out={minX:Infinity,maxX:-Infinity,minY:Infinity,maxY:-Infinity}; let pours=[];
function cl(pair,b){}
function walk(sub,o){ if(!Array.isArray(sub)||sub.length<2)return; function take(i){o.minX=Math.min(o.minX,sub[i]);o.maxX=Math.max(o.maxX,sub[i]);o.minY=Math.min(o.minY,sub[i+1]);o.maxY=Math.max(o.maxY,sub[i+1]);} take(0); let i=2; while(i<sub.length){const t=sub[i]; if(t==='L'){i++; while(i+1<sub.length&&typeof sub[i]==='number'&&typeof sub[i+1]==='number'){take(i);i+=2}}else if(t==='ARC'){if(i+3<sub.length&&[sub[i+1],sub[i+2],sub[i+3]].every(x=>typeof x==='number')){take(i+2);i+=4}else i++}else if(typeof t==='number'&&typeof sub[i+1]==='number'){take(i);i+=2}else i++;}}
for(let n=0;n<lines.length;n++){const line=lines[n];if(!line.includes('||')||!line.endsWith('|'))continue;const p=line.indexOf('||');let d,m;try{d=JSON.parse(line.slice(0,p));m=JSON.parse(line.slice(p+2,-1))}catch{continue}if(d.type==='POUR')pours.push({line:n+1,marker:m});if(d.type==='POURED')for(const f of m.pourFill||[])for(const sub of f.path||[])walk(sub,out);}
console.log(JSON.stringify({out,pours:pours.map(x=>({line:x.line,path:x.marker.path}))}));
