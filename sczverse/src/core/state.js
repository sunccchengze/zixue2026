
export class State{
  constructor(){
    this.explored = new Set(JSON.parse(localStorage.getItem('scz-explored')||'[]'));
    this.zen = parseInt(localStorage.getItem('scz-zen')||'0');
    this.mood = localStorage.getItem('scz-mood')||'😊';
  }
  explore(id){
    this.explored.add(id);
    localStorage.setItem('scz-explored', JSON.stringify([...this.explored]));
  }
  addZen(n){
    this.zen = Math.min(100,this.zen+n);
    localStorage.setItem('scz-zen', this.zen);
  }
}
