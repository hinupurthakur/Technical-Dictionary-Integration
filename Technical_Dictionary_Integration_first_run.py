import re,sys,os
e_corpus=sys.argv[1]
h_corpus=sys.argv[2]
dicname=sys.argv[3]
final_dict_created = sys.argv[4]
def read_dic():
    lines=open(dicname,"r").readlines()
    lines = sorted(lines, key=lambda line: len(line.split(" <> ")[0]), reverse=True)
    ewords = []
    hwords = []
    for i in lines :
        str1=re.split(r' <>+ ', i)
        ewords+=str1[::2]  #list slicing 
        hwords+=str1[1::2] #list slicing
        ewords = [x.lower() for x in ewords]
    return ewords,hwords
    
def gen_eng_log() :
    word = []
    eng=open("eng_words.log","w")
    elist,hlist=read_dic()
    f = open(e_corpus, 'r')
    line= f.read()
    line= line.split('\n')
    line=[x.lower() for x in line]
    pattern = re.compile(r'\b(?:' + '|'.join(re.escape(w) for w in elist) + r')\b')
    for i in range(len(line)) :
        j = pattern.findall(line[i])
        for k in j :
            if k != '' :
                str1=k+"\t"+str(i)
                word.append(str1)
    for i in word :
        eng.write(i+'\n') 
def temp_dic_form(logfile) :
    ewords = []
    elist,hlist=read_dic()
    gen_eng_log()
    #print(elist)
    log=open(logfile,'r+')
    word=log.read()
    list1=word.strip().split("\n")
    for i in list1 :
        str1=i.split('\t')
        ewords+=str1[::2]  #list slicing
        #sent_no+=str1[1::2] #list slicing
    list4=[]
    k=0
    for i in range(len(elist)):
        for k in range(len(ewords)):
        #print(elist[i])
        #print(list1[k])
            if elist[i] == ewords[k] :
                str1=ewords[k]+" <> "+hlist[i]
                if str1 not in list4 :
                    list4.append(str1)
            
    f= open("temp.txt","w")
    for i in list4:
        f.write(i)     
def fact_generation() :
    temp_dic_form("eng_words.log")
    log=open("eng_words.log","r")
    word=log.read()
    logs=word.strip().split("\n")
    eng_word = []
    sent_no = []
    final = []
    final_sent = []
    for i in logs :
        list_log=i.split('\t')
        eng_word+=list_log[::2]
        sent_no+=list_log[1::2]
    
    hin_corpus=open(h_corpus,"r")
    corpus=hin_corpus.read()
    corpus=corpus.strip().split('\n') #list of all the Hindi sentences
    dic=open("temp.txt","r")
    dic_data=dic.read()
    dic_data=dic_data.strip().split("\n")
    ewords = []
    hwords = []
    for i in dic_data : #dic_data
        str1=i.split(' <> ')
        ewords+=str1[::2]  #list slicing
        hwords+=str1[1::2] #list slicing
    for i in range(len(corpus)) :
        for j in range(len(sent_no)) :
            if str(i) == sent_no[j] :
                for k in range(len(dic_data)) :
                    if ewords[k] == eng_word[j] :
                        hwords[k] = re.sub(r" ?\([^)]+\)", "", hwords[k])
                        list1 = re.split('; |, |[0-9]. ',hwords[k])
                        while("" in list1) : 
                            list1.remove("")
                        #rint(eng_word[j],sent_no[j],list1)
                        pattern = re.compile(r'\b(?:' + '|'.join(re.escape(w) for w in list1) + r')\b')
                        match = pattern.findall(corpus[i])
                        for s in match :
                            if s != '' :
                                final_sent.append([eng_word[j],s,int(sent_no[j])+1])
                                str1 = ewords[k]+" <> "+s
                                if str1 not in final :
                                    final.append(str1)
                        
    path=os.getenv("HOME_anu_tmp")
    #/home/nupur/tmp_anu_dir/tmp/BUgol2.1E_tmp
    #final_file=path+"/tmp/"+e_corpus+"_tmp/multiword_facts.dat" #name to be confirmed from ma'am
#    final_file="Lookup_of_tech_dictionary_Bhratavani.txt" #name to be confirmed from ma'am
    fact=open(final_dict_created,"w")
    for i in final :
        fact.write(i+"\n")
    return final_sent
final=fact_generation()

