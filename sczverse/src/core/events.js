
export const Events = {
  listeners:{},
  on(e,fn){ (this.listeners[e]=this.listeners[e]||[]).push(fn); },
  emit(e,data){ (this.listeners[e]||[]).forEach(fn=>fn(data)); },
};
