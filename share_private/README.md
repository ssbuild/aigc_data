## 非开放数据分享

##  制作数据集

    - text 格式

        python main.py --input=./input.txt --output=./outputs/output.record --dataset_type=text  --dataset_name=test数据集 --dataset_desc=test
    
    - json 格式

        python main.py --input=./input.txt --output=./outputs/output.record --dataset_type=json  --dataset_name=test数据集 --dataset_desc=test

    - csv 格式

        python main.py --input=./input.txt --output=./outputs/output.record --dataset_type=csv  --dataset_name=test数据集 --dataset_desc=test

##  制作并上传数据集

    python main.py --user admin --method upload --input=./input.txt --output=./outputs/output.record --dataset_type=text  --dataset_name=test数据集 --dataset_desc=test

##  下载数据集信息

    python main.py --user admin --method download --dataset_name test

##  查看列表

    python main.py --user admin --method list 