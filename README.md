# 2024 CCF 国际AIOPS挑战赛数据集
## 数据集下载
🤗 可以通过点击 <a href="https://doi.org/10.5281/zenodo.14286275"><img src="https://img.shields.io/endpoint?&url=https://cdn.jsdelivr.net/gh/logpai/loghub@zenodo/downloads.json&labelColor=1AE&color=DDEEFF&style=flat&label=Downloads"></a> 查看下载数据集详细信息。
## 数据集描述
赛事主办方提供四个ZEDX文档，以及将ZEDX文档解析后得到的txt文件。

### 运维文档zedx源文件
- 大小： 645MB
- 文件格式：zedx文件
- 文件数量：4

### 运维文档zedx解析后的txt文件
- 大小：175MB
- 文件格式：txt文件
- 文件数量：42139

**zedx格式说明**
- 将.zedx替换为.zip，使用unzip等工具解压即可得到html格式文档页
- nodetree.xml中记录了所有文档页的路径和文档标题
- documents/nodes 下的文档页为整个文档的顶层目录
- documents/log.html 中包含了文档中的缩略语

```shell
# 目录结构示意
director
├── doctype.xml
├── documents
│   ├── License申请操作指南
│   ├── TCF部署TECS Director
│   ├── log.html # 缩略语
│   ├── nodes # 顶层目录
...
├── index
├── nodetree.xml # 文档标题及所在路径
└── package.xml
```

### 文档阅读工具eReader
支持在Windows下解压使用，解压后运行run.exe，并将相关文档拖入后，即可进行阅读

## 数据集的格式和描述
### 数据集加载方式
**手动zenodo手动下载**
https://zenodo.org/records/14286275

**git clone with http**
```shell
# 要求安装 git lfs
git clone https://www.modelscope.cn/datasets/issaccv/aiops2024-challenge-dataset.git
```

###

```python
import jsonlines

def read_jsonl(path):
    content = []
    with jsonlines.open(path, "r") as json_file:
        for obj in json_file.iter(type=dict, skip_invalid=True):
            content.append(obj)
    return content

question = read_jsonl('./question.jsonl')
```
