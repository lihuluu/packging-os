# 包装插画需求分析框架

以**资深包装创意总监**视角进行深度分析的方法论框架。

当前默认业务域是茶叶包装插画。用户没有说明品类时，先按茶叶 SKU、茶礼盒、茶叶标签、茶罐、茶袋或茶叶系列包装判断；明确非茶叶品类时，可使用本框架的通用方法，但要标注缺少该品类专用模块。

## 目的

在生成插画之前，对产品简报进行全面分析，以便：
- 理解产品品类与品牌定位
- 明确插画必须传达的核心视觉故事
- 将主题×构图×风格与品牌及消费者期望精准匹配
- 预判印刷与生产端的约束条件
- 识别竞争白地，找到可占据的视觉领土

## 分析维度

### 1. 产品品类信号 → 推荐主题类型

| 品类 | 首选主题 | 备选主题 |
|----------|----------------|-----------------|
| 茶 / 草本 / 植物 | `botanicals` | `landscape-geography` |
| 茉莉花茶 / 花茶 | `botanicals` | `abstract-botanical` |
| 红茶 / 乌龙 / 黑茶 | `landscape-geography` 或 `cultural-motif` | `vintage-etching` |
| 茶礼盒 / 节庆茶礼 | `pattern-allover` 或 `cultural-motif` | `botanicals` |
| 咖啡 | `landscape-geography` | `lifestyle-scene` |
| 烈酒 / 葡萄酒 | `landscape-geography` 或 `cultural-motif` | `product-hero` |
| 精酿啤酒 | `landscape-geography` | `brand-mascot` |
| 护肤 / 美妆 | `botanicals` 或 `abstract-botanical` | `lifestyle-scene` |
| 保健品 / 营养补剂 | `abstract-botanical` | `botanicals` |
| 零食 / 糖果 | `food-ingredients` | `brand-mascot` |
| 儿童产品 | `brand-mascot` | `wildlife-nature` |
| 蜂蜜 / 蜂产品 | `wildlife-nature` | `botanicals` |
| 手工 / 精酿食品 | `food-ingredients` | `landscape-geography` |
| 文化 / 地域产品 | `cultural-motif` | `landscape-geography` |
| 礼品 / 高端 | `pattern-allover` | `product-hero` |

### 2. 包装物理形态 → 构图约束

| 包装形态 | 最佳构图 | 避免 | 注意事项 |
|-----------|-----------------|-------|-------|
| 圆形瓶 | `wrap-around-360` 或 `central-medallion` | `panel-story` | 标签环绕；注意可视接缝位置 |
| 方形/长方形盒 | `full-bleed` 或 `panel-story` | — | 多面板可做场景延伸 |
| 自立袋 | `full-bleed` 或 `central-medallion` | `wrap-around-360` | 正面是核心视觉面 |
| 金属罐 | `wrap-around-360` | `corner-ornament` | 无缝拼接至关重要 |
| 平袋 / 小包 | `central-medallion` 或 `floating-elements` | `panel-story` | 面积小，插画宜简洁 |
| 广口瓶 | `central-medallion` | `wrap-around-360` | 标签通常为圆形或椭圆形 |
| 软管 | `floating-elements` 或 `border-frame` | — | 长条窄幅格式 |
| 硬质礼盒 | `full-bleed` 或 `corner-ornament` | — | 可在多个面板上使用插画 |

### 3. 品牌定位 → 风格信号

| 定位 | 首选风格 | 备选风格 |
|-------------|--------------|-----------------|
| 高端 / 奢华 | `luxury-line-art` 或 `art-deco-geometric` | `botanical-engraving` |
| 天然 / 有机 | `watercolor-wash` | `botanical-engraving` |
| 传统 / 遗产 | `vintage-etching` 或 `retro-lithograph` | `art-nouveau` |
| 现代 / 极简 | `japanese-minimalist` 或 `modern-flat` | — |
| 趣味 / 活泼 | `children-storybook` 或 `folk-naive` | `gouache-flat` |
| 手工坊 / 精酿 | `linocut-relief` 或 `painterly-expressive` | `watercolor-wash` |
| 文化 / 地域 | `ukiyo-e-woodblock` 或 `folk-naive` | `art-nouveau` |

### 4. 消费者分析

| 维度 | 核心问题 | 对插画的影响 |
|--------|-----------|----------------------|
| **年龄** | 儿童、成人还是老年人？ | 角色风格、画面复杂度 |
| **生活方式** | 都市白领、环保人士、家庭用户？ | 场景/主题选择 |
| **价值观** | 真实感、奢华感、健康、趣味？ | 风格的温度感 vs 精准感 |
| **文化背景** | 西方、中国、日本、全球受众？ | 纹样选择、色彩象征 |

### 5. 色彩象征检查

在推荐配色前，标记以下潜在风险：

| 市场 | 注意事项 |
|---------|-----------|
| 中国市场 | 白色=丧葬；绿帽=出轨；4=死亡 |
| 西方市场 | 黑色=高端 OR 丧葬（视语境而定） |
| 食品包装 | 避免蓝色用于肉类/咸味（抑制食欲） |
| 儿童产品 | 原色系=活泼；粉彩色系=温柔 |
| 高端/奢华 | 金色、深海军蓝、墨绿色、酒红色 |
| 有机/天然 | 大地色系、鼠尾草绿、暖米白色 |

### 6. 印刷与生产说明

| 要求 | 标准 |
|-------------|---------|
| 色彩空间 | CMYK（胶版/柔版印刷） |
| 分辨率 | 最低 300 DPI；精细线描建议 600 DPI |
| 出血 | 四边各 3mm 出血 |
| 压凹/烫金 | 平色块或线描区域适合做工艺效果 |
| 承印材料颜色 | 白卡、牛皮纸（棕色）、镀铝膜——影响色彩呈现 |

## 输出格式

分析结果保存至 `analysis.md`：

```yaml
---
product: "[产品名称与品类]"
pack_type: "[瓶/盒/袋/罐/广口瓶/软管/手提袋/小包]"
brand_positioning: "[高端/天然/趣味/传统/现代/手工坊]"
target_audience: "[简要描述]"
cultural_context: "[主要目标市场]"
---

## 产品故事
[插画必须传达的核心叙事，1-2 句话]

## 核心视觉主张
[这幅插画视觉上最重要的一件事]

## 包装形态分析
- **形态**：[包装类型]
- **核心展示面**：[正面标签 / 全周环绕 / 等]
- **构图约束**：[此形态允许什么 / 禁止什么]

## 品牌与消费者信号
- **定位**：[定位类型]
- **消费者价值观**：[什么能打动这位购买者]
- **视觉语言期待**：[他们在这个品类中期望看到什么]

## 竞争白地
- **品类俗套**：[所有人都在做的、应该回避的]
- **机会点**：[哪片视觉领土尚未被占据]

## 文化与色彩备注
- **风险标记**：[任何象征意义隐患]
- **积极共鸣**：[可借力的文化正向联想]

## 印刷说明
- **色彩空间**：CMYK
- **最低分辨率**：300 DPI
- **承印材料**：[白卡 / 牛皮纸 / 镀铝膜 / 其他]
- **特殊工艺**：[压凹区域 / 烫金区域（如适用）]

## 推荐组合方案
1. **[主题] × [构图] × [风格]**（推荐）：[一句话说明理由]
2. **[主题] × [构图] × [风格]**：[理由]
3. **[主题] × [构图] × [风格]**：[理由]

## 设计指令（来自用户输入）
[用户简报中明确提出的颜色、氛围、参考或约束条件]
```

## 分析检查清单

进入插画简报阶段前确认：

- [ ] 是否理解了产品品类与核心主张？
- [ ] 是否明确了包装物理形态及其构图约束？
- [ ] 是否将品牌定位映射到了风格信号？
- [ ] 是否考虑了目标消费者的视觉期待？
- [ ] 是否检查了文化/色彩象征意义风险？
- [ ] 是否识别了品类俗套（需要回避的）？
- [ ] 是否记录了印刷/生产约束条件？
- [ ] 是否提供了 3 个「主题×构图×风格」组合及各自理由？
