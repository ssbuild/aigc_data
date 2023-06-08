# 有多少人工，才有多少智能，从0到1预训练大语言模型
    搜集开源数据收集、构造，清洗方法，包括预训练数据和指令数据<br>


# ChatGLM-6B 全套微调代码，经过两周对ChatGLM-6B的指令微调，两条经验如下：<br>
1. glm-6B是经过SFT和RLHF后的版本，再次微调不够友好<br>
2. 需要在一个干净的纯基座模型上进行微调（SFT），使用高质量的业务指令数据；RLHF，是一个难题，需要一个高质量的reward model，目前正确的rlhf pipeline比较稀少，训练出来好的效果也是一个挑战。<br>



# Open-data for LLMs 

 If you like the project, please show your support by leaving a star ⭐.

 | No. |Projects |                        URL                        | Comments |
 |-----| :-----------:  |:-------------------------------------------------:| :-----------:|
 | 1   |悟道 200G文本 | https://data.baai.ac.cn/details/WuDaoCorporaText  | 
 | 2   |Pile, 1.3T的英文数据|             https://pile.eleuther.ai/             | 需要强力清洗  | 


# 可下载的开源数据集
1，悟道 200G文本，下载链接：https://data.baai.ac.cn/details/WuDaoCorporaText, 数据格式<br>
    {<br>
        "id": 2,<br>
        "uniqueKey": "074ca2f564544686f0fb6da026e00cac",<br>
        "titleUkey": "231af201b8e7e359f8ab3c1a716dbe86",<br>
        "dataType": "孕育常识",<br>
        "title": "幼儿急疹一定会出疹子吗",<br>
        "content": "婴儿抵抗力低下,时常发生小病小痛,可操碎了做父母的心,相信每个初为人母的妈妈,都会为了孩子的健康成长而对襁褓中的新生儿关怀备至,作为一个合格的妈妈,需要了解更多关于更好的照顾孩子的知识,才能防患于未然。那么幼儿急疹一定会出疹子吗。幼儿急疹一定会出疹子吗 幼儿急疹,也叫烧疹或玫瑰疹,是由病毒感染而引起的突发性皮疹,一年四季都可以发生,尤以春、秋两季较为普遍
。常见于出生6个月至1岁左右的宝宝。幼儿急疹的潜伏期大约是10~15天。它虽然是传染性的疾病,却很安全,不会象麻疹、水痘那样广泛传染,家中成员同时患上的机会不大。 症状为宝宝首先是持续3~4天发高
烧,体温在39~40度之间,热退后周身迅速出现皮疹,并且皮疹很快消退,没有脱屑,没有色素沉着。这些婴儿在没有出现皮疹前也有发热,热度可以比较高,但是感冒症状并不明显,精神、食欲等都还可以,咽喉可能
有些红,颈部、枕部的淋巴结可以触到,但无触痛感,其他也没有什么症状和体症。当体温将退或已退时,全身出现玫瑰红色的皮疹时才恍然大悟,其实这时幼儿急疹已近尾声。幼儿急疹对婴儿健康并没什么影响,
出过一次后将终身免疫。幼儿急疹的护理 (1)宝宝要多休息,不剧烈玩耍,体育锻炼暂停。 (2)多喝水,适当的加入果汁,这样即提高了维生素的摄入又利于出汗和排尿,可以促进毒物排出。 (3)宝宝患病期间吃
些易消化食物,已经可以吃固体食物的宝宝,此时吃流质或半流质饮食。但是注意尽量要有营养。(不建议喝糖分较高的甜水,宝宝此时食欲不佳,会影响宝宝食欲) (4)刻意的适当补充维生素c和维生素b。 (5)宝
宝休息的地方要安静,空气注意流通并保持新鲜。 (6)被子不能盖得太厚太多,这样不利于散热。 (7)注意宝宝的皮肤要保持清洁卫生,经常给孩子擦去身上的汗渍,即防止着凉同时防止出疹的宝宝感染。 (8)体
温超过39度时,可用温水或37%的酒精为孩子擦身,防止高热惊厥。(小宝宝不建议酒精降温,如果家长不知道酒 精浓度也不建议给大宝宝使用,对皮肤有刺激性) (9)幼儿急疹是为数不多的出疹可以外出玩耍见风
的疾病,但是中医认为此时宝宝体质虚,如果宝宝汗多,则不建议出 门见风。 (10) 此时部分宝宝可能很赖妈妈,希望一直依偎在妈妈怀里,可能是疾病导致宝宝的心理需要。所以请妈妈们尽量满足 宝宝的心理
需要,也有利于亲子关系。"<br>
    },<br>
<br>
2, Pile, 1.3T的英文数据, 需要强力清洗，下载链接 https://pile.eleuther.ai/, 数据格式：<br>
{"text": "Q:\n\nFor some reason after inputting cin text, the cout comes out blank. Any ideas?\n\nSo I am trying to create a simple Text RPG. But, this one problem is holding me back.\n#include <iostream>\n\nusing namespace std;\n\nint main()\n{\n int input;\n long Sven;\n long Macy;\n\n  cout<<\"Choose your Character- 1.Sven or 2.Macy: \";\n cin>>input;\n cin.ignore();\n\n if ( input == Sven ){\n cout<<\"Welcome to CRPG, my good Sir!\";\n }\n\n if (input == Macy ){\n cout<<\"Girls cant fight, go back: \";\n }\n}\n\nSo this code here is what I have at the moment. When I run the program, it allows me to type the name of the character I want to choose. But, the output is always just a blank area of text. I am more or less new to C++ but, I have nice prior knowledge. Any help is great.\n\nA:\n\nWhat threw me off is when you said it allows me to type the name of the character I want to choose\nIn that case, go ahead with comparing the strings:\nEDIT: As Mohammed suggested, comparing strings can be done directly:\nstring input;\n\ncout<<\"Choose your Character- 1.Sven or 2.Macy: \";\ncin>>input;\ncin.ignore();\n\nif ( input == \"Sven\" ){\n cout<<\"Welcome to CRPG, my good Sir!\";\n}\n\nelse if ( input == \"Macy\"){\ncout<<\"Girls cant fight, go back: \";\n}\n\n", "meta": {"pile_set_name": "StackExchange"}}<br>
<br>


