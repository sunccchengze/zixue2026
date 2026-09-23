
export const ZEN_QUOTES = [
  {text:'知是行之始，行是知之成', from:'传习录', author:'王阳明', mood:'💡'},
  {text:'上善若水，水善利万物而不争', from:'道德经', author:'老子', mood:'💧'},
  {text:'本来无一物，何处惹尘埃', from:'六祖坛经', author:'慧能', mood:'🍃'},
  {text:'吾心自足，不假外求', from:'传习录', author:'王阳明', mood:'☯️'},
  {text:'为学日益，为道日损', from:'道德经', author:'老子', mood:'🌀'},
  {text:'菩提本无树，明镜亦非台', from:'六祖坛经', author:'神秀', mood:'🪞'},
  {text:'知行合一，涡轮驱动', from:'承泽宇宙', author:'孙承泽', mood:'🚀'},
  {text:'概率是宇宙的随机，力学是宇宙的必然', from:'承泽手记', author:'SCZ', mood:'🎲'},
  {text:'捏一捏小鹰，烦恼都融化', from:'软物研究所', author:'小鹰', mood:'🦅'},
  {text:'74维叶片，1颗初心', from:'turbine-blade-ai-platform', author:'SCZ', mood:'🌀'},
];
export function randomQuote(){ return ZEN_QUOTES[Math.floor(Math.random()*ZEN_QUOTES.length)]; }
