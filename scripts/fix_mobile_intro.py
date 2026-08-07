#!/usr/bin/env python3
from pathlib import Path
import argparse

CSS = r'''
/* TIKOWIKO_MOBILE_INTRO_FIX_V1 */
#tkSplash{position:fixed;inset:0;z-index:9999;background:#13a7ed;display:flex;align-items:center;justify-content:center;opacity:1;transition:opacity .42s ease;pointer-events:auto}
#tkSplash.hide{opacity:0;pointer-events:none}
#tkSplash img{width:100%;height:100%;object-fit:cover;object-position:center;display:block}
.intro-overlay{align-items:flex-start!important;justify-content:center!important;overflow-y:auto!important;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;padding:max(10px,env(safe-area-inset-top)) 12px max(10px,env(safe-area-inset-bottom))!important}
.intro-card.story-card{box-sizing:border-box;width:min(430px,100%)!important;max-height:calc(100vh - 20px)!important;max-height:calc(100dvh - 20px)!important;margin:auto!important;padding:16px 14px!important;display:flex!important;flex-direction:column!important;overflow:hidden!important}
.intro-card.story-card h2{font-size:clamp(18px,5vw,22px)!important;line-height:1.1;margin-bottom:7px!important;flex:0 0 auto}
.intro-card.story-card>p{font-size:13px!important;line-height:1.35!important;flex:0 0 auto}
.intro-card.story-card .story-letter{flex:1 1 auto!important;min-height:90px!important;max-height:none!important;overflow-y:auto!important;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;touch-action:pan-y!important;padding:12px!important;margin:8px 0!important}
.intro-card.story-card .story-price{flex:0 0 auto;margin:7px 0!important;font-size:13px}
#buyStoreBtn{flex:0 0 auto;width:100%;min-height:48px;margin-top:6px!important;position:relative;z-index:3;touch-action:manipulation}
@media(max-height:650px){.intro-card.story-card{padding:11px 12px!important}.intro-card.story-card>p{display:none}.intro-card.story-card .story-letter{font-size:13px;line-height:1.35}}
'''

SPLASH = '''\n<div id="tkSplash" aria-hidden="true"><img src="./splash.jpg" alt=""></div>\n'''

JS = r'''
<script>
(function(){
  const splash=document.getElementById('tkSplash');
  const hideSplash=()=>{if(!splash)return;splash.classList.add('hide');setTimeout(()=>splash.remove(),500)};
  window.addEventListener('load',()=>setTimeout(hideSplash,1450),{once:true});
  setTimeout(hideSplash,2600);
  const fix=()=>{
    const overlay=document.getElementById('introOverlay');
    const letter=overlay&&overlay.querySelector('.story-letter');
    const button=document.getElementById('buyStoreBtn');
    if(overlay){overlay.style.overflowY='auto';overlay.style.webkitOverflowScrolling='touch'}
    if(letter){letter.style.overflowY='auto';letter.style.webkitOverflowScrolling='touch';letter.style.touchAction='pan-y'}
    if(button)button.style.touchAction='manipulation';
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',fix,{once:true});else fix();
})();
</script>
'''

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    html=Path(args.input).read_text(encoding='utf-8')
    if 'TIKOWIKO_MOBILE_INTRO_FIX_V1' not in html:
        html=html.replace('</style>',CSS+'\n</style>',1)
        html=html.replace('<body>','<body>'+SPLASH,1)
        html=html.replace('</body>',JS+'\n</body>',1)
    Path(args.output).write_text(html,encoding='utf-8')

if __name__=='__main__':
    main()
