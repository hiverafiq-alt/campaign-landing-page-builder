"""Validate a campaign config and export a static website without dependencies."""
import argparse,json,re,shutil
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
def validate(c):
    for k in ['brand','headline','description','cta','ctaUrl','date','location','intro','story','heroImage','heroAlt','privacyUrl']:
        if not isinstance(c.get(k),str) or not c[k].strip():raise ValueError('Missing '+k)
    for k in ['background','foreground','accent']:
        if not re.fullmatch(r'#[0-9a-fA-F]{6}',c.get(k,'')):raise ValueError('Use six-digit hex colors')
    for k in ['ctaUrl','privacyUrl']:
        u=urlparse(c[k])
        if u.scheme!='https' or not u.netloc or u.username or u.password:raise ValueError('Use an HTTPS '+k+' without credentials')
    p=Path(c['heroImage'])
    if p.is_absolute() or '..' in p.parts or not str(p).startswith('assets/') or not (ROOT/p).is_file():raise ValueError('Choose an existing local image under assets/')
    if not isinstance(c.get('features'),list) or not 1<=len(c['features'])<=6 or any(not x.get('title') or not x.get('body') for x in c['features']):raise ValueError('Provide 1–6 complete feature cards')
    tracking=c.get('tracking',{})
    for k,pattern in [('ga4',r'G-[A-Z0-9]+'),('meta',r'\d+')]:
        if tracking.get(k) and not re.fullmatch(pattern,tracking[k]):raise ValueError('Invalid '+k+' tracker ID')
    if any(k not in ['ga4','meta'] for k in tracking):raise ValueError('Unsupported tracker; ask your agent to implement and test it')
    return c
def build(config,dest):
    c=validate(json.loads(Path(config).read_text()));dest=Path(dest).resolve()
    if dest==ROOT:raise ValueError('Export into a separate folder')
    dest.mkdir(parents=True,exist_ok=True)
    for name in ['index.html','style.css','app.js','builder.html']:shutil.copyfile(ROOT/name,dest/name)
    (dest/'config.js').write_text('window.CAMPAIGN = '+json.dumps(c,ensure_ascii=False).replace('<','\\u003c')+';\n')
    image=Path(c['heroImage']);(dest/image).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/image,dest/image)
    return dest
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',default=str(ROOT/'campaign.json'));p.add_argument('--out',default=str(ROOT/'dist'));a=p.parse_args();print(build(a.config,a.out))
