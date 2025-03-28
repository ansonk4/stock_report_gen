from datetime import date
import streamlit as st
import get_price
from report_generate import Config, ReportGenerator

def main():
    st.title("Stock News Report Generator")
    
    stock = st.text_input("Enter Stock Ticker (e.g., AAPL, JPM):")
    
    config = Config()
    generator = ReportGenerator(config)

    if st.button("Generate Report"):
        if stock:
            try:
                report, citations = generator.generate_report(stock, report=True)
                print(report)
                st.subheader("Full Report")
                st.markdown(report)
                st.subheader("Citations:")
                st.write(citations)

            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
        else:
            st.error("Please enter a valid stock ticker.")

if __name__ == "__main__":
    main()