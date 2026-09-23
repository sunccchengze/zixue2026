
export const rand = (a,b)=>Math.random()*(b-a)+a;
export const lerp = (a,b,t)=>a+(b-a)*t;
export const clamp = (v,a,b)=>Math.max(a,Math.min(b,v));
export const dist = (x1,y1,x2,y2)=>Math.hypot(x2-x1,y2-y1);
export const map = (v,a,b,c,d)=>(v-a)/(b-a)*(d-c)+c;
export function shuffle(arr){ return [...arr].sort(()=>Math.random()-0.5); }
export function choose(arr){ return arr[Math.floor(Math.random()*arr.length)]; }
