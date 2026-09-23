export const DISCIPLINES = [
  {
    id:'probability', name:'概率论与数理统计', en:'Probability', emoji:'🎲', color:'#ffcc00', dark:'#8a6d00',
    progress:85, tasks:12,
    desc:'随机性是宇宙的源代码。课题01-08已完成，大数定律待开。',
    realProgress:{done:['课题01-概率是什么','课题02-条件概率','课题03-随机变量','课题04-分布函数','课题05-随机变量函数','课题06-期望','课题07-方差协方差','课题08-矩生成特征函数'], next:'课题09-大数定律'},
    formulas:['P(A|B)=P(AB)/P(B)','E[X]=∫x f(x)dx','Var(X)=E[X²]-E[X]²','φ(t)=E[e^{itX}]','切比雪夫: P(|X̄-μ|≥ε)≤σ²/(nε²)'],
    textbook:'茆诗松《概率论与数理统计》',
    exam:'学习通8章测验已完成80题'
  },
  {
    id:'mathphys', name:'数理方程', en:'Math Physics', emoji:'🌊', color:'#00f5ff', dark:'#006a80',
    progress:20, tasks:8,
    desc:'用偏微分方程描述振动与热传导。定解问题攻关中。',
    realProgress:{done:['定解问题校准'], next:'波动方程'},
    formulas:['波动: u_tt = a² u_xx','热传导: u_t = a² u_xx','拉普拉斯: Δu=0','定解: 方程+初值+边值','分离变量: u=XT'],
    textbook:'数学物理方程',
    location:'主楼C-204 周一1-2/周三3-4'
  },
  {
    id:'mechanics', name:'工程力学', en:'Mechanics', emoji:'🏗️', color:'#ff8a00', dark:'#7a3d00',
    progress:45, tasks:10,
    desc:'力与平衡。课题01-02已验收，课题03平面任意力系攻关中。',
    realProgress:{done:['课题01-静力学公理','课题02-平面汇交力系与力偶系'], next:'课题03-平面任意力系简化与平衡'},
    formulas:['平衡: ΣF=0, ΣM=0','力矩: M=r×F','力偶: 自由矢量','二力杆: 力沿连线','主矢+主矩'],
    textbook:'杨庆生《工程力学》第三版',
    homework:'9-18作业2-1/3-1/3-2, 9-20作业2-2/2-7, 9-22作业1-2',
    location:'主楼C-304 周二3-4/周五1-2'
  },
  {
    id:'complex', name:'复变函数', en:'Complex', emoji:'🌀', color:'#7c5cff', dark:'#3a1a8a',
    progress:30, tasks:9,
    desc:'复平面是另一个维度。课题01复数与复平面收口中，作业已完成。',
    realProgress:{done:['复数运算','辐角','欧拉公式校准'], next:'棣莫弗/共轭/柯西-黎曼'},
    formulas:['e^{iθ}=cosθ+i sinθ','|z|=√(x²+y²)','z·z̄=|z|²','(cosθ+i sinθ)^n=cos nθ+i sin nθ','C-R: u_x=v_y, u_y=-v_x'],
    textbook:'复变函数与积分变换',
    homework:'P24作业1(2)(4)/8(4)(6)/14(3)(4)/19/22(3)(10)/26/31/32, P47作业已完成',
    location:'主楼A-404 周一5-6/周三3-4'
  },
  {
    id:'physics', name:'大学物理', en:'Physics', emoji:'⚛️', color:'#00ff88', dark:'#006a3a',
    progress:25, tasks:11,
    desc:'从简谐振动到量子。机械振动校准中，第十二次作业机械波24题。',
    realProgress:{done:['质点运动学回顾'], next:'机械振动五站'},
    formulas:['简谐: x=A cos(ωt+φ)','ω=√(k/m)','v=-Aω sin, a=-Aω² cos','旋转矢量','拍: |ω1-ω2|'],
    textbook:'大学物理 II-2',
    location:'中2-3203 周二1-2/周四5-6, 仲英楼B401 周一9-10实验',
    teacher:'常泽圣/潘雪峰/宋鹏涛/张二虎/张凯'
  },
  {
    id:'chemistry', name:'大学化学', en:'Chemistry', emoji:'🧪', color:'#ff5c8a', dark:'#7a3a3a',
    progress:60, tasks:10,
    desc:'分子与反应。真题解剖14份，三卷C档已就绪，决战程序中。',
    realProgress:{done:['前四章期中','首周课堂信息转录'], next:'决战三卷-镜中院'},
    formulas:['ΔH=ΔU+PΔV','ΔG=ΔH-TΔS','K=exp(-ΔG/RT)','速率: v=k[A]^m[B]^n','电极: E=E°-RT/nF lnQ'],
    textbook:'大学化学',
    location:'教2楼-西307 周三1-2/周五3-4, 中1-3125 周一3-4实验',
    teacher:'张雯/张淼, 实验吴勇'
  },
  {
    id:'eastern', name:'东方智慧', en:'Eastern Wisdom', emoji:'☯️', color:'#ffffff', dark:'#666',
    progress:70, tasks:20,
    desc:'知行合一，无为，本来无一物。3/20已完成，Track 5。',
    realProgress:{done:['主题01-传习录-知行合一(8.8/10封档)','主题02-道德经-无为','主题03-六祖坛经-本来无一物'], next:'主题04-侘寂(待换书)'},
    formulas:['知是行之始，行是知之成','上善若水','本来无一物，何处惹尘埃','打脸链路=知行合一实验室'],
    method:'预测→实验→打脸→修正→记录',
    location:'打脸链路'
  },
  {
    id:'papers', name:'论文精读', en:'Papers', emoji:'📄', color:'#8affff', dark:'#2a5a5a',
    progress:40, tasks:12,
    desc:'ML in ASO，涡轮叶片气动优化，你的科研主线。',
    realProgress:{done:['P01《ML in ASO》103页/47图会话01第1轮','白皮书v2 15/15单元'], next:'v3 AI教练训练场'},
    formulas:['Kriging: y(x)=μ+Z(x)','PCA/DMD: 协方差特征值','NSGA-II: 非支配排序','MC Dropout: UQ','RANS/Euler + PINN'],
    project:'turbine-blade-ai-platform: NASA Rotor37/74维/残差代理/NSGA-II/MC Dropout',
    plan:'12篇论文/51会话'
  },
  {
    id:'english', name:'学术英语', en:'Academic English', emoji:'🌍', color:'#ffaa00', dark:'#6a4400',
    progress:50, tasks:6,
    desc:'国际学术交流，blended learning，第二课堂15分。',
    realProgress:{done:['16周课程表','治国理政语料库第二卷150词'], next:'组4人队+词汇测试10-01~11-30'},
    formulas:['Research Presentation=期末口试(15-16周)','SPOC线上: 4/6/8/13周','三项第二课堂: 词汇/听写/摘抄'],
    location:'外文楼A-612 周四1-2',
    teacher:'邵娟'
  },
  {
    id:'ai', name:'人工智能基础', en:'AI Basics', emoji:'🤖', color:'#00ffcc', dark:'#006a5a',
    progress:35, tasks:11,
    desc:'BPE分词器，唐杰2026清华作业清单7条本地化，16周11课题。',
    realProgress:{done:['三轨合一标准骨架','9份章程+M0-M9知识地图+22项资源'], next:'课题01 BPE分词器'},
    formulas:['BPE: Byte Pair Encoding','Transformer: Attention(Q,K,V)','Kaggle 2×T4 30h/周','大论文70%+平时30%'],
    location:'东1东-328 周三9-10/周五9-10',
    teacher:'陈炜煌'
  },
];
