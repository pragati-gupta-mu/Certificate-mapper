
import streamlit as st
import openpyxl
from agent_api import call_agent

def main():
    st.title("Certificate Mapper Agent UI")
    st.write("Upload your Excel file, select columns to send to the agent, and choose columns to update.")

    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    if uploaded_file:
        wb = openpyxl.load_workbook(uploaded_file)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            st.error("No rows found in the uploaded file.")
            return
        headers = rows[0]
        st.write("Columns in your file:", headers)
        columns_to_send = st.multiselect(
            "Select columns to send to agent:", headers, default=[]
        )

        new_cert_header = st.selectbox(
            "Select the new certificate name header:", headers
        )

        remark_header = st.selectbox(
            "Select the remark header:", headers
        )
        start_row = st.number_input("Start row (inclusive)", min_value=2, value=2, step=1)
        end_row = st.number_input("End row (inclusive)", min_value=start_row, value=start_row, step=1)
        row_numbers = ",".join(str(i) for i in range(start_row, end_row + 1))
        if st.button("Run Agent on Selected Rows"):
            try:
                row_nums = [int(x.strip()) for x in row_numbers.split(",") if x.strip().isdigit()]
                st.write(f"Rows to update: {row_nums}")
                for idx in row_nums:
                    if idx < 2 or idx > len(rows):
                        st.warning(f"Row {idx} is out of range.")
                        continue
                    row = rows[idx-1]
                    row_dict = {header: value for header, value in zip(headers, row) if header in columns_to_send}
                    st.write(f"Sending to agent: {row_dict}")
                    # Here you would call your agent logic and get the result
                    # result = call_agent(row_dict)
                    # For demo, just echo
                    result = call_agent(row_dict)
                    print(result)
                    ws.cell(row=idx, column=headers.index(new_cert_header) + 1, value=result.get("newCertificateName"))
                    ws.cell(row=idx, column=headers.index(remark_header) + 1, value=result.get("remark"))

                    #result = {col: f"Updated {col}" for col in columns_to_update}
                    # st.write(f"Agent result: {result}")
                    # # Update the Excel file (in-memory)
                    # for col in columns_to_update:
                    #     col_idx = headers.index(col) + 1
                    #     ws.cell(row=idx, column=col_idx, value=result[col])
                # Save updated file
                output_path = "updated_" + uploaded_file.name
                wb.save(output_path)
                st.success(f"Updated file saved as {output_path}")
                with open(output_path, "rb") as f:
                    st.download_button("Download updated file", f, file_name=output_path)
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
