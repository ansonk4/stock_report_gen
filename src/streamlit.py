from datetime import date
import streamlit as st
from report_generate import Config, ReportGenerator
import os

def main():

    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["NEWSAPI_KEY"] = st.secrets["NEWSAPI_KEY"]

    st.title("Stock News Report Generator")
    
    stock = st.text_input("Enter Stock Ticker (e.g., AAPL, JPM):")
    
    config = Config()
    generator = ReportGenerator(config)

    if st.button("Generate Report"):
        if stock:
            try:
                with st.spinner('Generating report... This may take a few minutes...'):
                    report, citations = generator.generate_report(stock, report=True)
                    print(report)
                
                st.success("Report generated successfully!")
                
                # Create a container for the report
                with st.container():
                    st.subheader("Full Report")
                    st.markdown("---")  # Horizontal line for visual separation
                    st.markdown(report)
                    # Add download button for the report
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"{stock}_report_{date.today()}.txt",
                        mime="text/plain"
                    )
                    st.markdown("---")
                    st.subheader("Citations:")
                    st.write(citations)

            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
        else:
            st.error("Please enter a valid stock ticker.")

if __name__ == "__main__":
    main()