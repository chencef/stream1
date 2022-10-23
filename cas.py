import streamlit as st
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import qrcode
from urllib import parse
from PIL import Image

url='http://192.168.1.103:8501/?option='
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=3,
    border=2
)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">下載您專屬二維條碼 {file_label}</a>'
    return href



query_params = st.experimental_get_query_params()
if query_params:  # http://localhost:8501/?option=123
    query_option = query_params['option'][0] 
    st.write(query_option)
else:  #無參數，顯示一般 使用者
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
        expander = st.expander("專屬條碼", expanded=False )
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

        
    st.sidebar.write("------")
      
    ## 查詢
    option1 = st.sidebar.selectbox('選擇查詢範圍',("","今日","近三日","本周"))
    if option1 != "":
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

## 以下為 下單資料
#st.markdown("# 步驟一 🎉 (選擇商品)")
#st = st.expander("選擇訂購商品", expanded=False )
if not firebase_admin._apps:
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./cool-key.json')
    # 初始化firebase，注意不能重複初始化
    firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()

#搜尋資料有多少筆資料，做成迴圈顯示
contents = list(db.collection('product').get())  #contents[0].to_dict()['...']

order_item = "  "

check1 = st.checkbox(label='訂購 ',key=2)   
st.write( "名稱:" + contents[0].to_dict()['item_name'] )
st.write( "價格:" + str(contents[0].to_dict()['item_price']) )
select1 = st.selectbox( label='訂購數量',key=1, options=list(range(1,6)))   
  
check2 = st.checkbox(label='訂購',key=4)  
st.write( "名稱:" + contents[1].to_dict()['item_name'] )
st.write( "價格:" + str(contents[1].to_dict()['item_price']) )
select2 = st.selectbox( label='訂購數量',key=3, options=list(range(1,6)))   
     
check3 = st.checkbox(label='訂購',key=6)
st.write( "名稱:" + contents[2].to_dict()['item_name'] )
st.write( "價格:" + str(contents[2].to_dict()['item_price']) )
select3 = st.selectbox( label='訂購數量',key=5, options=list(range(1,6)))   
   
st.write("------")
if check1:
    order_item = order_item + " (" + contents[0].to_dict()['item_name']+ "，數量:" + str(select1) +")；"
if check2:
    order_item = order_item + " (" + contents[1].to_dict()['item_name']+ "，數量:" + str(select2) +")；"
if check3:
    order_item = order_item + " (" + contents[2].to_dict()['item_name']+ "，數量:" + str(select3) +")；"
    
st.write("目前採購項目為" + order_item )
order = st.button("計算購買金額")

if order :
    total=0
    if check3==False and check2==False and check1==False :
        st.write(" 💔 請選購商品 💔")
    else:

        if  check1==True:
            total= total + select1 * contents[0].to_dict()['item_price']
        if  check2==True:
            total= total + select2 * contents[1].to_dict()['item_price']        
        if  check3==True:
            total= total + select3 * contents[2].to_dict()['item_price'] 
        #st.write("購買總金額:  "+ str(total) + "  元")
        st.markdown("# "+"購買總金額:  "+ str(total) + "  元")

    if total != 0:
        st.markdown(" 💖 已訂購商品完成，(下一步驟)填寫送貨資訊 💖 ")       
        
#st = st.expander("填寫送貨資訊", expanded=False)
name_input = st.text_input(label='姓名')
tel_input = st.text_input(label='電話')
st.write("------")
addr_input=""
choice_addr = st.radio("請選擇送貨地點",('店面', '住家(送貨住址)'))
if choice_addr == '店面':
    choice_city=st.selectbox( label='縣市',key=11, options=["","aaa","bbb","ccc"]) 
    choice_area=st.selectbox( label='鄉鎮',key=12, options=["","111","222","333"]) 
    choice_door=st.selectbox( label='店家',key=13, options=["","&&&","***","%%%"])
    addr_input=choice_city+choice_area+choice_door
else:
    addr_input = st.text_input(label='送貨住址',key=14)
st.write("------")    
st.write("送貨地點為 : "+ addr_input)
st.write("------")
order = st.button("確定") 
       
if order==True:
    if name_input =="":
        st.write("未填寫姓名")
    if tel_input =="":
        st.write("未填寫電話")        
    if addr_input =="":
        st.write("未填寫住址")
    if name_input!="" and tel_input!="" and choice_addr!="" :
        e = datetime.datetime.now()
        st.markdown(" 💖 本訂單已於 " + e.strftime("%m/%d %H:%M:%S") + " 訂購完成 💖 ")    
        st.markdown(" 💖 (下一步驟) 觀賞直播送贈品活動 💖 ")  