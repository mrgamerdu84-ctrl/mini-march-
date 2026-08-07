#!/usr/bin/env python3
from pathlib import Path
import argparse

CSS = r'''
/* TIKOWIKO_MOBILE_INTRO_FIX_V2 */
#tkSplash{position:fixed;inset:0;z-index:9999;background:#13a7ed;display:flex;align-items:center;justify-content:center;opacity:1;transition:opacity .42s ease;pointer-events:auto}
#tkSplash.hide{opacity:0;pointer-events:none}
#tkSplash img{width:100%;height:100%;object-fit:cover;object-position:center;display:block}

/* L'introduction doit toujours rester utilisable sur petit écran Android. */
#introOverlay.intro-overlay,
.intro-overlay{
  position:fixed!important;
  inset:0!important;
  z-index:9000!important;
  box-sizing:border-box!important;
  display:flex!important;
  align-items:flex-start!important;
  justify-content:center!important;
  overflow-y:auto!important;
  overscroll-behavior:contain!important;
  -webkit-overflow-scrolling:touch!important;
  touch-action:pan-y!important;
  pointer-events:auto!important;
  padding:max(8px,env(safe-area-inset-top)) 10px calc(86px + env(safe-area-inset-bottom))!important;
}

.intro-card.story-card{
  box-sizing:border-box!important;
  width:min(430px,100%)!important;
  max-width:100%!important;
  height:auto!important;
  max-height:none!important;
  margin:0 auto!important;
  padding:14px 13px 105px!important;
  display:block!important;
  overflow:visible!important;
  pointer-events:auto!important;
}

.intro-card.story-card h2{
  font-size:clamp(18px,5vw,22px)!important;
  line-height:1.15!important;
  margin:4px 0 7px!important;
}

.intro-card.story-card>p{
  font-size:13px!important;
  line-height:1.35!important;
  margin:5px 0!important;
}

.intro-card.story-card .story-letter{
  box-sizing:border-box!important;
  display:block!important;
  width:100%!important;
  height:min(46dvh,390px)!important;
  min-height:190px!important;
  max-height:390px!important;
  overflow-y:auto!important;
  overflow-x:hidden!important;
  overscroll-behavior:contain!important;
  -webkit-overflow-scrolling:touch!important;
  touch-action:pan-y!important;
  pointer-events:auto!important;
  padding:12px!important;
  margin:8px 0 10px!important;
  font-size:clamp(15px,4.2vw,18px)!important;
  line-height:1.45!important;
}

.intro-card.story-card .story-letter *{
  font-size:inherit!important;
  line-height:inherit!important;
}

.intro-card.story-card .story-price{
  margin:8px 0 12px!important;
  padding:8px 4px!important;
  font-size:15px!important;
  line-height:1.25!important;
  text-align:center!important;
}

/* Le bouton reste TOUJOURS visible, même si la lettre ne défile pas. */
#buyStoreBtn{
  position:fixed!important;
  left:50%!important;
  bottom:max(10px,env(safe-area-inset-bottom))!important;
  transform:translateX(-50%)!important;
  z-index:10050!important;
  box-sizing:border-box!important;
  width:min(410px,calc(100vw - 24px))!important;
  min-height:58px!important;
  margin:0!important;
  padding:13px 16px!important;
  display:block!important;
  visibility:visible!important;
  opacity:1!important;
  pointer-events:auto!important;
  touch-action:manipulation!important;
  box-shadow:0 6px 24px rgba(0,0,0,.30)!important;
}

@media(max-height:700px){
  .intro-card.story-card{padding-top:8px!important;padding-bottom:100px!important}
  .intro-card.story-card>p{font-size:12px!important}
  .intro-card.story-card .story-letter{height:40dvh!important;min-height:155px!important;font-size:14px!important}
  #buyStoreBtn{min-height:54px!important;padding:11px 14px!important}
}
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
    const overlay=document.getElementById('introOverlay') || document.querySelector('.intro-overlay');
    const letter=overlay && overlay.querySelector('.story-letter');
    const button=document.getElementById('buyStoreBtn');

    if(overlay){
      overlay.style.overflowY='auto';
      overlay.style.webkitOverflowScrolling='touch';
      overlay.style.touchAction='pan-y';
      overlay.style.pointerEvents='auto';
    }

    if(letter){
      letter.style.overflowY='auto';
      letter.style.webkitOverflowScrolling='touch';
      letter.style.touchAction='pan-y';
      letter.style.pointerEvents='auto';
      ['touchstart','touchmove','pointerdown','pointermove','wheel'].forEach(type=>{
        letter.addEventListener(type,e=>e.stopPropagation(),{passive:true});
      });
    }

    if(button){
      button.style.display='block';
      button.style.visibility='visible';
      button.style.opacity='1';
      button.style.pointerEvents='auto';
      button.style.touchAction='manipulation';
      ['touchstart','pointerdown','click'].forEach(type=>{
        button.addEventListener(type,e=>e.stopPropagation(),{passive:true});
      });
    }
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',fix,{once:true});
  else fix();
  setTimeout(fix,300);
  setTimeout(fix,1000);
})();
</script>
'''

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    html=Path(args.input).read_text(encoding='utf-8')
    if 'TIKOWIKO_MOBILE_INTRO_FIX_V2' not in html:
        html=html.replace('</style>',CSS+'\n</style>',1)
        html=html.replace('<body>','<body>'+SPLASH,1)
        html=html.replace('</body>',JS+'\n</body>',1)
    Path(args.output).write_text(html,encoding='utf-8')

if __name__=='__main__':
    main()
