import jiagu
import pandas as pd
from pyltp import SentenceSplitter
import re
import data
sens_split = SentenceSplitter()

car_dic=[x.replace("\n",'').strip() for x in open('./corpus/car_dic.txt','r',encoding='utf-8')]
cpt_dic = [y.replace("\n",'').strip() for y in open('./corpus/cpt_dic.txt','r',encoding='utf-8')]
user_dic = [z.replace("\n",'').strip() for z in open('./corpus/user_dict.txt','r',encoding='utf-8')]
jiagu.load_userdict(user_dic)


def to_lower_case(filepath,outpath):
    lower_words=[]
    with open(filepath,'r',encoding='utf-8') as f:
        for word in f.readlines():
            flag = re.search('[A-Z]',word)
            if flag!=None:
                lower_words.append(str(word).lower())
    with open(outpath,'w',encoding='utf-8') as w:
        for i,word_ in enumerate(lower_words):
            print(i)
            w.write(word_)

#to_lower_case('./corpus/car_dic.txt','./corpus/lower_car.txt')

def train_test_split(filepath,outpath):
    df_train=pd.read_excel(filepath,sheet_name='训练集')
    df_test = pd.read_excel(filepath,sheet_name='测试集')
    train_row_len = df_train.shape[0]
    test_row_len = df_test.shape[0]
    train_temp=[]
    test_temp=[]
    for i in range(train_row_len):
        sens = df_train.loc[i,'content'].replace("\n","")
        sens_cut = sens_split.split(sens)
        train_temp.extend(sens_cut)

    with open(outpath+'/train_data.txt','a+',encoding='utf-8') as w:
        for sen in train_temp:
            print(sen)
            w.write(sen+"\n")

    for i in range(test_row_len):
        sens = df_test.loc[i,'content'].replace("\n","")
        sens_cut = sens_split.split(sens)
        test_temp.extend(sens_cut)

    with open(outpath+'/test_data.txt','a+',encoding='utf-8') as w1:
        for sen in test_temp:
            print(sen)
            w1.write(sen+"\n")
#train_test_split('./corpus/train_or_test_split.xlsx','./data_path/original')

"""
#=======================================================================
#csv 文件分句转换成文本
def get_data(filepath,sheetname):
    df = pd.read_excel(filepath,sheet-name=sheetname,encoding='gb18030')
    return df
"""

def sens_cut(filepath,outpath,sheetname):
    #f=open(filepath,'r',encoding='utf-8')
    df = pd.read_excel(filepath,encoding='gb18030',sheet_name=sheetname)
    row_len = df.shape[0]
    temp=[]
    for i in range(row_len):
        sens = df.loc[i,'content'].replace("\n","")
        sens_cut = sens_split.split(sens)
        temp.extend(sens_cut)

    with open(outpath,'w',encoding='utf-8') as w:
        for sen in temp:
            print(sen)
            w.write(sen+"\n")



def words_label(filepath,outpath):
    f = open(filepath, 'r', encoding='utf-8')
    i=0
    with open(outpath,'a+',encoding='utf-8') as w:
        for line in f.readlines():

            i=i+1
            space_=[]
            print("正在处理第"+str(i)+"行")
            words = jiagu.seg(line)  # 自定义分词，字典分词模式有效
            for j,word in enumerate(words):
                if word in car_dic:
                   words[j]=word+'/car'
                elif word in cpt_dic:
                    words[j] = word+'/cpt'
                elif 'P' in word:
                    words[j] = word +'/brd'
                elif '\n' in word:
                    words[j] = ''
                    space_.append(j)
                else:
                    words[j] = word + '/o'
            for num in space_:
                del words[num]
            print(words)

            w.write('\t'.join(words)+'\n')
    f.close()
    print("处理结束，一共"+str(i)+"行")



# 将数据进行字符级别实体类型标注
def data_format(filepath,outpath):
    f = open(filepath, 'r', encoding='utf-8')
    i = 0
    with open(outpath, 'a+', encoding='utf-8') as w:
        for line in f.readlines():
            i=i+1
            print("正在处理第"+str(i)+"行")
            if line == '\n':
                continue
            tuple_list = []
            datas = line.strip().split('\t')
            for data in datas:
                temp = tuple(data.strip().split('/'))
                try:

                    if 'cpt' in temp[1]:
                        cpt_len = len(temp[0])
                        ii=0
                        while ii<cpt_len:
                            if ii==0:
                                tagg_cpt=tuple([temp[0][ii],'B-CPT'])
                            else:
                                tagg_cpt = tuple([temp[0][ii], 'I-CPT'])
                            tuple_list.append(tagg_cpt)
                            ii+=1
                    elif 'car' in temp[1]:
                        car_len = len(temp[0])
                        j=0
                        while j<car_len:
                            if j==0:
                                tagg_car = tuple([temp[0][j],'B-CAR'])
                            else:
                                tagg_car = tuple([temp[0][j],'I-CAR'])
                            tuple_list.append(tagg_car)
                            j+=1
                    elif 'brd' in temp[1]:
                        brd_len = len(temp[0])
                        k = 0
                        while k < brd_len:
                            if k == 0:
                                tagg_brd = tuple([temp[0][k], 'B-BRD'])
                            else:
                                tagg_brd = tuple([temp[0][k], 'I-BRD'])
                            tuple_list.append(tagg_brd)
                            k+=1
                    else:
                        else_len = len(temp[0])
                        h = 0
                        while h<else_len:
                            tagg_else = tuple([temp[0][h],'O'])
                            tuple_list.append(tagg_else)
                            h+=1
                except Exception as e:
                    print(temp)
                    continue
                #tuple_list.append(temp)
            #print(tuple_list)
            for tagg_item in tuple_list:
                #print(tagg_item)
                w.write('\t'.join(tagg_item)+'\n')
            w.write('\n')
    f.close()
    print("处理结束，一共" + str(i) + "行")

#================================================================================

"""
sens_cut("./corpus/car_ner_corpus.xlsx","./data_path/original/combine_data.txt","合并")
sens_cut("./corpus/car_ner_corpus.xlsx","./data_path/original/train_data.txt","train")
sens_cut("./corpus/car_ner_corpus.xlsx","./data_path/original/test_data.txt","test")
words_label('./data_path/original/combine_data.txt','./data_path/original/combine_tagged.txt')

words_label('./data_path/original/train_data.txt','./data_path/original/train_tagged.txt')
words_label('./data_path/original/test_data.txt','./data_path/original/test_tagged.txt')
"""
data_format('./data_path/original/combine_tagged.txt','./data_path/combine_format')
data_format('./data_path/original/train_tagged.txt','./data_path/train_data')
data_format('./data_path/original/test_tagged.txt','./data_path/test_data')

data.vocab_build('./data_path/word2id.pkl','./data_path/combine_format',5)
