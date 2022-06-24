import base64
import os

import streamlit as st


def app():
    """homepage of the app: plot and table"""
    st.title('Metrics')

    """### gif from local file"""
    file_ = open(os.path.join('pages_dir', 'resources', 'metrics2.gif'), "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="forecast gif" height=370px width=100%>',
        unsafe_allow_html=True,
    )

    st.subheader('`MSE`-Mean Squared Error')

    st.write("""
It calculates the difference between each real observation and its predicted value and squares it. Those squares are summed up and divided by the total number of observations. The most useful advantage of MSE is the capacity of determining whether the dataset has unexpected values which should be taken into consideration    """)
    st.latex(r'''
MSE =\frac{1}N \sum_{i=1}^{N} (y_i-\hat{y}_i)^2 \\
         ''')
    with st.expander('View equation explanation'):
        st.latex(
            r'''\textnormal{MSE=Mean Squared Error} \\ \textnormal{N=number of observants}\\ y_i \textnormal{=actual observation} \\ \hat{y}_i \textnormal{=predicted value}''')

    st.subheader('`R2`-R Squared')
    st.write(
        """R Squared, also named the coefficient of determination. It represents a metric which evaluates the accuracy of the model, being related to MSE. Its values range from ∞ to 1, studies showing that the greater its proximity to 1, the better the accuracy.""")

    st.write("""
 It calculates the difference between each real observation and its predicted value and squares it. Those squares are summed up and divided by the total number of observations. The most useful advantage of MSE is the capacity of determining whether the dataset has unexpected values which should be taken into consideration    """)
    st.latex(r'''
 R^2 =1- \frac{\sum (y_i-\hat{y}_i)^2}{\sum (y_i-\overline{y}_i)^2 }\\
          ''')
    with st.expander('View equation explanation'):
        st.latex(
            r'''R^2 \textnormal{=R Squared} \\  y_i \textnormal{=actual observation} \\ \hat{y}_i \textnormal{=predicted value} \\ \overline{y}_i \textnormal{=mean value}''')

    st.subheader('`MAPE`-Mean Absolute Percentage Error')
    st.write(
        """ MAPE usually expresses the accuracy as a ratio defined by the below formula. It is the sum of individual absolute errors divided by the demand. It is the average of the percentage errors.""")

    st.subheader('`MAE`-Mean Absolute Error')
    st.write(
        """MAE is the mean of the absolute error, as its name suggests. It calculates the absolute difference between the predicted and actual values, sums these differences, and divides the sum by the number of observations.""")
    st.latex(r'''
    MAE =\frac{1}N \sum_{i=1}^{N} |y_i-\hat{y}_i| \\
             ''')
    with st.expander('View equation explanation'):
        st.latex(
            r'''\textnormal{MAE=Mean Absolute Error} \\ \textnormal{N=number of observants}\\ y_i \textnormal{=actual observation} \\ \hat{y}_i \textnormal{=predicted value}''')

    with st.expander('\nView more information about these metrics'):
        st.info('https://www.codingprof.com/3-ways-to-calculate-the-mean-absolute-error-mae-in-r-examples/')
        st.info('https://towardsdatascience.com/forecast-kpi-rmse-mae-mape-bias-cdc5703d242d')
        st.info('https://en.wikipedia.org/wiki/Mean_absolute_percentage_error')
