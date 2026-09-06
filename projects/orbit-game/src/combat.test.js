import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import {createCombat,laserHits} from './combat.js';

test('laser swept hit detects skipped depth and rejects another lane',()=>{
  assert.equal(laserHits(-16,-24,-20,0,0,1),true);
  assert.equal(laserHits(-16,-24,-20,3.2,0,1),false);
  assert.equal(laserHits(-24,-28,-20,0,0,1),false);
});
test('automatic fire destroys enemies, boss arrives and can be defeated',()=>{
  const scene=new THREE.Scene();let points=0,boss=null,bossKilled=false;
  const combat=createCombat(scene,{kill:(score,isBoss)=>{points+=score;bossKilled ||= isBoss;},boss:value=>boss=value},()=>.5);
  for(let i=0;i<1500;i++)combat.update(.02,0,18,0);
  assert.ok(points>=250,'enemy kill awards score');
  assert.ok(boss,'boss appears after 25 seconds');
  for(let i=0;i<5000&&!bossKilled;i++)combat.update(.02,0,18,1);
  assert.ok(bossKilled,'boss can be killed by real projectiles');
  assert.ok(points>=2250);
  combat.reset();assert.equal(scene.children[0].children.length,0);assert.equal(boss,null);
});
test('enemy bullets damage a player who moves into their lane',()=>{
  let hits=0;const combat=createCombat(new THREE.Scene(),{damage:()=>hits++},()=>.5);
  // Stay away while the first centered enemy prepares its shot, then cross into its lane.
  for(let i=0;i<250;i++)combat.update(.02,-3.2,18,0);
  for(let i=0;i<110;i++)combat.update(.02,0,18,0);
  assert.ok(hits>0);
});
