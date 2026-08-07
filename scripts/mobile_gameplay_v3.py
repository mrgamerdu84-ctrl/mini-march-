#!/usr/bin/env python3
from pathlib import Path
import argparse, json, zipfile, base64

MARKER='TIKOWIKO_MOBILE_GAMEPLAY_V3'
SHOP_CSS='''
/* TIKOWIKO_MOBILE_GAMEPLAY_V3 */
html,body{overscroll-behavior-y:auto!important}
#tkShopFab{position:fixed;right:14px;bottom:calc(14px + env(safe-area-inset-bottom));z-index:260;border:0;border-radius:18px;padding:12px 16px;background:#1e9c5a;color:#fff;font-family:'Baloo 2',sans-serif;font-weight:900;font-size:15px;box-shadow:0 5px 0 #147a44,0 8px 22px rgba(0,0,0,.22);display:none;touch-action:manipulation}
#tkShopFab:active{transform:translateY(3px);box-shadow:0 2px 0 #147a44}
#tkShopOverlay{position:fixed;inset:0;z-index:320;background:rgba(10,20,28,.78);display:none;align-items:stretch;justify-content:center;padding:0;touch-action:pan-y}
#tkShopOverlay.show{display:flex}
#tkShopPanel{width:min(720px,100%);height:100%;max-height:100dvh;background:#fbfaf4;display:flex;flex-direction:column;overflow:hidden}
#tkShopHeader{position:sticky;top:0;z-index:3;display:flex;align-items:center;gap:10px;padding:calc(12px + env(safe-area-inset-top)) 14px 12px;background:#1d3557;color:#fff;box-shadow:0 3px 10px rgba(0,0,0,.2);flex:0 0 auto}
#tkShopHeader h2{font:900 21px 'Baloo 2',sans-serif;margin:0;flex:1}
#tkShopClose{border:0;border-radius:12px;background:#fff;color:#1d3557;font-weight:900;font-size:20px;width:44px;height:44px;touch-action:manipulation}
#tkShopScroll{overflow-y:auto!important;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;touch-action:pan-y!important;padding:14px 14px calc(90px + env(safe-area-inset-bottom));flex:1 1 auto}
#tkShopScroll .shop-grid{grid-template-columns:1fr!important}
#tkShopScroll .card{min-height:88px}
#tkShopHint{font-size:13px;font-weight:800;color:#53606a;background:#fff4cc;border:2px solid #e0b94f;border-radius:12px;padding:9px 11px;margin-bottom:14px}
body.tk-shop-open{overflow:hidden!important}
@media(min-width:700px){#tkShopScroll .shop-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
'''
SHOP_HTML='''
<button id="tkShopFab" type="button">🛒 Boutique</button>
<div id="tkShopOverlay" aria-hidden="true"><section id="tkShopPanel" role="dialog" aria-modal="true" aria-label="Boutique du magasin"><header id="tkShopHeader"><h2>🛒 Boutique du magasin</h2><button id="tkShopClose" type="button" aria-label="Fermer">✕</button></header><div id="tkShopScroll"><div id="tkShopHint">Achète ici des étagères, caisses, présentoirs, congélateurs, caméras et agrandissements.</div></div></section></div>
'''
SHOP_JS='''
<script>
(function(){
 const fab=document.getElementById('tkShopFab'),overlay=document.getElementById('tkShopOverlay'),close=document.getElementById('tkShopClose'),scroll=document.getElementById('tkShopScroll');
 const prod=document.getElementById('productionShop'); if(prod&&prod.parentElement)scroll.appendChild(prod.parentElement);
 const stop=e=>e.stopPropagation(); ['touchstart','touchmove','pointerdown','pointermove','wheel'].forEach(t=>scroll.addEventListener(t,stop,{passive:true}));
 function openShop(){overlay.classList.add('show');overlay.setAttribute('aria-hidden','false');document.body.classList.add('tk-shop-open');scroll.scrollTop=0}
 function closeShop(){overlay.classList.remove('show');overlay.setAttribute('aria-hidden','true');document.body.classList.remove('tk-shop-open')}
 fab.addEventListener('click',openShop);close.addEventListener('click',closeShop);overlay.addEventListener('click',e=>{if(e.target===overlay)closeShop()});
 function syncFab(){const intro=document.getElementById('introOverlay');fab.style.display=(intro&&intro.classList.contains('show'))?'none':'block'} syncFab();setInterval(syncFab,500);
})();
</script>
'''
WALK_OLD='''function animateWalker(mesh, dt, moving){
  if(!mesh) return;
  mesh.userData.walkPhase = (mesh.userData.walkPhase || 0) + (moving ? dt * 9.5 : dt * 4);
  const phase = mesh.userData.walkPhase;
  const legL = mesh.getObjectByName('leg-left');
  const legR = mesh.getObjectByName('leg-right');
  const armL = mesh.getObjectByName('arm-left');
  const armR = mesh.getObjectByName('arm-right');
  const swing = moving ? Math.sin(phase) * 0.48 : 0;
  if(legL) legL.rotation.x += (swing - legL.rotation.x) * Math.min(1, dt * 12);
  if(legR) legR.rotation.x += (-swing - legR.rotation.x) * Math.min(1, dt * 12);
  if(armL) armL.rotation.x += (-swing * .65 - armL.rotation.x) * Math.min(1, dt * 10);
  if(armR) armR.rotation.x += (swing * .65 - armR.rotation.x) * Math.min(1, dt * 10);
  mesh.position.y = moving ? Math.abs(Math.sin(phase * 2)) * 0.025 : 0;
}'''
WALK_NEW='''function animateWalker(mesh, dt, moving){
  if(!mesh) return;
  mesh.userData.walkPhase = (mesh.userData.walkPhase || 0) + (moving ? dt * 7.8 : dt * 3.2);
  const phase = mesh.userData.walkPhase;
  const legL = mesh.getObjectByName('leg-left');
  const legR = mesh.getObjectByName('leg-right');
  const armL = mesh.getObjectByName('arm-left');
  const armR = mesh.getObjectByName('arm-right');
  const swing = moving ? Math.sin(phase) * 0.30 : 0;
  if(legL) legL.rotation.x += (swing - legL.rotation.x) * Math.min(1, dt * 10);
  if(legR) legR.rotation.x += (-swing - legR.rotation.x) * Math.min(1, dt * 10);
  if(armL) armL.rotation.x += (-swing * .55 - armL.rotation.x) * Math.min(1, dt * 9);
  if(armR) armR.rotation.x += (swing * .55 - armR.rotation.x) * Math.min(1, dt * 9);
  mesh.position.y = 0;
}'''
CAR_START='/* --- simple low-poly cars driving loops around the road --- */\nfunction makeSimpleCar(color){'
CAR_END='/* --- illuminated storefront sign, glows brighter at night --- */'

def car_code(frames):
    urls=','.join(json.dumps('data:image/png;base64,'+x) for x in frames)
    return f'''/* --- voitures rouges Kenney Isometric Vehicles --- */
const KENNEY_CAR_URLS=[{urls}];
const kenneyCarTextures=KENNEY_CAR_URLS.map(src=>{{const t=new THREE.TextureLoader().load(src);t.encoding=THREE.sRGBEncoding;t.magFilter=THREE.NearestFilter;t.minFilter=THREE.LinearFilter;return t;}});
function makeSimpleCar(color){{const mat=new THREE.SpriteMaterial({{map:kenneyCarTextures[6],transparent:true,depthWrite:false}});const car=new THREE.Sprite(mat);car.scale.set(1.35,1.0,1);car.center.set(.5,.12);car.position.y=.02;car.userData.frame=-1;return car;}}
const roadCenterHW=innerHW+ROAD_WIDTH/2,roadCenterHD=innerHD+ROAD_WIDTH/2;
const carWaypoints=[{{x:-roadCenterHW,z:-roadCenterHD}},{{x:roadCenterHW,z:-roadCenterHD}},{{x:roadCenterHW,z:roadCenterHD}},{{x:-roadCenterHW,z:roadCenterHD}}];
const CAR_COLORS=[0xd94b3f,0xd94b3f,0xd94b3f,0xd94b3f];const cars=[];
CAR_COLORS.forEach((color,i)=>{{const car=makeSimpleCar(color),startIdx=i%4,a=carWaypoints[startIdx],b=carWaypoints[(startIdx+1)%4],t=(i+.18)/CAR_COLORS.length;car.position.set(a.x+(b.x-a.x)*t,.02,a.z+(b.z-a.z)*t);scene.add(car);cars.push({{mesh:car,idx:startIdx,speed:2.5+Math.random()*.45}});}});
function updateCars(dt){{cars.forEach(c=>{{const target=carWaypoints[(c.idx+1)%4],dx=target.x-c.mesh.position.x,dz=target.z-c.mesh.position.z,dist=Math.hypot(dx,dz);if(dist<.12){{c.idx=(c.idx+1)%4;return}}const nx=dx/dist,nz=dz/dist;c.mesh.position.x+=nx*c.speed*dt;c.mesh.position.z+=nz*c.speed*dt;c.mesh.position.y=.02;const camAngle=Math.atan2(camera.position.z-target.z,camera.position.x-target.x);let a=Math.atan2(nz,nx)-camAngle;while(a<0)a+=Math.PI*2;while(a>=Math.PI*2)a-=Math.PI*2;const frame=(Math.round(a/(Math.PI*2)*16)+6)%16;if(frame!==c.mesh.userData.frame){{c.mesh.material.map=kenneyCarTextures[frame];c.mesh.material.needsUpdate=true;c.mesh.userData.frame=frame;}}}});}}

'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);ap.add_argument('--vehicles-zip',required=True);args=ap.parse_args()
    html=Path(args.input).read_text(encoding='utf-8')
    if MARKER in html: Path(args.output).write_text(html,encoding='utf-8');return
    frames=[]
    with zipfile.ZipFile(args.vehicles_zip) as z:
        for i in range(16):
            name=f'PNG/Civilian/Red/Sedan 1/carRed2_{i:03d}.png'
            frames.append(base64.b64encode(z.read(name)).decode('ascii'))
    if len(frames)!=16: raise SystemExit('16 sprites Kenney attendus')
    if WALK_OLD not in html: raise SystemExit('animateWalker attendu introuvable')
    html=html.replace(WALK_OLD,WALK_NEW,1)
    s=html.find(CAR_START);e=html.find(CAR_END,s)
    if s<0 or e<0: raise SystemExit('bloc voitures attendu introuvable')
    html=html[:s]+car_code(frames)+html[e:]
    html=html.replace('</style>',SHOP_CSS+'\n</style>',1)
    html=html.replace('</body>',SHOP_HTML+SHOP_JS+'\n</body>',1)
    Path(args.output).write_text(html,encoding='utf-8')
    print('✓ Boutique mobile, personnages au sol et voitures Kenney appliqués')
if __name__=='__main__':main()
