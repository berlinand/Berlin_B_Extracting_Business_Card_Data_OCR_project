import streamlit as st
from streamlit.errors import StreamlitAPIException
from PIL import Image as im,ImageEnhance,ImageFilter
import io
import mysql.connector
import pandas as pd


# Change the connection value in the parameter and database name
connection=mysql.connector.connect(host='localhost',user="root",password="berlin",database="bizcard")
mycursor=connection.cursor()

# This function checks the value given by the user in a MySQL table and returns the matched row.
def check_sql(name,mob):
    query=f"""select * from biscard_details where Name='{name}' and (mobile_1='{mob}' or mobile_2='{mob}') """
    mycursor.execute(query)
    res= mycursor.fetchall()
    b=[]
    c=[]
    for  a in res:
      b.append(a)
    for d in range(0,len(b)):
      c.append("False")
    return b,c

# This function updates the value of a row in a MySQL table based on user input
def save_sql(id,names,occu,mob1,mob2,email,web,address,c_name,s_img):
   query=f"""update biscard_details set Name= %s,Designation = %s,mobile_1 = %s,
      mobile_2 = %s,Email = %s,Website =%s,Address = %s, 
      Company_Name = %s,Original_Image = %s where Id= %s"""
   values = (names, occu, mob1, mob2, email, web, address, c_name, s_img, id)
   mycursor.execute(query,values)
   connection.commit()

# This function deletes the row in a MySQL table that is selected by the user
def delete_sql(id):
   query=f"delete from biscard_details where id={id}"
   mycursor.execute(query)
   connection.commit()


st.title(":violet[RETRIEVE DATA] FOR :blue[UPDATE] AND :orange[DELETE]")
st.warning("Enter the name and mobile number exactly as they appear on the business card. ")
co1,co2=st.columns(2)
name=co1.text_input(label="Enter Cardholder Name")
mobile=co2.text_input(label="Mobile number")
check1=st.checkbox(label="Check")
try:
 if check1==True:
   st.warning("Check one at a time for updates. If deleting multiple data, check them all at once.")
   res,ch=check_sql(name,mobile)

   df=pd.DataFrame(res,columns=["Id","Name","Designation","mobile_1","mobile_2","Email","Website","Address","Company_Name",
           "Original_Image"])
   df.insert(0,"select",ch)

   df1=st.data_editor(
       df,
       column_config={
        "select": st.column_config.CheckboxColumn(
            "select",
            
            default=False,
        )
    },

    hide_index=True,
   )
   df2 = df1[df1['select'] == "True"]
   a=len(df2)
   delete1=st.button(label="Delete" )
   if delete1==True: 
     for x in range(0,len(df2)):
      idd=str(df2.iloc[x][1])
      delete_sql(idd)
     st.rerun()

   for x in range(0,len(df2)):

        c1 = st.container(border=True)
        id=str(df2.iloc[x][1])
        names=c1.text_input(label="CardHolder_Name",value=df2.iloc[x][2],key="a1")
        occu=c1.text_input(label="Designation",value=df2.iloc[x][3],key="a2")
        mob1=c1.text_input(label="mobile 1",value=df2.iloc[x][4],key="a3")
        mob2=c1.text_input(label="mobile 2",value=df2.iloc[x][5],key="a4")
        email=c1.text_input(label="Email",value=df2.iloc[x][6],key="a5")
        web=c1.text_input(label="Website Link",value=df2.iloc[x][7],key="a6")
        address=c1.text_input(label="Address",value=df2.iloc[x][8],key="a7")
        c_name=c1.text_input(label="Company Name",value=df2.iloc[x][9],key="a8")
        s_img = (df2.iloc[x][10])
        img=im.open(io.BytesIO(s_img))
        image_save=c1.image(img)
        u_img=c1.file_uploader(label="Upload the new image",type=['png', 'jpg','jpeg'] )
        if u_img!=None:
          s_img=u_img.getvalue()

        click2=c1.button(label="update")
        if click2==True:
           save_sql(id,names,occu,str(mob1),str(mob2),email,web,address,c_name,s_img) 
        break
except StreamlitAPIException:       
 
   st.warning("The data you are searching for is not in the database. Please enter valid user name and Mobile number")
