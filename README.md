# 飞机大战   

### 用pygame开发的2D小游戏，根据网上教程搭建的基本框架，自己复杂化了敌机类以及难度系统，增加了一些个性化设计　　　

### 环境配置：python 3.8, 需要安装pygame库    

------------------------
# 基本介绍

### 通过WASD(英文状态)或方向键控制己方飞机移动,自动发射子弹,按空格键可使用全屏炸弹,躲避并击毁敌机增加得分,随着得分增加游戏难度等级也会提升

### ![全屏炸弹补给](/images/bomb_supply.png)　全屏炸弹补给：拾取后增加一枚炸弹数,按空格键使用后摧毁屏幕上所有敌机,上限3枚

### ![超级子弹补给](/images/bullet_supply.png)　超级子弹补给：拾取后发射持续15秒的超级子弹,超级子弹威力翻倍且坚不可摧

### ![增加弹道补给](/images/+1.png)　增加弹道补给：拾取后增加一条弹道

### ![增加伤害补给](images/DAM.png)　增加伤害补给：拾取后我方伤害增加（与当前等级有关)

### ![增加射速补给](/images/ROF.png)　增加射速补给：拾取后增加我方射速

### ![增加射程补给](/images/range.png)　增加射程补给：拾取后增加我方射程

### ![增加生命补给](/images/+life.png)　增加生命补给：拾取后我方生命值+1

### ![增加速度补给](/images/speed.png)　增加速度补给：拾取后我方速度+1


---------------------------
## 准备实现但尚未实现的功能
1、增加敌机发射子弹功能

2、合理设定数值和等级系统

~~3、增加更多我方攻击方法~~    
  
## 考虑可添加功能
1、双人成行

2、增加更多敌人种类和敌人攻击方法

3、设计更多界面

----------------------

## 开发记录  

2023.7.8 完成基本框架的搭建

2023.7.9 新增多种buff与对应设计

2023.7.10 新增自爆敌机与增速buff，新增敌机发射子弹功能

2023.7.11 增加我方升级,优化了难度系统

### 暂时搁置


