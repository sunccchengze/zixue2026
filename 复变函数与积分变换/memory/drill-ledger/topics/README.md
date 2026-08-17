# topics/ · 卡片文件格式

每个课题一个文件：`topicNN-课题名.md`。开卡（新概念交付）时创建；结构如下：

```markdown
# topicNN · 课题名 卡片账本

## 卡片表
| # | concept | S(days) | D(1-5) | last | due | flags | history |

## 计分规则（简化FSRS）
- 新卡：Again S=1.0 / Hard 1.5 / Good 3.0 / Easy 6.0，初始 D=3
- 复习：S' = S×系数（Hard 1.4 / Good 2.2 / Easy 3.0，按 D 与准点率微调）
- Again → S'=max(1.0, S×0.3) 且 D+1
- flags：cw=自信错、leech=累计4次Again（换角度重教不重考）
- 到期卡优先于新内容；单次新卡 ≤7；history 记最近8档
- 会话内重考：Again/Hard 的卡隔约3轮换表面形式再问，只写最终档

## Not yet taught（本课题后续要教的点，备忘）
```
