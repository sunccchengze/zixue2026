
export const TURBINE_DATA = {
  blades:74, // NASA Rotor 37 + extension
  rpm:17188,
  pressureRatio:2.106,
  efficiency:0.877,
  materials:['Ti-6Al-4V','Inconel 718','CMSX-4'],
  stages:[
    {name:'Rotor 37', blades:36, type:'transonic'},
    {name:'Stator', blades:38, type:'supersonic'},
  ],
  nsga: {pop:100, gen:200, objectives:['efficiency','pressureRatio','weight']},
  surrogate:{type:'Kriging + MLP Residual', r2:0.96, uq:'MC Dropout'}
};
