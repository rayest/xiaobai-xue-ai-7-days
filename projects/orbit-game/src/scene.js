import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const lime = 0xd3f434;
export function createSpace(container) {
  const scene = new THREE.Scene();
  new THREE.TextureLoader().load(`${import.meta.env.BASE_URL}nebula.png`, texture => {
    texture.colorSpace = THREE.SRGBColorSpace;
    scene.background = texture;
  });
  scene.fog = new THREE.FogExp2(0x050e10, .009);
  const camera = new THREE.PerspectiveCamera(48, 1, .1, 220);
  camera.position.set(0, 5, 18);
  camera.lookAt(0, 0, -7);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.7));
  renderer.setClearColor(0x050e10, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.appendChild(renderer.domElement);
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(1,1), .45, .6, .95);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());
  scene.add(new THREE.HemisphereLight(0xc5efe7, 0x071219, 2.1));
  const key = new THREE.DirectionalLight(0xf1f4df, 2.1);
  key.position.set(-5, 9, 7); scene.add(key);
  const rim = new THREE.DirectionalLight(0x65d7c3, 2.5);
  rim.position.set(8, 2, -5); scene.add(rim);

  const white = new THREE.MeshStandardMaterial({ color: 0xc6d9d4, metalness: .52, roughness: .38, flatShading: true });
  const dark = new THREE.MeshStandardMaterial({ color: 0x123238, metalness: .7, roughness: .3 });
  const glow = new THREE.MeshStandardMaterial({ color: lime, emissive: lime, emissiveIntensity: .8, roughness: .4, metalness: .25, flatShading: true });
  const rockMaterial = new THREE.MeshStandardMaterial({ color: 0x244d50, roughness: .87, flatShading: true });
  const rockGeometry = new THREE.IcosahedronGeometry(1, 1);
  // Irregular shared surface avoids identical smooth spheres without loading models.
  const position = rockGeometry.attributes.position;
  for (let i = 0; i < position.count; i++) {
    const x = position.getX(i), y = position.getY(i), z = position.getZ(i);
    const scale = 1 + .15 * Math.sin(x * 15 + y * 7 + z * 12);
    position.setXYZ(i,x*scale,y*scale,z*scale);
  }
  rockGeometry.computeVertexNormals();
  const ship = new THREE.Group();
  function hull(vertices, indices, material) {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(vertices,3));
    geo.setIndex(indices); geo.computeVertexNormals();
    const mesh = new THREE.Mesh(geo,material); ship.add(mesh); return mesh;
  }
  hull([0,.12,-2.1, -.48,-.15,1, .48,-.15,1, 0,.5,.6, 0,-.35,.75], [0,1,3,0,3,2,1,2,3,0,4,1,0,2,4,1,4,2],white);
  const exhausts=[];
  for (const sign of [-1,1]) {
    hull([sign*.22,.05,-1.3, sign*1.9,-.06,1.3, sign*.38,.05,.8,sign*.8,.23,.9], [0,1,3,0,3,2,1,2,3,0,2,1],new THREE.MeshStandardMaterial({color:0xb8ceca,metalness:.4,roughness:.5,side:THREE.DoubleSide,flatShading:true}));
    const engine = new THREE.Mesh(new THREE.CylinderGeometry(.18,.24,.48,6),dark);
    engine.rotation.x = Math.PI/2;engine.position.set(sign*.53,-.04,1);ship.add(engine);
    const exhaust = new THREE.Mesh(new THREE.ConeGeometry(.14,2,12),new THREE.MeshBasicMaterial({color:lime,transparent:true,opacity:.8}));
    exhaust.rotation.x = Math.PI/2;exhaust.position.set(sign*.53,-.04,2.05);ship.add(exhaust);exhausts.push(exhaust);
  }
  const cockpit = new THREE.Mesh(new THREE.ConeGeometry(.3,1.2,4),dark);
  cockpit.rotation.x = -Math.PI/2;cockpit.position.set(0,.3,-.35);ship.add(cockpit);
  scene.add(ship);

  function makeRing(radius=5) {
    const group = new THREE.Group();
    for (const [offset,width,opacity] of [[0,.034,1],[.12,.018,.65],[-.13,.012,.35]]) {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(radius+offset,width,8,120),new THREE.MeshBasicMaterial({color:new THREE.Color(lime).multiplyScalar(2.3),transparent:true,opacity,toneMapped:false})); group.add(ring);
    }
    const ticks = new THREE.Group();
    for (let i=0;i<40;i++) {
      const angle=i/40*Math.PI*2;
      const tick=new THREE.Mesh(new THREE.BoxGeometry(.035,.19,.025),glow);
      tick.position.set(Math.cos(angle)*radius,Math.sin(angle)*radius,0);tick.rotation.z=angle-Math.PI/2;ticks.add(tick);
    }
    group.add(ticks);return group;
  }
  const heroRing=makeRing(4.2);scene.add(heroRing);
  const heroCrystal=new THREE.Mesh(new THREE.OctahedronGeometry(.46),glow);scene.add(heroCrystal);
  const decor=[];
  const placements=[[9,4,-4,1.0],[8,-3,0,1.4],[5,-5,-4,.85],[1,3,-8,.5],[9,0,-12,.55],[-7,2,-18,.45],[0,-3,-8,.35],[12,7,-16,.7],[5,6,-26,1],[-9,-5,-20,.7]];
  for (const [x,y,z,s] of placements) {const rock=new THREE.Mesh(rockGeometry,rockMaterial);rock.position.set(x,y,z);rock.scale.setScalar(s);rock.rotation.set(x,y,z);rock.userData.home=rock.position.clone();scene.add(rock);decor.push(rock);}

  const starsGeo=new THREE.BufferGeometry();
  const stars=[];
  for(let i=0;i<650;i++)stars.push((Math.random()-.5)*150,(Math.random()-.5)*100,-Math.random()*160);
  starsGeo.setAttribute('position',new THREE.Float32BufferAttribute(stars,3));
  const starfield=new THREE.Points(starsGeo,new THREE.PointsMaterial({color:0xadcbc0,size:.065,transparent:true,opacity:.7}));scene.add(starfield);
  const streakGeometry=new THREE.BufferGeometry();
  const streakPositions=new Float32Array(stars.length*2);
  streakGeometry.setAttribute('position',new THREE.BufferAttribute(streakPositions,3));
  const streakMaterial=new THREE.LineBasicMaterial({color:0xb1f6df,transparent:true,opacity:.3});
  const streaks=new THREE.LineSegments(streakGeometry,streakMaterial);streaks.frustumCulled=false;scene.add(streaks);
  const track=new THREE.Group();
  for(const x of [-4.8,-1.6,1.6,4.8]){
    const points=[new THREE.Vector3(x,-1.15,12),new THREE.Vector3(x,-1.15,-140)];
    track.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),new THREE.LineBasicMaterial({color:0x4e8a7a,transparent:true,opacity:.24})));
  }scene.add(track);track.visible=false;
  const items=new THREE.Group();scene.add(items);
  const energyGeometry=new THREE.OctahedronGeometry(.42);
  const checkpoint=makeRing(6.4);checkpoint.position.set(0,0,-70);scene.add(checkpoint);checkpoint.visible=false;
  let mobile=false;
  function resize(){
    mobile=innerWidth<701;
    camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();
    renderer.setSize(innerWidth,innerHeight);composer.setSize(innerWidth,innerHeight);
  }
  window.addEventListener('resize',resize);resize();
  function addItem(kind,lane,z){
    const mesh=new THREE.Mesh(kind==='energy'?energyGeometry:rockGeometry,kind==='energy'?glow:rockMaterial);
    mesh.position.set(lane,0,z);
    if(kind==='rock')mesh.scale.set(.9,1,1.1);
    items.add(mesh);return mesh;
  }
  function render(time,dt,active,playerX,invulnerable,reduceMotion,speed=18,boost=0){
    const targetFov=active&&!reduceMotion?48+boost*12:48;
    camera.fov+=(targetFov-camera.fov)*Math.min(1,dt*5);camera.updateProjectionMatrix();
    for(const exhaust of exhausts){exhaust.scale.y=1+(active?boost*2:0);exhaust.position.z=1.05+exhaust.scale.y;}
    track.visible=active;items.visible=active;checkpoint.visible=active;heroCrystal.visible=!active;heroRing.visible=!active;
    if(active){
      camera.position.lerp(new THREE.Vector3(0,mobile?7:5,mobile?30:18),Math.min(1,dt*4));camera.lookAt(0,0,-9);
      ship.position.set(playerX,0,5);ship.scale.setScalar(.62);ship.rotation.set(0,0,-(playerX-ship.userData.lastX||0)*2.5);ship.userData.lastX=playerX;
      ship.visible=!(invulnerable>0 && Math.floor(time*12)%2===0);
      checkpoint.position.z+=dt*speed;if(checkpoint.position.z>12)checkpoint.position.z=-90;
    }else{
      camera.position.set(0,5,18);camera.lookAt(0,0,-7);
      ship.visible=true;ship.userData.lastX=0;
      ship.position.set(mobile?1.1:2.5,mobile?3.2:-.55,mobile?-4:3);
      ship.rotation.set(.04,-.8,-.13);ship.scale.setScalar(mobile?.9:1.22);
      heroRing.position.set(mobile?1.8:6.0,mobile?3.3:1.25,-3);
      heroRing.rotation.set(.07,-.55,-.36);heroRing.scale.set(mobile?.49:.77,mobile?.83:1.3,1);
      heroCrystal.position.copy(heroRing.position);heroCrystal.rotation.y=time*.6;
      if(!reduceMotion)ship.position.y+=Math.sin(time*.8)*.14;
    }
    for(let i=0;i<decor.length;i++){
      const rock=decor[i];rock.visible=!mobile||i<6;
      if(active){
        // Background rocks stay outside playable lanes so decoration never looks like a missed collision.
        rock.position.x=(i%2?1:-1)*(7+i%4*2);
        rock.position.z+=dt*speed*(.6+(i%3)*.2);
        if(rock.position.z>24)rock.position.z=-110-i*5;
      }else rock.position.copy(rock.userData.home);
      if(!reduceMotion)rock.rotation.y+=dt*.07;
    }
    streaks.visible=active&&!reduceMotion;
    if(active){
      const positions=starsGeo.attributes.position;
      for(let i=0;i<positions.count;i++){
        let z=positions.getZ(i)+dt*speed*(reduceMotion?.35:1);
        if(z>24)z-=184;
        positions.setZ(i,z);
        const j=i*6,x=positions.getX(i),y=positions.getY(i);
        streakPositions[j]=x;streakPositions[j+1]=y;streakPositions[j+2]=z;
        streakPositions[j+3]=x;streakPositions[j+4]=y;streakPositions[j+5]=z-(.15+boost*3.5);
      }
      positions.needsUpdate=true;streakGeometry.attributes.position.needsUpdate=true;
      streakMaterial.opacity=.2+boost*.35;
    }
    composer.render();
  }
  return {scene,addItem,removeItem:mesh=>items.remove(mesh),render,canvas:renderer.domElement};
}
