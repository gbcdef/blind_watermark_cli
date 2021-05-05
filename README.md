# 说明

```shell
python main.py fixture/abc.png -t 'text watermark' -o embedded.png
```

默认输出的文件名为：<原文件名>_<6位wm密码>_<6位img密码>_<水印长度>.<原扩展名>

务必保留好密码及水印长度，解密提取文字水印时，需要提供密码及水印长度