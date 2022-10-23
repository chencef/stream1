import streamlit as st
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import qrcode
from urllib import parse
from PIL import Image
import datetime
import logging
from datetime import timedelta

#import logging
#logging.basicConfig(filename='example.log')
#logging.debug('This message should go to the log file')

url='http://192.168.1.103:8501/?option='

#用成共享參數
list_data=["user_tel", "buy_name", "buy_tel", "buy_add", "item_name", "item_price", "item_num", "item_total", "buy_date", "buy_time"]

for ss in list_data:
    if ss not in st.session_state:
        st.session_state[ss]=""
        
#st.write(st.session_state)

qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=8,
    border=2
)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">下載您專屬二維條碼 {file_label}</a>'
    return href

##----
#把 streamlit 底部跟左上方 隱藏
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
##----
#把 按鈕放大
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #00cc00; color:black;font-size:15px;height:3em;width:10em;border-radius:10px 10px 10px 10px;
}
</style>""", unsafe_allow_html=True)

def reset_button():  # 把選購按鈕清除
    st.session_state["p1"] = False
    st.session_state["p2"] = False
    st.session_state["p3"] = False    
    return


## 資料庫

if not firebase_admin._apps:
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./cool-key.json')
    # 初始化firebase，注意不能重複初始化
    firebase_admin.initialize_app(cred)
# 初始化firestore
db = firestore.client()

## 資料庫


query_params = st.experimental_get_query_params()

# http://localhost:8501/?option=123

if query_params:  
    query_option = query_params['option'][0] 
#    st.write(query_option)
    st.session_state["user_tel"]= str(query_option)
else:  #無參數，顯示操作者
    #st.write("沒資料關閉")
    #st.write(query_params)
    #st.markdown("# 步驟一 ❄️")
    # with st.sidebar.form(key='my_tel'):
        # text_input = st.sidebar.text_input(label='輸入電話')
        # submit_button = st.sidebar.form_submit_button(label='確定')

    # if submit_button:
        # st.sidebar.write("產生QR Code")
        # st.sidebar.write("產生QR Code")
        # st.sidebar.write("產生QR Code")

    with st.form(key ='Form1'):
        with st.sidebar:
            text_input = st.text_input('輸入手機號碼',"09")              
            submitted1 = st.form_submit_button(label = '確定')
            
    if submitted1:
        if len( text_input) == 10:
            st.session_state["user_tel"]= text_input
            expander = st.expander("專屬條碼" )
           # expander.write("產生QR Code")
            #expander.write("產生QR Code")
            
            qr.add_data(url + parse.quote(text_input))
            print("url:", url + parse.quote(text_input) )
            qr.make()
            img = qr.make_image(fill_color="black", back_color="white")
            img.save('.\qrcode_index.png')  
            image_head = Image.open(".\qrcode_index.png")
            
            expander.image(image_head, caption='您的團購專屬條碼', use_column_width=True)

            #expander.download_button("下載直播主專屬QR-Code")
            # result = Image.fromarray(image_head)
            # expander.markdown(get_image_download_link(result), unsafe_allow_html=True)
            # expander.sidebar.info("請自行按右鍵下載儲存")

            with open(".\qrcode_index.png", "rb") as file:
                btn = expander.download_button(
                        label="下載",
                        data=file,
                        file_name="imagename.png",
                        mime="image/png"
                      )

            ### 把電話號碼新增到資料庫內
            user_list = db.collection('user_buy').get()
            check_user=[]
            for i in user_list:   # 把電話號碼列入矩陣內        
                check_user.append(i.id)
                
            if not text_input in check_user:  #新增
                userID=db.collection("user_buy").document(text_input)
                user_dic= {"number": 0 }
                userID.set( user_dic)
                st.sidebar.write("您為新團購主")
                st.sidebar.write("帳號為:" + text_input)
            
        else:
            st.sidebar.write("輸入電話有誤")
        
    st.sidebar.write("------")
      
    ## 查詢

    with st.form(key ='Form2'):
        with st.sidebar:
            option1 = st.sidebar.selectbox('選擇查詢範圍',("","今日","近三日","近七日"))            
            submitted2 = st.form_submit_button(label = '確定')
            
        if submitted2:
            item_db = db.collection('user_buy').document( st.session_state["user_tel"] ).get()
            
            st.sidebar.write( "目前您共有: "+ str(item_db.to_dict()["number"]) + " 訂單")
            #列出點擊數 X
            
            #列出觀看人數(合作) 
            st.sidebar.write( "購買人如下:")
            db_users = db.collection('user_buy').document( st.session_state["user_tel"] ).collections()
            
            # db_today = datetime.datetime.strptime(st.session_state["buy_date"],"%Y-%m-%d").date()
            # db_today3 = db_today+timedelta(days=3)
            # db_today7 = db_today+timedelta(days=7)
            for db_user in db_users:
         #       db_users = db.collection('user_buy').document( st.session_state["user_tel"] ).collection( db_user.id ).where( 
                st.sidebar.write(db_user.id)
            #列出總金額
            item_db = db.collection('user_buy').document( st.session_state["user_tel"] ).collection( st.session_state["buy_name"] ).document( str(datetime.datetime.now()))
            st.sidebar.write( option1 )

    st.sidebar.write("------")
    
    my_large_df = '''
    Foo, Bar
    123, 中文
    789, 000
    '''
    # 
    st.sidebar.write("下載本日訂購資訊，請自行匯入系統")
    st.sidebar.download_button('下載 CSV 檔',  my_large_df , 'text/csv')
    
   # csv = convert_df(my_large_df)

    # st.sidebar.download_button(
        # label="Download data as CSV",
        # data= my_large_df.to_csv().encode('utf-8'),
        # file_name='large_df.csv',
        # mime='text/csv',
    # )  



st.markdown("<h1 style='text-align: center; color: green;'> 🌍方舟團購🌍 </h1>", unsafe_allow_html=True)

#st.markdown("# 步驟一 🎉 (選擇商品)")
expander1 = st.expander("選擇訂購商品", expanded=True )
#搜尋資料有多少筆資料，做成迴圈顯示
contents = list(db.collection('product').get())  #contents[0].to_dict()['...']  去資料庫找出 品項

order_item = "  "

check1 = expander1.checkbox(label='訂購 ',key="p1")   
expander1.write( "名稱:" + contents[0].to_dict()['item_name'] )
expander1.write( "價格:" + str(contents[0].to_dict()['item_price']) )
select1 = expander1.selectbox( label='訂購數量',key=1, options=list(range(1,6)))   
  
check2 = expander1.checkbox(label='訂購',key="p2")  
expander1.write( "名稱:" + contents[1].to_dict()['item_name'] )
expander1.write( "價格:" + str(contents[1].to_dict()['item_price']) )
select2 = expander1.selectbox( label='訂購數量',key=3, options=list(range(1,6)))   
     
check3 = expander1.checkbox(label='訂購',key="p3")
expander1.write( "名稱:" + contents[2].to_dict()['item_name'] )
expander1.write( "價格:" + str(contents[2].to_dict()['item_price']) )
select3 = expander1.selectbox( label='訂購數量',key=5, options=list(range(1,6)))   
   
expander1.write("------")
if check1:
    order_item = order_item + " (" + contents[0].to_dict()['item_name']+ "，數量:" + str(select1) +")；"
if check2:
    order_item = order_item + " (" + contents[1].to_dict()['item_name']+ "，數量:" + str(select2) +")；"
if check3:
    order_item = order_item + " (" + contents[2].to_dict()['item_name']+ "，數量:" + str(select3) +")；"
    
expander1.write("目前採購項目為" + order_item )
order_money = expander1.button("計算購買金額")

if order_money :   ##計算購買
    total=0
    if check3==False and check2==False and check1==False :
        expander1.write(" 💔 請選購商品 💔")
    else:                     #有選商品
        item_name=[]
        item_price=[]
        item_num=[]
        if  check1==True:
            total= total + select1 * contents[0].to_dict()['item_price']
            item_name.append( contents[0].to_dict()['item_name'] )
            item_price.append( contents[0].to_dict()['item_price'] )
            item_num.append( select1 )
        if  check2==True:
            total= total + select2 * contents[1].to_dict()['item_price']   
            item_name.append( contents[1].to_dict()['item_name'] )
            item_price.append( contents[1].to_dict()['item_price'] )
            item_num.append( select2 )            
        if  check3==True:
            total= total + select3 * contents[2].to_dict()['item_price'] 
            item_name.append( contents[2].to_dict()['item_name'] )
            item_price.append( contents[2].to_dict()['item_price'] )
            item_num.append( select3 )            
        #st.write("購買總金額:  "+ str(total) + "  元")


        if total != 0:
            #["user_tel", "buy_name", "buy_tel", "buy_add", "item_name", "item_price", "item_num", "item_total", "buy_date", "buy_time"]
            if st.session_state["user_tel"] == "":
                expander1.write(" 💔 請在左上側，輸入您的電話 💔")
            else: 
                st.session_state["item_name"]=  item_name
                st.session_state["item_price"]= item_price
                st.session_state["item_num"]=   item_num
                st.session_state["item_total"]= total        
#                st.write(st.session_state)
                expander1.markdown("# "+"購買總金額:  "+ str(total) + "  元")                
                st.markdown(" 💖 已訂購商品完成，(下一步驟)填寫送貨資訊 💖 ")       
        
expander2 = st.expander("填寫送貨資訊", expanded=True )
name_input = expander2.text_input(label='姓名')
tel_input = expander2.text_input(label='電話')
if tel_input.isalpha():
    expander2.write(" 💔 請輸入電話號碼 💔 ")
expander2.write("------")
addr_input=""
choice_addr = expander2.radio("請選擇送貨地點",('店面', '住家(送貨住址)'))
if choice_addr == '店面':
    choice_city=expander2.selectbox( label='縣市',key=11, options=["","aaa","bbb","ccc"]) 
    choice_area=expander2.selectbox( label='鄉鎮',key=12, options=["","111","222","333"]) 
    choice_door=expander2.selectbox( label='店家',key=13, options=["","&&&","***","%%%"])
    addr_input=choice_city+choice_area+choice_door
else:
    addr_input = expander2.text_input(label='送貨住址',key=14)
expander2.write("------")    
expander2.write("送貨地點為 : "+ addr_input)
expander2.write("------")
order_addr = expander2.button(" 確定下單 " , on_click=reset_button) 
       
if order_addr==True:
    if name_input =="":
        st.write("未填寫姓名")
    if tel_input =="":
        st.write("未填寫電話")        
    if addr_input =="":
        st.write("未填寫住址")
    if name_input!="" and tel_input!="" and choice_addr!="" and st.session_state["item_total"] != "":
        e = datetime.datetime.now()
        st.markdown(" 💖 本訂單已於 " + e.strftime("%m/%d %H:%M:%S") + " 訂購完成 💖 ")    
        st.markdown(" 💖 (下一步驟) 觀賞直播送贈品活動 💖 ")  
##寫入資料庫在這裡        
        #["buy_name", "buy_tel", "buy_add", "buy_date", "buy_time"]
        st.session_state["buy_name"]= name_input
        st.session_state["buy_tel"] = tel_input
        st.session_state["buy_add"] = addr_input
        st.session_state["buy_date"]= str(e.date())   #strftime("%m/%d")  加三天後 tomorrow = now + timedelta(days=1)
        st.session_state["buy_time"]= e.strftime("%H:%M:%S")   
        
       # item_db = db.collection('user_buy').document( st.session_state["user_tel"] ).collection( st.session_state["buy_name"] ).document( str(datetime.datetime.now()))
        # db_user = db.collection("user_buy").get()
        
        # for i in db_user:
            # if i == st.session_state["user_tel"]:
                # db_buy_name = db.collection("user_buy").document(st.session_state["buy_name"]).collection( str(datetime.datetime.now()) )
                # db_buy_name.set( st.session_state)
            # else:
            
            
        
        # .
        # if not st.session_state["user_tel"] in db_user:        
            # if not 
        # else:
            
            # db_buy_name = db.collection("user_buy").
            
     ### 把電話號碼新增到資料庫內，有問題??
        # user_list = db.collection('user_buy').document( st.session_state["user_tel"] ).collection( st.session_state["buy_name"] ).get()
        # check_user=[]
        # for i in user_list:   # 把電話號碼列入矩陣內        
            # check_user.append(i.id)
                
        # if not text_input in check_user:  #新增
            # print("ssss:")
            # userID=db.collection("user_buy").document(text_input)
            # user_dic= {"uers": firestore.Increment(1)}
            # userID.set( user_dic)




        #寫入一筆資料
        item_db = db.collection('user_buy').document( st.session_state["user_tel"] ).collection( st.session_state["buy_name"] ).document( str(datetime.datetime.now()))
        item_db.set( st.session_state)
        
        #修正文件參數，把數量變多
        item_num_add= db.collection('user_buy').document( st.session_state["user_tel"] )
        item_num_add.update( {"number": firestore.Increment(1)})        
#        st.write( st.session_state)  

        ## 把參數清空
        #list_data=["user_tel", "buy_name", "buy_tel", "buy_add", "item_name", "item_price", "item_num", "item_total", "buy_date", "buy_time"]
        list_data=["item_name", "item_price", "item_num", "item_total", "buy_date", "buy_time"]
        for ss in list_data:
            st.session_state[ss]=""
        
        ## 把參數寫出
        #st.write( st.session_state) 
    
    else:
        st.markdown(" 💔 您填寫資料有誤 💔 ")    
   # st.write("...:", total ,addr_input, name_input, tel_input)
        
        
expander3 = st.expander("商品影片介紹", expanded=False )

expander3.write("------")         
col1, col2, col3 = expander3.columns(3)

with col1:
    col1.header("米")
    col1.video("https://youtu.be/XINrPEobyB0")

with col2:
    col2.header("果乾")
    col2.video("https://youtu.be/nCHixC6eFp4")

with col3:
    col3.header("介紹")
    col3.video("https://youtu.be/uTteJhzXGkI")    


    
expander4 = st.expander("直播現場", expanded=False )

expander4.write("------")     



    
# col1, col2, col3 = expander4.columns(3)

# with col1:
    # col1.header("A cat")
    # col1.image("https://static.streamlit.io/examples/cat.jpg")

# with col2:
    # col2.header("A dog")
    # col2.image("https://static.streamlit.io/examples/dog.jpg")

# with col3:
    # col3.header("An owl")
    # col3.image("https://static.streamlit.io/examples/owl.jpg")