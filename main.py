import streamlit as st
from multiapp import MultiApp
from pages_dir import welcome, home, data, lstm_page, aqi_now, fb, info, admin, fb_custom, eda, \
    xgboost_page  # import app modules here

app = MultiApp()

# button css
st.markdown("""
  <style>
  div.stButton > button:first-child {
      background-color: rgb(11, 121, 126);
      color:#ffffff;
      border-radius: 50px;
  }





  </style>""", unsafe_allow_html=True)

# Add all your application here
app.add_app("Introduction", welcome.app)
app.add_app("Data", data.app)
app.add_app("Custom Data-Explore", eda.app)
app.add_app("Air quality", aqi_now.app)
app.add_app("LSTM", lstm_page.app)
app.add_app('Facebook Prophet', fb.app)
app.add_app("Choose Dates-Facebook Prophet", home.app)
app.add_app("Custom Dataset-Facebook Prophet", fb_custom.app)
app.add_app("XGBoost", xgboost_page.app)

app.add_app("Metrics", info.app)
app.add_app("Admin", admin.app)

# # The main app
app.run()
