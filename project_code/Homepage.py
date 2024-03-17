import streamlit as st
import easyocr as oc
from PIL import Image as im
import io




def reader_file(up_file):
        result=up_file.getvalue()
        reader=oc.Reader(['en'])
        result1 = reader.readtext(result)
        st.write(result1)

st.header("BizCardX: Extracting Business Card Data with OCR")
up_file=st.file_uploader(label="Upload the image",type=['png', 'jpg','jpeg'] )

if up_file != None:
  st.image(up_file)
  
  
click1=st.button(label="submit")
if click1 == True:
   reader_file(up_file)


  