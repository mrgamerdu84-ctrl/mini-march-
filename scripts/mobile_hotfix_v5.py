#!/usr/bin/env python3
from pathlib import Path
import argparse

MARKER='TIKOWIKO_MOBILE_HOTFIX_V5'
CSS='''
/* TIKOWIKO_MOBILE_HOTFIX_V5 */
#tkAppShell{z-index:1000!important}
#tkViewport{z-index:1!important}
#tkMissionBar{position:relative;z-index:20!important;pointer-events:auto!important}
#tkBottomNav{position:relative;z-index:30000!important;pointer-events:auto!important;isolation:isolate}
#tkBottomNav .tkNavBtn{position:relative;z-index:30001!important;pointer-events:auto!important;touch-action:manipulation!important;-webkit-tap-highlight-color:transparent}
.tkOverlay{z-index:40000!important;pointer-events:auto!important}
.tkSheet,.tkSheetScroll,.tkSheet button{pointer-events:auto!important}
#tkViewport #scene-wrap,#tkViewport #scene-canvas{z-index:1!important}
'''
JS='''
<script>
/* TIKOWIKO_MOBILE_HOTFIX_V5: boutons tactiles fiables */
(function(){
  const action={
    tkNavShop:()=>document.getElementById('tkRefonteShop')?.classList.add('show'),
    tkNavStock:()=>document.getElementById('tkRefonteStock')?.classList.add('show'),
    tkNavManage:()=>document.getElementById('tkRefonteManage')?.classList.add('show'),
    tkNavCash:()=>{ if(window.TKGameBridge?.scan) window.TKGameBridge.scan(); else document.getElementById('clickBtn')?.click(); }
  };
  let lastTap=0;
  function run(id,e){
    if(e){e.preventDefault();e.stopPropagation();}
    const now=Date.now(); if(now-lastTap<220)return; lastTap=now;
    action[id]?.();
  }
  Object.keys(action).forEach(id=>{
    const b=document.getElementById(id); if(!b)return;
    b.style.pointerEvents='auto'; b.style.touchAction='manipulation';
    b.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();},{capture:true});
    b.addEventListener('pointerup',e=>run(id,e),{capture:true});
    b.addEventListener('touchend',e=>run(id,e),{capture:true,passive:false});
    b.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();},{capture:true});
  });
  document.querySelectorAll('.tkClose').forEach(b=>{
    const close=e=>{e.preventDefault();e.stopPropagation();document.getElementById(b.dataset.close)?.classList.remove('show')};
    b.addEventListener('pointerup',close,{capture:true});
    b.addEventListener('touchend',close,{capture:true,passive:false});
  });
  document.querySelectorAll('.tkOverlay,.tkSheet,.tkSheetScroll,#tkBottomNav').forEach(el=>{
    ['pointerdown','pointermove','pointerup','touchstart','touchmove','touchend'].forEach(t=>
      el.addEventListener(t,e=>e.stopPropagation(),{passive:t==='touchmove'})
    );
  });
})();
</script>
'''

def replace_once(s, old, new, label, required=True):
    if old not in s:
        if required: raise SystemExit(f'Motif introuvable: {label}')
        return s
    return s.replace(old,new,1)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    s=Path(a.input).read_text('utf-8')
    if MARKER in s:
        Path(a.output).write_text(s,'utf-8'); print('✓ Hotfix V5 déjà présent'); return
    s=replace_once(s,"const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:false });","const renderer = new THREE.WebGLRenderer({ canvas, antialias:false, alpha:false, powerPreference:'high-performance', precision:'mediump' });",'WebGLRenderer')
    s=replace_once(s,"renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));","renderer.setPixelRatio(1);",'pixel ratio')
    s=replace_once(s,"renderer.shadowMap.enabled = true;","renderer.shadowMap.enabled = false;",'shadows')
    s=replace_once(s,"sun.castShadow = true;","sun.castShadow = false;",'sun shadow')
    s=s.replace("mesh.castShadow=true; mesh.receiveShadow=true; mesh.frustumCulled=false;","mesh.castShadow=false; mesh.receiveShadow=false; mesh.frustumCulled=true;")
    s=s.replace("scene.add(lamp1);","/* mobile V5: lamp1 lighting disabled */")
    s=s.replace("scene.add(lamp2);","/* mobile V5: lamp2 lighting disabled */")
    s=s.replace("  scene.add(light);\n  streetLamps.push(light);","  /* mobile V5: decorative street point-light disabled */\n  streetLamps.push(light);",1)
    s=replace_once(s,"for(let i=0;i<5;i++) spawnPedestrian();","for(let i=0;i<3;i++) spawnPedestrian();",'pedestrians')
    s=replace_once(s,"if(customers.length >= 9) return null;","if(customers.length >= 6) return null;",'customer cap')
    s=replace_once(s,"for(let i=0;i<5;i++) setTimeout(()=> spawnCustomer(false), i*220);","for(let i=0;i<3;i++) setTimeout(()=> spawnCustomer(false), i*300);",'rush crowd')
    old="""window.addEventListener('pointerup', e => {\n  if(dragging && moved < 6){\n    const usedShelf = handleShelfPointer(e);\n    if(!usedShelf) handleScan();\n  }\n  dragging = false;\n});"""
    new="""window.addEventListener('pointerup', e => {\n  if(e.target !== canvas){ dragging = false; return; }\n  if(dragging && moved < 6){\n    const usedShelf = handleShelfPointer(e);\n    if(!usedShelf) handleScan();\n  }\n  dragging = false;\n});\ncanvas.addEventListener('pointercancel',()=>{dragging=false;});"""
    s=replace_once(s,old,new,'pointerup canvas')
    old="""let clock = new THREE.Clock();\nfunction renderLoop(){\n  const dt = Math.min(clock.getDelta(), 0.05);\n  animateSpawns(dt);\n  updateAmbiance(dt);\n  updateCustomers(dt);\n  updateSpawning(dt);\n  updateRush(dt);\n  updateDoor(dt);\n  updatePedestrians(dt);\n  updateCars(dt);\n  updateEmployees(dt);\n  updateStoryEvents(dt);\n  renderer.render(scene, camera);\n  requestAnimationFrame(renderLoop);\n}"""
    new="""let clock = new THREE.Clock();\nlet tkFrameAccum = 0;\nfunction renderLoop(){\n  requestAnimationFrame(renderLoop);\n  tkFrameAccum += Math.min(clock.getDelta(), 0.05);\n  if(tkFrameAccum < (1/30)) return;\n  const dt = Math.min(tkFrameAccum, 0.05); tkFrameAccum = 0;\n  animateSpawns(dt);\n  updateAmbiance(dt);\n  updateCustomers(dt);\n  updateSpawning(dt);\n  updateRush(dt);\n  updateDoor(dt);\n  updatePedestrians(dt);\n  updateCars(dt);\n  updateEmployees(dt);\n  updateStoryEvents(dt);\n  renderer.render(scene, camera);\n}"""
    s=replace_once(s,old,new,'render loop')
    s=s.replace("    renderStock();\n  }\n  setInterval(refreshAll,500);","    if(document.getElementById('tkRefonteStock')?.classList.contains('show')) renderStock();\n  }\n  setInterval(refreshAll,1000);",1)
    s=replace_once(s,'</style>',CSS+'\n</style>','style injection')
    s=replace_once(s,'</body>',JS+'\n</body>','script injection')
    Path(a.output).write_text(s,'utf-8')
    print('✓ V5 appliquée : boutons tactiles + rendu mobile allégé')
if __name__=='__main__': main()
