#!/usr/bin/env python3
from pathlib import Path
import argparse

MARKER = 'TIKOWIKO_MOBILE_LAYOUT_V6'

CSS = r'''
/* TIKOWIKO_MOBILE_LAYOUT_V6 */
html,body,#tkAppShell{
  width:100%!important;
  max-width:100vw!important;
  overflow-x:hidden!important;
  box-sizing:border-box!important;
}
#tkBottomNav{
  position:relative!important;
  z-index:60000!important;
  display:grid!important;
  grid-template-columns:repeat(4,minmax(0,1fr))!important;
  width:100%!important;
  max-width:100vw!important;
  min-width:0!important;
  gap:6px!important;
  padding:7px max(7px,env(safe-area-inset-right)) calc(7px + env(safe-area-inset-bottom)) max(7px,env(safe-area-inset-left))!important;
  margin:0!important;
  overflow:hidden!important;
  box-sizing:border-box!important;
  pointer-events:auto!important;
  touch-action:manipulation!important;
}
#tkBottomNav .tkNavBtn{
  min-width:0!important;
  width:100%!important;
  max-width:none!important;
  height:74px!important;
  margin:0!important;
  padding:7px 2px!important;
  border-radius:15px!important;
  box-sizing:border-box!important;
  font-size:12px!important;
  line-height:1.05!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:clip!important;
  pointer-events:auto!important;
  touch-action:manipulation!important;
  user-select:none!important;
  -webkit-user-select:none!important;
}
#tkBottomNav .tkNavBtn *{
  pointer-events:none!important;
  user-select:none!important;
  -webkit-user-select:none!important;
}
#tkBottomNav .tkNavBtn span:first-child,
#tkBottomNav .tkNavBtn .icon{
  font-size:24px!important;
  line-height:26px!important;
}
#tkMissionBar{
  width:100%!important;
  max-width:100vw!important;
  min-width:0!important;
  box-sizing:border-box!important;
  overflow:hidden!important;
}
.tkOverlay{
  position:fixed!important;
  inset:0!important;
  z-index:70000!important;
  pointer-events:auto!important;
}
.tkOverlay.show{display:flex!important;}
.tkSheet{
  width:100%!important;
  max-width:100vw!important;
  max-height:100dvh!important;
  box-sizing:border-box!important;
  pointer-events:auto!important;
}
.tkSheetScroll{
  overflow-y:auto!important;
  -webkit-overflow-scrolling:touch!important;
  touch-action:pan-y!important;
  pointer-events:auto!important;
}
@media(max-width:390px){
  #tkBottomNav{gap:4px!important;padding-left:4px!important;padding-right:4px!important;}
  #tkBottomNav .tkNavBtn{font-size:11px!important;height:70px!important;}
}
'''

JS = r'''
<script>
/* TIKOWIKO_MOBILE_LAYOUT_V6 */
(function(){
  const overlays={
    tkNavShop:'tkRefonteShop',
    tkNavStock:'tkRefonteStock',
    tkNavManage:'tkRefonteManage'
  };

  function showPanel(id){
    const el=document.getElementById(id);
    if(!el) return false;
    el.classList.add('show');
    el.style.display='flex';
    el.style.pointerEvents='auto';
    el.setAttribute('aria-hidden','false');
    const scroll=el.querySelector('.tkSheetScroll');
    if(scroll) scroll.scrollTop=0;
    return true;
  }

  function hidePanel(el){
    if(!el) return;
    el.classList.remove('show');
    el.style.display='none';
    el.setAttribute('aria-hidden','true');
  }

  function activate(btn,e){
    if(!btn) return;
    if(e){ e.preventDefault(); e.stopImmediatePropagation(); }
    const id=btn.id;
    if(id==='tkNavCash'){
      if(window.TKGameBridge && typeof window.TKGameBridge.scan==='function') window.TKGameBridge.scan();
      else document.getElementById('clickBtn')?.click();
      return;
    }
    const panel=overlays[id];
    if(panel) showPanel(panel);
  }

  document.addEventListener('pointerdown',function(e){
    const btn=e.target.closest && e.target.closest('#tkBottomNav .tkNavBtn');
    if(btn){ e.preventDefault(); e.stopImmediatePropagation(); }
  },true);

  document.addEventListener('pointerup',function(e){
    const btn=e.target.closest && e.target.closest('#tkBottomNav .tkNavBtn');
    if(btn) activate(btn,e);
  },true);

  document.addEventListener('touchend',function(e){
    const t=e.changedTouches && e.changedTouches[0];
    if(!t) return;
    const node=document.elementFromPoint(t.clientX,t.clientY);
    const btn=node && node.closest && node.closest('#tkBottomNav .tkNavBtn');
    if(btn) activate(btn,e);
  },{capture:true,passive:false});

  document.addEventListener('pointerup',function(e){
    const close=e.target.closest && e.target.closest('.tkClose');
    if(!close) return;
    e.preventDefault(); e.stopImmediatePropagation();
    const id=close.dataset.close;
    hidePanel(document.getElementById(id));
  },true);

  document.querySelectorAll('.tkOverlay').forEach(el=>{
    if(!el.classList.contains('show')) el.style.display='none';
  });
})();
</script>
'''

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    p=Path(a.input)
    s=p.read_text(encoding='utf-8')
    if MARKER in s:
        Path(a.output).write_text(s,encoding='utf-8')
        print('✓ V6 déjà présente')
        return
    if '</style>' not in s or '</body>' not in s:
        raise SystemExit('HTML attendu introuvable')
    s=s.replace('</style>',CSS+'\n</style>',1)
    s=s.replace('</body>',JS+'\n</body>',1)
    Path(a.output).write_text(s,encoding='utf-8')
    print('✓ V6 appliquée : barre 4 boutons + tactile renforcé')

if __name__=='__main__':
    main()
