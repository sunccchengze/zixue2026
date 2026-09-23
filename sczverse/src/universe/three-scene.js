
import * as THREE from 'three';
export class ThreeScene{
  constructor(){
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, innerWidth/innerHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer({alpha:true, antialias:true});
    this.renderer.setSize(innerWidth, innerHeight);
    this.renderer.domElement.style.position='fixed';
    this.renderer.domElement.style.inset='0';
    this.renderer.domElement.style.zIndex='0';
    this.renderer.domElement.style.pointerEvents='none';
    document.body.prepend(this.renderer.domElement);
    this.camera.position.z=20;
    this.createTorus();
    window.addEventListener('resize',()=>{ this.camera.aspect=innerWidth/innerHeight; this.camera.updateProjectionMatrix(); this.renderer.setSize(innerWidth,innerHeight); });
  }
  createTorus(){
    const geo = new THREE.TorusGeometry(10, 0.3, 16, 100);
    const mat = new THREE.MeshBasicMaterial({color:0x7c5cff, wireframe:true, transparent:true, opacity:0.15});
    this.torus = new THREE.Mesh(geo, mat);
    this.scene.add(this.torus);
    // particles
    const pGeo = new THREE.BufferGeometry();
    const count=2000;
    const pos=new Float32Array(count*3);
    for(let i=0;i<count*3;i++) pos[i]=(Math.random()-0.5)*60;
    pGeo.setAttribute('position', new THREE.BufferAttribute(pos,3));
    const pMat = new THREE.PointsMaterial({size:0.05, color:0x00f5ff, transparent:true, opacity:0.6});
    this.points = new THREE.Points(pGeo, pMat);
    this.scene.add(this.points);
  }
  animate(){
    requestAnimationFrame(()=>this.animate());
    if(this.torus){ this.torus.rotation.x+=0.002; this.torus.rotation.y+=0.003; }
    if(this.points) this.points.rotation.y+=0.0005;
    this.renderer.render(this.scene, this.camera);
  }
}
