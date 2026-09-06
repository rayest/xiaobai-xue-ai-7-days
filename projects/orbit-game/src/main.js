import './style.css';
import {createCombat} from './combat.js';
import {createFlightAudio} from './audio.js';
import {createSpace} from './scene.js';
import {LANES,nextLane,flightSpeed,crossesPlayer,intersectsPlayer,calculateScore} from './rules.js';

const $=id=>document.getElementById(id);
let space;
try{space=createSpace($('space'));}
catch(error){$('start').innerHTML='<span>3D 场景无法启动</span>';$('intro').querySelector('.description').textContent='请使用支持 WebGL 2 的浏览器，并开启硬件加速后刷新。';console.error(error);}
if(space) boot(space);

function boot(space){
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let state='intro',lane=1,playerX=0,elapsed=0,energy=0,lives=3,invulnerable=0,spawnTimer=0,wave=0;
  let objects=[],lastTime=0,toastUntil=0,best=0,soundEnabled=true;
  const audio=createFlightAudio();
  let combatScore=0,kills=0;
  const combat=createCombat(space.scene,{
    alert:message=>toast(message),
    fire:()=>audio.laser(),
    damage:()=>{damage('敌方弹幕命中 · 立即变道');return state==='running';},
    kill:(points,boss)=>{combatScore+=points;kills++;audio.explosion(boss);if(boss)lives=Math.min(3,lives+1);toast(boss?'+2000 母舰击破 · 护盾修复':'+250 敌机击毁');},
    boss:value=>{$('boss-bar').hidden=!value||state!=='running';if(value){$('boss-health').value=value.hp;$('boss-health').max=value.max;$('boss-hp').textContent=value.hp+' / '+value.max;}},
  });
  function damage(message){
    if(state!=='running'||invulnerable>0)return;
    lives--;invulnerable=1.6;audio.explosion(false);document.body.classList.remove('hit');void document.body.offsetWidth;document.body.classList.add('hit');toast(message);
    if(lives===0)finish();
  }

  let boost=0,boostLatched=false;
  const boostKeys=new Set();
  const wantsBoost=()=>state==='running'&&(boostLatched||boostKeys.size>0);
  function resetBoost(){boost=0;boostLatched=false;boostKeys.clear();$('boost').setAttribute('aria-pressed','false');document.body.classList.remove('boosting');}
  function syncSound(){ $('sound').classList.toggle('sound-on',soundEnabled);$('sound').setAttribute('aria-label',soundEnabled?'关闭音效':'开启音效');$('sound').setAttribute('aria-pressed',String(soundEnabled));$('sound').title=soundEnabled?'关闭音效':'开启音效'; }
  syncSound();
  try{best=Math.max(0,Number(localStorage.getItem('orbit-best'))||0);}catch{/* Storage may be unavailable in private browsers. */}
  $('best').textContent=best.toLocaleString();$('start').disabled=false;$('start').querySelector('span').textContent='开始飞行';
  const beep=(frequency,duration=.09)=>audio.tone(frequency,duration);
  function toast(message){$('toast').textContent=message;$('toast').classList.add('visible');toastUntil=performance.now()+1300;}
  function updateHud(){
    $('score').textContent=String((calculateScore(elapsed,energy)+combatScore)).padStart(6,'0');
    $('kills').textContent=kills;
    $('lives').textContent=Array.from({length:3},(_,i)=>i<lives?'●':'○').join(' ');
    $('speed').textContent=Math.round(flightSpeed(elapsed,boost)*10);$('lane').textContent=['左','中','右'][lane];
  }
  function clearObjects(){for(const obj of objects)space.removeItem(obj.mesh);objects=[];}
  function start(){
    audio.unlock();combat.reset();combatScore=0;kills=0;resetBoost();clearObjects();lane=1;playerX=0;elapsed=0;energy=0;lives=3;invulnerable=0;spawnTimer=0;wave=0;
    state='running';$('intro').hidden=true;$('dialog').hidden=true;$('hud').hidden=false;$('touch-controls').hidden=false;$('pause').disabled=false;
    $('pause').setAttribute('aria-label','暂停游戏');updateHud();beep(440);toast('武器已上线 · 变道瞄准，自动开火');$('start').blur();
  }
  function setPaused(paused){
    if(!['running','paused'].includes(state))return;
    resetBoost();audio.unlock();state=paused?'paused':'running';audio.update(!paused,flightSpeed(elapsed,0),0);$('dialog').hidden=!paused;$('touch-controls').hidden=paused;
    $('pause').setAttribute('aria-label',paused?'继续游戏':'暂停游戏');
    if(paused){$('dialog-caption').textContent='FLIGHT PAUSED';$('dialog-title').textContent='航行已暂停';$('dialog-description').textContent='星海会等你。准备好就继续出发。';$('results').hidden=true;$('resume').textContent='继续飞行';$('resume').focus();}else{$('resume').blur();}
  }
  function finish(){
    resetBoost();audio.update(false,0,0);state='ended';const score=(calculateScore(elapsed,energy)+combatScore);const record=score>best;
    if(record){best=score;try{localStorage.setItem('orbit-best',String(best));}catch{}$('best').textContent=best.toLocaleString();}
    $('dialog-caption').textContent=record?'NEW PERSONAL BEST':'FLIGHT COMPLETE';$('dialog-title').textContent=record?'新的星际纪录':'航行结束';
    $('dialog-description').textContent='护盾已耗尽。每一次出发，都会飞得更远。';$('final-score').textContent=score.toLocaleString();$('final-energy').textContent=energy;$('final-time').textContent=Math.floor(elapsed)+'s';$('final-kills').textContent=kills;
    $('results').hidden=false;$('dialog').hidden=false;$('touch-controls').hidden=true;$('pause').disabled=true;$('resume').textContent='再次出发';$('resume').focus();
  }
  function home(){resetBoost();audio.update(false,0,0);state='intro';combat.reset();clearObjects();$('intro').hidden=false;$('dialog').hidden=true;$('hud').hidden=true;$('touch-controls').hidden=true;$('pause').disabled=true;$('pause').setAttribute('aria-label','暂停游戏');$('toast').classList.remove('visible');$('toast').textContent='';$('start').focus();}
  function move(direction){if(state!=='running')return;const target=nextLane(lane,direction);if(target!==lane){lane=target;beep(220,.04);updateHud();}}
  $('start').addEventListener('click',start);
  $('resume').addEventListener('click',()=>state==='ended'?start():setPaused(false));
  $('home').addEventListener('click',home);
  $('pause').addEventListener('click',()=>setPaused(state==='running'));
  $('sound').addEventListener('click',()=>{soundEnabled=!soundEnabled;audio.setEnabled(soundEnabled);syncSound();beep(660);});
  $('boost').addEventListener('click',()=>{if(state!=='running')return;boostLatched=!boostLatched;audio.unlock();$('boost').setAttribute('aria-pressed',String(boostLatched));$('boost').blur();});
  $('left').addEventListener('pointerdown',event=>{event.preventDefault();move(-1);});
  $('right').addEventListener('pointerdown',event=>{event.preventDefault();move(1);});
  document.addEventListener('keydown',event=>{
    if(event.altKey||event.ctrlKey||event.metaKey)return;
    if(['ShiftLeft','ShiftRight','KeyW','ArrowUp'].includes(event.code)&&state==='running'){event.preventDefault();boostKeys.add(event.code);}
    if(['ArrowLeft','ArrowRight','KeyA','KeyD'].includes(event.code)){event.preventDefault();if(!event.repeat)move(['ArrowLeft','KeyA'].includes(event.code)?-1:1);}
    if(event.code==='Space'&&!event.repeat){
      if(state==='running'||state==='paused'){event.preventDefault();setPaused(state==='running');}
    }
    if(event.code==='Escape'&&state==='running')setPaused(true);
  });
  document.addEventListener('keyup',event=>boostKeys.delete(event.code));
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&state==='running')setPaused(true);});
  window.addEventListener('blur',()=>{if(state==='running')setPaused(true);});
  let touchX=null;
  space.canvas.addEventListener('pointerdown',event=>{touchX=event.clientX;});
  space.canvas.addEventListener('pointerup',event=>{if(touchX!==null&&Math.abs(event.clientX-touchX)>22)move(event.clientX>touchX?1:-1);touchX=null;});
  space.canvas.addEventListener('pointercancel',()=>touchX=null);
  space.canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();if(state==='running')setPaused(true);$('dialog-description').textContent='图形连接中断，请刷新页面重新启动。';});
  function spawn(){
    // Gentle opening: three centered collectibles, followed by one readable hazard per wave.
    const first=wave<3;const chosen=first?1:wave===3?1:Math.floor(Math.random()*3);
    const kind=first?'energy':wave%3===0?'rock':Math.random()<.55?'rock':'energy';
    objects.push({kind,x:LANES[chosen],mesh:space.addItem(kind,LANES[chosen],-64),resolved:false});wave++;
  }
  function tick(time){
    const dt=Math.min((time-lastTime)/1000||0,.05);lastTime=time;
    if(time>toastUntil)$('toast').classList.remove('visible');
    if(state==='running'){
      boost+=((wantsBoost()?1:0)-boost)*(1-Math.exp(-dt*5));
      document.body.classList.toggle('boosting',boost>.2);
      $('boost').setAttribute('aria-pressed',String(wantsBoost()));
      $('boost').textContent=wantsBoost()?'加速中 · 再点关闭':'加速 · Shift / W';
      elapsed+=dt;invulnerable=Math.max(0,invulnerable-dt);playerX+=(LANES[lane]-playerX)*(1-Math.exp(-dt*14));
      spawnTimer-=dt;if(spawnTimer<=0){spawn();spawnTimer=Math.max(.85,1.45-elapsed*.003);}
      for(const obj of objects){
        const previousZ=obj.mesh.position.z;obj.mesh.position.z+=flightSpeed(elapsed,boost)*dt;obj.mesh.rotation.y+=dt*(obj.kind==='energy'?2:.5);obj.mesh.rotation.z+=dt*.2;
        if(!obj.resolved&&crossesPlayer(previousZ,obj.mesh.position.z)){
          obj.resolved=true;
          if(intersectsPlayer(playerX,obj.x,obj.kind)){
            if(obj.kind==='energy'){energy++;obj.mesh.visible=false;beep(880,.14);toast('+100 能量已收集');}
            else {damage('撞击陨石 · 护盾受损');if(state==='ended')break;}
          }
        }
      }
      if(state==='running')combat.update(dt,playerX,flightSpeed(elapsed,boost),boost);
      objects=objects.filter(obj=>{if(obj.mesh.position.z>19){space.removeItem(obj.mesh);return false;}return true;});updateHud();
    }
    combat.setVisible(state!=='intro');if(state!=='running')$('boss-bar').hidden=true;
    audio.update(state==='running',flightSpeed(elapsed,boost),boost);
    $('boost').hidden=state!=='running';
    space.render(time/1000,state==='paused'||state==='ended'?0:dt,state!=='intro',playerX,state==='running'?invulnerable:0,reduced.matches,flightSpeed(elapsed,boost),boost);
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
