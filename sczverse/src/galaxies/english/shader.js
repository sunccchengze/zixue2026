
export const SHADER = `
// english galaxy shader
precision highp float;
uniform float uTime;
varying vec2 vUv;
void main(){
  vec2 uv=vUv;
  float c = sin(uv.x*10.0 + uTime)*0.5+0.5;
  gl_FragColor = vec4(vec3(c),1.0);
}
`;
