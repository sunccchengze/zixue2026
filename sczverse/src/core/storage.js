
export const Storage = {
  get(k,d=null){ try{ return JSON.parse(localStorage.getItem(k))||d; }catch{ return d; } },
  set(k,v){ localStorage.setItem(k, JSON.stringify(v)); },
  inc(k){ const v=(this.get(k,0)||0)+1; this.set(k,v); return v; }
};
