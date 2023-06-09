## 非开放数据分享

##  制作数据集

    python main.py --input ./input.txt --output ./outputs/output.record


##  制作并上传数据集

    python main.py --user admin --method upload --input ./input.txt --output ./outputs/output.record

##  下载数据集信息

    python main.py --user admin --method download --dataset_name test

##  查看列表

    python main.py --user admin --method list 