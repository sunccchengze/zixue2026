
// SCZVERSE Shader 04 - for fluid
// Author: SCZ
precision highp float;
uniform float uTime;
uniform vec2 uResolution;
varying vec2 vUv;
void main(){
  vec2 uv = vUv;
  vec3 col = vec3(0.0);
  float t = uTime*1.26;
  col.r = sin(uv.x*10.0 + t)*0.5+0.5;
  col.g = cos(uv.y*8.0 + t*1.2)*0.5+0.5;
  col.b = sin((uv.x+uv.y)*6.0 + t*0.8)*0.5+0.5;
  gl_FragColor = vec4(col,1.0);
}
