/* Optional third-party trackers load only after explicit consent. */
(()=>{'use strict';const c=window.CAMPAIGN;const $=s=>document.querySelector(s);const hex=/^#[0-9a-f]{6}$/i;
for(const [key,css] of [['background','--paper'],['foreground','--ink'],['accent','--accent']])if(hex.test(c[key]))document.documentElement.style.setProperty(css,c[key]);
document.querySelectorAll('[data-text]').forEach(e=>e.textContent=c[e.dataset.text]||'');document.title=c.brand+' · '+c.headline.replaceAll('\n',' ');document.querySelector('meta[name=description]').content=c.description;
$('#demo').hidden=!c.demo;$('#hero').src=c.heroImage;$('#hero').alt=c.heroAlt;
function safeURL(value){const u=new URL(value,location.href);if(!['https:','http:'].includes(u.protocol))throw Error('Only web links are supported');return u}
$('#privacy').href=safeURL(c.privacyUrl).href;
const allowed=['utm_source','utm_medium','utm_campaign','utm_content','utm_term'];const input=new URLSearchParams(location.search);const url=safeURL(c.ctaUrl);for(const k of allowed){const value=input.get(k)||c.utm?.[k];if(value)url.searchParams.set(k,String(value).slice(0,150))}document.querySelectorAll('.campaign-link').forEach(a=>a.href=url.href);
$('#features').replaceChildren(...c.features.map((f,i)=>{const d=document.createElement('article');d.className='feature';for(const [tag,text] of [['span',String(i+1).padStart(2,'0')],['h3',f.title],['p',f.body]]){const e=document.createElement(tag);e.textContent=text;d.append(e)}return d}));
if('IntersectionObserver'in window){const o=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');o.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('.reveal').forEach(e=>{e.classList.add('ready');o.observe(e)})}
let active=false;const configured=/^G-[A-Z0-9]+$/.test(c.tracking?.ga4||'')||/^\d+$/.test(c.tracking?.meta||'');let choice;try{choice=localStorage.getItem('campaign-tracking')}catch{}
function load(src){const s=document.createElement('script');s.src=src;s.async=true;document.head.append(s)}
function enable(){if(active||!configured)return;active=true;if(/^G-[A-Z0-9]+$/.test(c.tracking.ga4||'')){window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',c.tracking.ga4,{anonymize_ip:true});load('https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(c.tracking.ga4))}if(/^\d+$/.test(c.tracking.meta||'')){const f=window.fbq=function(){f.callMethod?f.callMethod.apply(f,arguments):f.queue.push(arguments)};f.queue=[];f.push=f;f.loaded=true;f.version='2.0';load('https://connect.facebook.net/en_US/fbevents.js');f('init',c.tracking.meta);f('track','PageView')}}
function choose(v){try{localStorage.setItem('campaign-tracking',v)}catch{}$('#consent').hidden=true;if(v==='yes')enable();else if(active)location.reload()}
$('#accept').onclick=()=>choose('yes');$('#decline').onclick=()=>choose('no');$('#preferences').onclick=()=>{$('#consent').hidden=false;$('#decline').focus()};if(choice==='yes')enable();else if(!choice&&configured)$('#consent').hidden=false;
document.querySelectorAll('[data-event]').forEach(a=>a.addEventListener('click',()=>{if(!active)return;window.gtag?.('event','campaign_cta',{placement:a.dataset.event});window.fbq?.('trackCustom','CampaignCTA',{placement:a.dataset.event})}));
})();
