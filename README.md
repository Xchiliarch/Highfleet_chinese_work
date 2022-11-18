# 使用说明

发行版汉化地址：[下载](https://github.com/Xchiliarch/Highfleet_chinese_work/releases)

![logo长](https://raw.githubusercontent.com/Xchiliarch/Xchiliarch_Image_Host/master/logo%E9%95%BF.png)

本项目为生成汉化文件的源代码，如只想生成默认的汉化（即与Release内相同的汉化文件），

只需要Pip安装Requirements.txt后依次运行下列代码，即可在build文件夹内生成所有汉化用文件

如想要自己修改汉化内容或添加字体，请根据文件内指示进行操作。



DOOM_SLAYER为一艘魔改的无敌舰船，用于快速完成战斗测试汉化

当然你卡关了也可以用。请不要在船坞内用它进行测试战，会使得游戏闪退

**警告：DOOM_SLAYER无法运行于v1.161版本游戏。**



## **如何更改字体**

对于存在于字库中的字体，你只需要如下所示

![img](https://docimg5.docs.qq.com/image/AgAABTTvR0xQDEyS0sRIuq-aXA1_aFi2.png?w=796&h=152)

![img](https://docimg2.docs.qq.com/image/AgAABTTvR0yWY7s1La1IZK7LObdB7ddt.png?w=769&h=44)

对想要改变字体的部分使用如下格式



```
$字体名称*内容*
```



即可完成字体转换。请严格遵守格式使用Latin半角字符*与$。

**中文输入法下输入￥无法识别**

对于不在字库的字体，可以自己制作，制作办法已附于jupyter内。



## How it works 汉化的原理

### 汉化方法的发现

在dialog文件被解密后， [Mysterious Eistin ](https://steamcommunity.com/id/TheRealEve/myworkshopfiles/?section=guides&appid=1434950) 发现dialog文件会通过形同{animation=event_accident}的代码在游戏内调用图片，而这张贴图恰好是Tex文件夹内已存在的一张贴图。那么可以通过贴图的注册文件即xxx.res中查找，event_accident对应的位置的确是这张贴图。

所以汉化的方法已经呼之欲出：将每个字以贴图的方式存储，在游戏内合适的位置调用即可。但是这种办法在实践的过程中发现了一些缺陷：游戏内并不是所有区域都可调用贴图，也就是说有些地方依然不能汉化，但即使如此，汉化工作也相比起本人的另一份github项目有了长足的进步。

### 汉化的原理

![image-20221031174112004](https://github.com/Xchiliarch/Xchiliarch_Image_Host/blob/master/image-20221031174112004.png)



Dialog文件通过{animation=an_image}发起调用，游戏就会在res中搜寻名称为an_image的注册信息，通过信息中的参数在tex文件中找到这张图片，最后显示在游戏内。

那么如何进行汉化呢？我们只需要将汉化后的文件提取出字符集，然后通过PS将字符集画为一张贴图，使用程序生成其res，就可以在游戏内调用这些字符贴图了。只需要将dialog中的汉字替换为贴图的调用函数即可完成游戏内文字的显示。

![image-20221031180439226](https://github.com/Xchiliarch/Xchiliarch_Image_Host/blob/master/image-20221031180439226.png)







## 致谢

Huge thanks to stopnoanime for decrypting the dialog file of Highfleet , localization would never be possible without your work.

感谢 Homobanana,Iansniper,Commie-Spy,Rogo921,BI-XY,Xchiliarch,Eistin-Yite,OpaqueArc,KagaJiankui,Suesun-1132,xlmzg,LeberechtSchorner 参与汉化工作。



感谢所有参与提交汉化问题的群友。



This project can never be done by me alone.

