import * as THREE from 'three';
import { LANES, crossesPlayer } from './rules.js';

export function laserHits(previousZ, z, targetZ, x, targetX, radius) {
  return previousZ >= targetZ - 1 && z <= targetZ + 1 && Math.abs(x - targetX) < radius;
}

export function createCombat(scene, events = {}, random = Math.random) {
  const root = new THREE.Group(); scene.add(root);
  const hullMaterial = new THREE.MeshStandardMaterial({color:0x503a6c,metalness:.65,roughness:.35,flatShading:true});
  const enemyGlow = new THREE.MeshBasicMaterial({color:new THREE.Color(0xff467b).multiplyScalar(2)});
  const laserMaterial = new THREE.MeshBasicMaterial({color:new THREE.Color(0x5cffff).multiplyScalar(2)});
  const hullGeometry = new THREE.OctahedronGeometry(1);
  const orbGeometry = new THREE.SphereGeometry(.18,8,6);
  const laserGeometry = new THREE.BoxGeometry(.07,.07,1.5);
  const particleGeometry = new THREE.OctahedronGeometry(.12);
  const wingGeometry = new THREE.ConeGeometry(.6,2.3,3);
  let enemies=[],shots=[],particles=[],clock=0,nextWave=3,nextBoss=25,gun=0,wave=0;
  function remove(mesh){root.remove(mesh);}
  function explode(position,big=false){
    for(let i=0;i<(big?32:12);i++){
      const mesh=new THREE.Mesh(particleGeometry,i%2?enemyGlow:laserMaterial);mesh.position.copy(position);root.add(mesh);
      particles.push({mesh,life:.7+random()*.4,velocity:new THREE.Vector3((random()-.5)*14,(random()-.5)*10,(random()-.5)*12)});
    }
  }
  function spawnEnemy(lane,boss=false){
    const mesh=new THREE.Group();
    const body=new THREE.Mesh(hullGeometry,hullMaterial);body.scale.set(boss?2.7:1,.45,boss?1.8:.9);mesh.add(body);
    const eye=new THREE.Mesh(orbGeometry,enemyGlow);eye.scale.setScalar(boss?3:1.5);eye.position.set(0,.1,1);mesh.add(eye);
    for(const side of [-1,1]){const wing=new THREE.Mesh(wingGeometry,hullMaterial);wing.rotation.set(Math.PI/2,0,side*.5);wing.position.set(side*(boss?2.2:1.05),0,.35);if(boss)wing.scale.setScalar(1.7);mesh.add(wing);}
    mesh.position.set(LANES[lane],0,-65);root.add(mesh);
    enemies.push({mesh,boss,hp:boss?24:3,maxHp:boss?24:3,age:0,fire:2.5,lane,hit:0});
    if(boss)events.alert?.('警报：外星母舰跃迁进入 · 击破可修复护盾');
  }
  function shoot(x,z,hostile=false){
    const mesh=new THREE.Mesh(hostile?orbGeometry:laserGeometry,hostile?enemyGlow:laserMaterial);mesh.position.set(x,0,z);
    if(hostile)mesh.scale.set(1.6,1.6,2.6);root.add(mesh);shots.push({mesh,hostile});
  }
  function reset(){for(const child of [...root.children])remove(child);enemies=[];shots=[];particles=[];clock=0;nextWave=3;nextBoss=25;gun=0;wave=0;events.boss?.(null);}
  function update(dt,playerX,speed,boost){
    clock+=dt;gun-=dt;
    if(gun<=0){shoot(playerX,3.8);gun=boost>.5?.17:.29;events.fire?.();}
    const bossActive=enemies.some(e=>e.boss);
    if(clock>=nextBoss&&!bossActive){spawnEnemy(1,true);nextBoss=clock+45;}
    else if(clock>=nextWave&&!bossActive){
      const lane=wave===0?1:Math.floor(random()*3);spawnEnemy(lane);
      if(wave>1)spawnEnemy((lane+1)%3);wave++;nextWave=clock+8;
      if(wave===1)events.alert?.('敌机接近 · 自动开火，变道瞄准');
    }
    for(const enemy of enemies){
      enemy.age+=dt;enemy.hit=Math.max(0,enemy.hit-dt);
      enemy.mesh.position.z=Math.min(-18,enemy.mesh.position.z+dt*15);
      if(enemy.boss){
        const target=LANES[Math.floor(enemy.age/4)%3];enemy.mesh.position.x+=(target-enemy.mesh.position.x)*(1-Math.exp(-dt*1.2));
      }
      enemy.mesh.rotation.z=Math.sin(enemy.age*2)*.12;
      enemy.mesh.scale.setScalar(enemy.hit>0?1.1:1);
      enemy.fire-=dt;
      if(enemy.fire<=0&&enemy.mesh.position.z>-40){
        if(enemy.boss){const safe=Math.floor(random()*3);LANES.forEach((x,i)=>{if(i!==safe)shoot(x,enemy.mesh.position.z+2,true);});}
        else shoot(enemy.mesh.position.x,enemy.mesh.position.z+2,true);
        enemy.fire=enemy.boss?1.6:2.6;
      }
    }
    for(const shot of shots){
      const before=shot.mesh.position.z;
      shot.mesh.position.z+=dt*(shot.hostile?24+speed*.08:-85);
      if(shot.hostile){
        if(crossesPlayer(before,shot.mesh.position.z)&&Math.abs(shot.mesh.position.x-playerX)<.85){shot.dead=true;if(events.damage?.()===false)return;}
      }else{
        for(const enemy of enemies){
          if(enemy.hp>0&&laserHits(before,shot.mesh.position.z,enemy.mesh.position.z,shot.mesh.position.x,enemy.mesh.position.x,enemy.boss?2.3:1.05)){
            shot.dead=true;enemy.hp--;enemy.hit=.1;
            if(enemy.hp===0){explode(enemy.mesh.position,enemy.boss);events.kill?.(enemy.boss?2000:250,enemy.boss);}
            break;
          }
        }
      }
    }
    shots=shots.filter(s=>{if(s.dead||s.mesh.position.z<-110||s.mesh.position.z>25){remove(s.mesh);return false;}return true;});
    enemies=enemies.filter(e=>{if(e.hp<=0||(!e.boss&&e.age>18)){remove(e.mesh);return false;}return true;});
    for(const p of particles){p.life-=dt;p.mesh.position.addScaledVector(p.velocity,dt);p.mesh.scale.setScalar(Math.max(0,p.life));}
    particles=particles.filter(p=>{if(p.life<=0){remove(p.mesh);return false;}return true;});
    const boss=enemies.find(e=>e.boss);events.boss?.(boss?{hp:boss.hp,max:boss.maxHp}:null);
  }
  return {update,reset,setVisible:value=>root.visible=value};
}
