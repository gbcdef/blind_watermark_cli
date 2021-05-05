# 说明

```shell
# 加盲水印到单个文件
python main.py encode fixture/abc.png -t "text watermark" -o embedded.png

# 加盲水印到文件夹下所有文件
python main.py encodedir fixture/bulk -t "text watermark"

# 提取盲水印
python main.py decode fixture/decode_145239_872640_87.png > mark.txt
```

默认输出的文件名为：<原文件名>_<6位wm密码>_<6位img密码>_<水印长度>.<原扩展名>

务必保留好密码及水印长度，解密提取文字水印时，需要提供密码及水印长度