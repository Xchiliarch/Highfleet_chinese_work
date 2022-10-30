from genericpath import exists
import imp
from itertools import chain
from xpinyin import Pinyin
import os
import re
import hashlib
p = Pinyin()
def to_pinyin(s):
    return ''.join(chain.from_iterable(p.get_pinyin(s, tone_marks='numbers') ))

def compare(file,texts):
    f= open(file,'rb')              
    chars =  f.read()
    filemd5 = hashlib.md5(chars).hexdigest()
    textmd5 = hashlib.md5(texts.encode('utf-8')).hexdigest()
    if filemd5!=textmd5:
        return 1
    else:
        return 0

def find_all_chara_text(a,font_name):     #输出并返回所有文本出现的单字、符号,以unicode编码排序 All_char.txt  该文档用于检视所有单字与编码检索
    f= open(a,encoding='utf-8')
    texts = f.read()
    f.close()

    font =[]
    for text in texts:
        if( ord(text)>3000 and text not in font):
            font.append(text)
    #font = sorted(font,key = to_pinyin)    #拼音排序
    font = sorted(font)                     #unicode编码排序

    #for item in font:
        #print(item,end='')
    print(f'total length:{len(font)}')      #统计字符数
    all_char =''
    for item in font:
        all_char = all_char+item
    if os.path.exists('.\\int_files\\font') == False:
        os.makedirs('.\\int_files\\font')
    if os.path.exists(f'.\\int_files\\font\\{font_name}all_char.txt'):
        if compare(f'.\\int_files\\font\\{font_name}all_char.txt',all_char):
            print(f'{font_name}字符集内字符发生改变，请重新绘制Tex')
        g = open(f'.\\int_files\\font\\{font_name}all_char.txt','w',encoding='utf-8')
        g.write(all_char)
        g.close()
    return font

def output_font(text,row_num,font_name):  #单字输出到格式化文本 Draw_char.txt. Row_num 为一排字个数  该文档用于PS内绘制贴图
    out =''                                         
    for i in range(len(text)):
        if(i%row_num==0 and i!=0):
            out = out+'\n'+text[i]
        else:
            out = out+text[i]
    if os.path.exists('.\\build\\Tex_Gen') == False:
        os.makedirs('.\\build\\Tex_Gen')
    f = open(f'.\\build\\Tex_Gen\\{font_name}draw_char.txt','w',encoding='utf-8')
    f.write(out)
    f.close()

name_lookup =[] 
def res_registration(font,tex_name,font_name,IcoorX,coorY,rectX,rectY,row_num):  #生成字库Res、字符编码对应集
    name_lookup.clear()
    res = '\n'
    coor = ''
    for i in range(len(font)):                                     
        character = font[i]
        #print(character)
        name = p.get_pinyin(character, tone_marks='numbers')        #获取字符拼音
        if ord(character)>65280 or ord(character) <12291:
            if name == '—':
                name = 'hengang'
            elif name == '‘':
                name = 'Ldanyinhao'
            elif name == '’':
                name = 'Rdanyinhao'
            elif name == '“':
                name = 'Lshuangyinhao'
            elif name == '”':
                name = 'Rshuangyinhao'
            elif name == '…':
                name = 'shenglvehao'
            elif name == '、':
                name = 'dunhao'
            elif name == '。':
                name = 'juhao'
            elif name == '！':
                name = 'gantanhao'
            elif name == '（':
                name = 'Lkuohao'
            elif name == '）':
                name = 'Rkuohao'
            elif name == '，':
                name = 'douhao'
            elif name == '：':
                name = 'maohao'
            elif name == '？':
                name = 'wenhao'

        j = 0
        while(1):
            fname = name+f'_{j}'
            if fname not in name_lookup:
                name_lookup.append(fname)
                break
            j += 1                              #获取字符唯一编码名

        if(i%row_num==0 and i!=0):
            coorY +=rectY
        coorX = (i%row_num)*rectX+IcoorX

        res =  res+(
            f"Animation {font_name}_{fname}\n"
            "{\n"
            f" texture = {tex_name}\n"
            f" rect = {coorX},{coorY},{rectX},{rectY}\n"
            f" hotspot = {rectX//2},{rectY//2}\n"
            f" zorder = 0.000000\n"
            f" resgroup = 0\n"
            f" frame = 1\n"
            "}\n"
        )                                           #打印Res
        coor = coor+fname+'\n'

    if os.path.exists('.\\int_files\\res') == False:
        os.makedirs('.\\int_files\\res')
    f = open(f'.\\int_files\\res\\{tex_name}_{font_name}.res','w',encoding='utf-8')
    f.write(res)
    f.close()
    if os.path.exists('.\\int_files\\font') == False:
        os.makedirs('.\\int_files\\font')
    g = open(f'.\\int_files\\font\\{font_name}lookup.txt','w',encoding='utf-8')
    g.write(coor)
    g.close()

def encode_gen(aa):               #通过chinese.txt生成编码后的english.txt，具有字体fallback机制
    ds = os.listdir('.\\int_files\\font')
    i=0
    fonts_name =[]
    fallback =0
    for d in ds:
        a = re.match('(.*?)lookup.txt',d)
        if(a):
            fonts_name.append(a.groups()[0])
            i+= 1
    for name in fonts_name:
        f= open(f'.\\int_files\\font\\{name}all_char.txt',encoding='utf-8')         
        locals()[f'{name}texts'] = f.read()
        f.close()
        g= open(f'.\\int_files\\font\\{name}lookup.txt',encoding='utf-8')         
        locals()[f'{name}lookup'] = g.read().split('\n')
        g.close()

    f= open(aa,encoding='utf-8')
    originals = f.read()
    f.close()
    
    trans =[]
    default_font_name = 'SH20'
    marker1 =0      #$检测
    counter =0      #*检测（字体套用范围）
    fontname =''
    font_name =  default_font_name
    for item in originals :
        if item =='$':                  #字体更改开始，开始读取字体名称
            marker1 =1
            continue
        if item =='*' and counter ==0:      #字体名称结束，套用范围开始
            marker1 =0
            counter =1
            font_name = fontname
            continue
        if item =='*' and counter ==1:      #套用范围结束
            counter =0
            font_name = default_font_name
            fontname =''
            continue
        if marker1 ==1:                     #读取字体名称
            fontname =fontname+ item
            continue

        try:
            texts = locals()[f'{font_name}texts']
        except KeyError:
            texts = locals()[f'{default_font_name}texts']
            fallback = 1

        try:
            name_lookup = locals()[f'{font_name}lookup'] 
        except KeyError:
            name_lookup = locals()[f'{default_font_name}lookup']
            fallback = 1
        

        if item in texts:
            index= name_lookup[texts.index(item)]           #查询单字index
            if fallback == 0:
                trans.append('{'+f'animation={font_name}_{index}'+'}')
            else:                                                                   #如未查到，fallback到默认字体
                trans.append('{'+f'animation={default_font_name}_{index}'+'}')
                fallback =0
        else:
            if item not in locals()[f'{default_font_name}texts']:
                trans.append(item)                              #非汉字直接加入
            else:
                index= locals()[f'{default_font_name}lookup'][locals()[f'{default_font_name}texts'].index(item)]
                trans.append('{'+f'animation={default_font_name}_{index}'+'}')
                print(f'{item} fall back to {default_font_name}')
                
    if os.path.exists('.\\int_files') == False:
        os.makedirs('.\\int_files')
    f= open('.\\int_files\\english.txt','w',encoding='utf-8')             #输出编码后english.txt
    for tran in trans:  
        f.write(tran)
    f.close()

def check_fonts(file,fonts,default_font):      #输出各字体使用
    f= open(file,encoding='utf-8')         
    chars= f.read()
    f.close()

    f= open(fonts,encoding='utf-8')         
    fonts_used= f.read().split('\n')
    f.close()
    for i in range(len(fonts_used)):
        reg = re.match('(.*?){.*',fonts_used[i])
        font = reg.groups()[0]
        locals()[font]=[]
        fonts_used[i] = font

    pattern ='(#.*)'
    aa =re.findall(pattern,chars)
    for a in aa:
        for font in fonts_used:
            if font == default_font:
                continue
            if re.findall(font,a):
                locals()[font].append(a)

    if os.path.exists('.\\int_files\\usage') == False:
        os.makedirs('.\\int_files\\usage')
    for font in fonts_used:
        if font == default_font:
            continue
        f= open(f'.\\int_files\\usage\\{font}usage.txt','w',encoding='utf-8') 
        for item in locals()[font]:     
            f.write(item)
            f.write('\n')
        f.close()

def res_compile(tex_name):        #将各字体res组成完整贴图res
    ds = os.listdir('.\\int_files\\res')
    i=0
    fonts_name =[]
    for d in ds:
        a = re.match(f'({tex_name}_.*?).res',d)
        if(a):
            fonts_name.append(a.groups()[0])
            i+= 1
    for name in fonts_name:
        f= open(f'.\\int_files\\res\\{name}.res',encoding='utf-8')         
        locals()[f'{name}_res'] = f.read()
        f.close()
    res =(f'Texture {tex_name}\n'
        '{\n'
        f'filename = Media/Tex/{tex_name}.png\n'
        f'resgroup = 0\n'
        '}\n')
    for name in fonts_name:       
        res = res+ locals()[f'{name}_res']
    if os.path.exists('.\\build') == False:
        os.makedirs('.\\build')
    f= open(f'.\\build\\{tex_name}.res','w',encoding='utf-8')         
    f.write(res)
    f.close()

def font_params(fontfile,fontname):     #输出字体参数
    f= open(fontfile,encoding='utf-8')         
    fonts = f.read().split('\n')
    f.close()
    for item in fonts:
        a = re.match('(.*?){(.*?),(.*?),(.*?),(.*?)}',item)
        if a.groups()[0] == fontname:
            return a.groups()

