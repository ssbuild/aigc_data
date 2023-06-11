

##  open data space 数据共享空间

愿景:<br>
  数据联盟小平台，反国内外垄断，反国内外卡脖子。<br>
  加密数据只对贡献成员开放。<br>
<br>
<br>


## 私密数据分享
    http://101.42.176.124:8080

释放6个邀请码
```text
    68812a3a4d1c48e39626aeb47a3f4052KhKC0CLbNQv6KIAgm4i4d0Zj4XiGssLWrcA7TlvjwBg8vydB22S6XEbUwDEOfuFkHrQAilImXCQC5tgMU0TJ9eI9tdP2F3Ni
    7c07076a2ded4fa6aa16bc484b7192a3ZajgaQrTvbSjDegTCyKVg6iKd1hwwLM6onwxew386vCyUh8Ey1E9CsKQdkIv5vFLL6LTRX8bsV7lA9TZ4csbHDKecyVcllk5
    c8a340f435be43ac8e72f265764c987fnRXB9E7hiarIPOrEy3aC5lDzfjArBmjvQP7L3EfBvBnQj7fCpDn1wLKP8dq96sLBw6X5U7Hazkv4MUQ8w9BNqWfyEs5T9WTH
    2df70a0d62d542d8b8919fd63603dc33OMpvf0kOPSkOtRzl0jdv0NO3x5MGccGItIc3WRCLqWA7kWIOTUnkzqFfr3so8AtgpyI2UYlDbNp7H6nUtBNTcr4IwN2gGVe6
    5b461015581c4b46aa979060b899ea94eBumlAmhsA6ZfFMGuXax6L8tjFHGANOnVNTnuOvHuTUXF2HbkNc7jfJXWUMzcAwP8GWBPz2cqlzDL0N5L0Z6Vg2p3Jll1S3M
    67f806e9bd95467889acacc75ff1e3aaDLnjPYcI54tS1YACGQB3t1v5Qcfaua1PPCZQjCRID29XZaFHCTLCtSVXL9jQplzERxg0MBAJsdwESiwGZ6jAGTYAnV04FMXg
```


## 一、 有多少人工，才有多少智能，从0到1构建预训练大语言模型
    搜集开源数据收集、构造，清洗方法，包括预训练数据和指令数据<br>
        ChatGLM-6B 全套微调代码，经过两周对ChatGLM-6B的指令微调，两条经验如下：<br>
    1. glm-6B是经过SFT和RLHF后的版本,另外sft模板未开放，再次微调不够友好<br>
    2. 需要在一个干净的纯基座模型上进行微调（SFT），使用高质量的业务指令数据；RLHF，是一个难题，需要一个高质量的reward model，目前正确的rlhf pipeline比较稀少，训练出来好的效果也是一个挑战。<br>



## 二、 Open-data for LLMs 

 If you like the project, please show your support by leaving a star ⭐.

 | No. |                                            project                                             | description |  secret |
 |-----|:----------------------------------------------------------------------------------------------:|:-----------:|:-------:|
 | 1   |                 [悟道 - 200G](https://data.baai.ac.cn/details/WuDaoCorporaText)                  |             |    不需要秘钥    |
 | 2   |                         [Pile英文数据 - 1.3T的](https://pile.eleuther.ai/)                          |   需要强力清洗    |  不需要秘钥  |
 | 3    | [Tigerbot 中文开源预训练集 - 55G](https://huggingface.co/datasets/TigerResearch/pretrain_zh/tree/main) |             |  不需要秘钥  |


## 三、数据概述
### 1.悟道 - 200G文本  
下载链接：https://data.baai.ac.cn/details/WuDaoCorporaText  
数据格式：
```json
{
        "id": 2,
        "uniqueKey": "074ca2f564544686f0fb6da026e00cac",
        "titleUkey": "231af201b8e7e359f8ab3c1a716dbe86",
        "dataType": "孕育常识",
        "title": "幼儿急疹一定会出疹子吗",
        "content": "婴儿抵抗力低下,时常发生小病小痛,可操碎了做父母的心,相信每个初为人母的妈妈,都会为了孩子的健康成长而对襁褓中的新生儿关怀备至,作为一个合格的妈妈,需要了解更多关于更好的照顾孩子的知识,才能防患于未然。那么幼儿急疹一定会出疹子吗。幼儿急疹一定会出疹子吗 幼儿急疹,也叫烧疹或玫瑰疹,是由病毒感染而引起的突发性皮疹,一年四季都可以发生,尤以春、秋两季较为普遍。常见于出生6个月至1岁左右的宝宝。幼儿急疹的潜伏期大约是10~15天。它虽然是传染性的疾病,却很安全,不会象麻疹、水痘那样广泛传染,家中成员同时患上的机会不大。 症状为宝宝首先是持续3~4天发高烧,体温在39~40度之间,热退后周身迅速出现皮疹,并且皮疹很快消退,没有脱屑,没有色素沉着。这些婴儿在没有出现皮疹前也有发热,热度可以比较高,但是感冒症状并不明显,精神、食欲等都还可以,咽喉可能有些红,颈部、枕部的淋巴结可以触到,但无触痛感,其他也没有什么症状和体症。当体温将退或已退时,全身出现玫瑰红色的皮疹时才恍然大悟,其实这时幼儿急疹已近尾声。幼儿急疹对婴儿健康并没什么影响,出过一次后将终身免疫。幼儿急疹的护理 (1)宝宝要多休息,不剧烈玩耍,体育锻炼暂停。 (2)多喝水,适当的加入果汁,这样即提高了维生素的摄入又利于出汗和排尿,可以促进毒物排出。 (3)宝宝患病期间吃些易消化食物,已经可以吃固体食物的宝宝,此时吃流质或半流质饮食。但是注意尽量要有营养。(不建议喝糖分较高的甜水,宝宝此时食欲不佳,会影响宝宝食欲) (4)刻意的适当补充维生素c和维生素b。 (5)宝宝休息的地方要安静,空气注意流通并保持新鲜。 (6)被子不能盖得太厚太多,这样不利于散热。 (7)注意宝宝的皮肤要保持清洁卫生,经常给孩子擦去身上的汗渍,即防止着凉同时防止出疹的宝宝感染。 (8)体温超过39度时,可用温水或37%的酒精为孩子擦身,防止高热惊厥。(小宝宝不建议酒精降温,如果家长不知道酒 精浓度也不建议给大宝宝使用,对皮肤有刺激性) (9)幼儿急疹是为数不多的出疹可以外出玩耍见风的疾病,但是中医认为此时宝宝体质虚,如果宝宝汗多,则不建议出 门见风。 (10) 此时部分宝宝可能很赖妈妈,希望一直依偎在妈妈怀里,可能是疾病导致宝宝的心理需要。所以请妈妈们尽量满足 宝宝的心理需要,也有利于亲子关系。"
    }
```
<br>

### 2. Pile - 1.3T的英文数据, 需要强力清洗  
下载链接 https://pile.eleuther.ai/  
数据格式：  
```json
{
  "text": "Q:\n\nFor some reason after inputting cin text, the cout comes out blank. Any ideas?\n\nSo I am trying to create a simple Text RPG. But, this one problem is holding me back.\n#include \n\nusing namespace std;\n\nint main()\n{\n int input;\n long Sven;\n long Macy;\n\n cout<<\"Choose your Character- 1.Sven or 2.Macy: \";\n cin>>input;\n cin.ignore();\n\n if ( input == Sven ){\n cout<<\"Welcome to CRPG, my good Sir!\";\n }\n\n if (input == Macy ){\n cout<<\"Girls cant fight, go back: \";\n }\n}\n\nSo this code here is what I have at the moment. When I run the program, it allows me to type the name of the character I want to choose. But, the output is always just a blank area of text. I am more or less new to C++ but, I have nice prior knowledge. Any help is great.\n\nA:\n\nWhat threw me off is when you said it allows me to type the name of the character I want to choose\nIn that case, go ahead with comparing the strings:\nEDIT: As Mohammed suggested, comparing strings can be done directly:\nstring input;\n\ncout<<\"Choose your Character- 1.Sven or 2.Macy: \";\ncin>>input;\ncin.ignore();\n\nif ( input == \"Sven\" ){\n cout<<\"Welcome to CRPG, my good Sir!\";\n}\n\nelse if ( input == \"Macy\"){\ncout<<\"Girls cant fight, go back: \";\n}\n\n", 
  "meta": {"pile_set_name": "StackExchange"}}
```
<br>
=======

### 3. Tigerbot 中文开源预训练集 <br>
下载链接: https://huggingface.co/datasets/TigerResearch/pretrain_zh/tree/main <br>
数据格式：<br>
```json
{
    "dataType": "zh-books", 
    "title ": "格列佛游记", 
    "content ": "格列佛游记 前言一不论是不是真正读过，或者通读过，大约谁都知道《格列佛游记》是一部世界名著。在中国读者中，乔纳森·斯威夫特的名字或者不如莎士比亚、狄更斯、萧伯纳来得响亮，可是他的“小人国”、“大人国”的故事倒差不多称得上家喻户晓了。我记得十多年前中学英语的课本上好像就有过“小人国”游记的节选，当然是简写过的。这么一来，在“家喻户晓”的同时，《格列佛游记》在一般人的心中仿佛成了一本儿童读物。那么到底是不是呢？如果不是，它究竟又是怎样的一部书？《格列佛游记》是一部奇书，但我不同意有些评论家的观点，认为这是一本“儿童读物”。神奇的想象，夸张的手段，寓言的笔法（第四卷），固然是一般儿童读物普遍的特点，但《格列佛游记》是以其杰出的讽刺而垂名世界文学史的，而斯威夫特的大名，至少在英国讽刺作家中，至今仍罕有其匹。也实在是斯威夫特的手段太高明了，把那些乌有之邦的故事讲得煞有介事，连最容易被人忽视的细节也描写得一丝不苟，以致近三百年来多少读者只贪婪地享受书中那异想天开的情节和横生的妙趣……", 
    "id": 1,
    "uniqueKey": "a52408b2792f1fa560f248a42f2bf50d",
    "titleUkey": "3ebac85a97fa2c94aa79ca71491171ae"
}
```
<br>
=======

## 四、数据质量6大标准

数据质量公认的六大评价标准为：完整性、有效性、及时性、一致性、准确性、唯一性。

数据质量六大评价标准

1、数据的准确性

数据的准确性是指数据与其描述的客观实体的特征是否一致，即数据采集值或者观测值和真实值之间的接近程度，也叫做误差值，误差越大，准确度越低。

2、数据的一致性

一致性是指存储在不同的系统中的同一个数据，是否存在差异或相互矛盾。例如航班始发站，在不同系统中记录的应该是同一个站点。

3、数据的唯一性

唯一性用于度量哪些数据是重复数据或者数据的哪些属性是重复的。例如一个人只能有唯一的身份证号码。

4、数据的规范性

规范指的是一项数据存在它特定的格式，规范性用于约束数据按统一标准存储。例如IP地址必定是由 4个0到255间的数字加上”.”组成的手机号码必定是13位的数字。

5、数据的及时性

数据的及时性是指数据从产生到可以查看的时间间隔，也叫数据的延时时长。就是数据能否在需要的时候得到保证。如果数据延时超出统计的要求，就可能导致分析得出的结论失去了意义。特别是业务覆盖多个市场、多个国家的大型企业，如果数据不能及时汇总，会影响到高层决策的及时程度。例如销售日报，用于要求每天统计T-1的销售数据，但是数据只能提供T-2，显然达不到用户的要求。

6、数据的完整性

数据的完整性是从数据采集到的程度来衡量的，是应采集和实际采集到数据之间的比例。指的是数据信息是否存在缺失的情况，数据缺失的情况可能是整个数据记载缺失，也可能是数据中某个字段信息的记载缺失。一个公司数据的完整性体现着这个公司对数据的重视程度。

## 五、数据清洗九大方法
   
清理数据的基础知识
```text
你并不一定始终可控制从数据库、文本文件或网页等外部数据源导入的数据格式和类型。 通常需要先清理数据，才能分析数据。 
```

拼写检查
```text
使用拼写检查不仅可查找拼写错误的单词，还可查找使用不一致的值（如产品或公司名称），只需将这些值添加到自定义词典即可。

```

删除重复行
```text
导入数据时，重复行是一个常见问题。 最好先筛选唯一值，确认结果是所需结果，然后再删除重复值。
```

查找和替换文本
```text
可能需要删除常见的前导字符串（例如后跟冒号和空格的标签）或后缀（例如已过时或不必要的字符串结尾处的附加说明短语）。 若要执行此操作，可查找文本的实例，然后将其替换为无文本或其他文本。
```
更改文本大小写
```text
有时文本格式混乱，尤其是文本大小写方面。 使用三种 Case 函数中的一种或多种，可将文本转换为小写字母（如电子邮件地址）、大写字母（如产品代码）或首字母大写（如姓名或书名）。
```
删除文本中的空格和非打印字符
```text
有时文本值包含前导空格、尾随空格或多个嵌入空格字符（Unicode 字符集值 32 和 160），或非打印字符（Unicode 字符集值 0 到 31、127、129、141、143、144 和 157）。 执行排序、筛选或搜索操作时，这些字符有时会导致意外结果。 例如，在外部数据源中，用户可能会无意添加额外的空格字符，从而导致打字错误，或者从外部源导入的文本数据可能包含嵌入在文本中的非打印字符。 由于这些字符不容易引起注意，因此意外结果可能很难理解。 若要删除这些不需要的字符，可组合使用 TRIM、CLEAN 和 SUBSTITUTE 函数。
```
修复数字和数字符号
```text
主要有两个数字问题可能需要你进行数据清理：无意中将数字导入为文本，以及需要根据你组织的标准更改负号。
```

修复日期和时间
```text
由于存在许多不同的日期格式，并且这些格式可能混杂有编号部件代码或其他包含斜杠标记或连字符的字符串，因此日期和时间通常需要进行转换和重新设置格式。
```

合并和拆分列
```text
从外部数据源导入数据后的常见任务是将两列或多列合并为一列，或将一列拆分为两列或多列。 例如，可能需要将包含全名的列拆分为名字和姓氏。 或者可能需要将包含地址字段的列拆分为单独的街道、城市、地区和邮政编码列。 反之亦可。 可能需要将名字和姓氏列合并为一个全名列，或者将单独的地址列合并为一列。 其他可能需要合并为一列或拆分为多列的常见值包括产品代码、文件路径和 Internet 协议 (IP) 地址。
```


## 欢迎加入
 QQ group 185144988