



## 下载制作好的数据
- [tool_alpaca_for_glm3 数据介绍](http://124.70.99.221:8080/data_share/index?ds_id=65)
- [tool_bench_for_glm3 数据介绍](http://124.70.99.221:8080/data_share/index?ds_id=67)
- [tool_alpaca_for_glm3](https://huggingface.co/datasets/ssbuild/tool_alpaca_for_glm3)
- [tool_bench_for_glm3](https://huggingface.co/datasets/ssbuild/tool_bench_for_glm3)


## 制作数据

### glm3 tools 数据集制作

- [tool_alpaca 原始数据](https://github.com/tangqiaoyu/ToolAlpaca/tree/main/data/train_data.json)
- [tool_bench 原始数据](https://cloud.tsinghua.edu.cn/f/c9e50625743b40bfbe10/)

### 制作数据

```commandline
cd data_sft_tools/glm3
python main.py
```