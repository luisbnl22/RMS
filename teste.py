import streamlit as st
import streamlit.components.v1 as components

html_string = '''
<h1>HTML string in RED</h1>

<script language="javascript">
  document.querySelector("h1").style.color = "red";
  console.log("Streamlit runs JavaScript");
  alert("Streamlit runs JavaScript");
</script>
'''

components.html(html_string)  # JavaScript works

st.markdown(html_string, unsafe_allow_html=True)  # JavaScript doesn't work