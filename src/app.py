import streamlit as st
import pandas as pd
import ipaddress
import pytricia
import os
import json
import re
from typing import Optional

drop_chars = [
    ".",
    ",",
    "+",
    "'",
    '"',
    "-",
    "–",
    "_",
    ":",
    "/",
    "\\",
    ":",
    "*",
    "#",
    "|",
]
replace_chars = {
    "&amp;": "&",
    "&quot;": '"',
    "&lt;": "<",
    "&gt;": ">",
}


def string_cleaning_lvl0_str(name: str):
    name = name.lower().strip()
    for char in drop_chars:
        name = name.replace(char, " ")
    for k, v in replace_chars.items():
        name = name.replace(k, v)
    name = re.sub(r"\s+", " ", name)
    return name


class IPLookupService:
    def __init__(self, curr_date: str):
        """Initialize the lookup service with the data file."""
        self.pyt = {}
        self.pyt[4] = pytricia.PyTricia()
        self.pyt[6] = pytricia.PyTricia(128)
        self.pfx_v4 = pytricia.PyTricia()
        self.pfx_v6 = pytricia.PyTricia(128)
        self.df_pfx2org = pd.DataFrame()
        self.df_asn = pd.DataFrame()
        self.org_size_dict = {}
        self.curr_date = curr_date

        self.load_data()

    def load_data(self):
        """Load the data file."""
        path_pfx2org = os.path.join(
            os.getcwd(), "data", f"pfx2org_sample_{self.curr_date}.parquet"
        )
        print(f"Loading data from {path_pfx2org}")
        self.df_pfx2org = pd.read_parquet(path_pfx2org)
        self.df_pfx2org["af"] = self.df_pfx2org["prefix"].apply(
            lambda x: 6 if ":" in x else 4
        )

        for pfx in self.df_pfx2org[self.df_pfx2org["af"] == 4].prefix.unique():
            self.pfx_v4[pfx] = True
        for pfx in self.df_pfx2org[self.df_pfx2org["af"] == 6].prefix.unique():
            self.pfx_v6[pfx] = True

        for af in [4, 6]:
            dd = self.df_pfx2org[self.df_pfx2org.af == af]
            mask = ~dd.prefix.duplicated(keep=False)

            df_curr = dd[mask].set_index("prefix")
            for k, v in df_curr.to_dict(orient="index").items():
                self.pyt[af][k] = [v]

            df_curr = dd[~mask].set_index("prefix")
            grp = df_curr.groupby(df_curr.index)
            for pfx, df_grp in grp:
                self.pyt[af][pfx] = df_grp.to_dict(orient="records")

    def search_by_prefix(self, prefix: str) -> Optional[pd.Series]:
        """Search for an exact prefix match."""
        try:
            # Validate IP prefix format
            ipaddress.ip_network(prefix)
            if "." in prefix:
                prefix = self.pfx_v4.get_key(prefix)
            else:
                prefix = self.pfx_v6.get_key(prefix)
            df_res = self.df_pfx2org[self.df_pfx2org["prefix"] == prefix]
            if df_res.empty:
                return None
            else:
                return df_res
        except ValueError:
            return None

    def search_by_organization(self, org_name: str) -> pd.DataFrame:
        """Search for entries matching the organization name."""
        return self.df_pfx2org[
            self.df_pfx2org["Direct Owner (DO)"].str.contains(
                org_name, case=False, na=False
            )
        ].reset_index(drop=True)


def main():
    tool_name = "Prefix2Org"
    st.set_page_config(page_title=tool_name, layout="wide")

    st.title(tool_name)

    # Initialize the service
    @st.cache_resource
    def load_service():
        return IPLookupService("2025-04-01")

    try:
        service = load_service()
    except FileNotFoundError:
        st.error(
            "Data file not found. Please ensure the data files exist in the application directory."
        )
        return

    # Create tabs for different search types
    tab1, tab2 = st.tabs(["Prefix Search", "Organization Search"])

    # Prefix Search Tab
    with tab1:
        st.header("Search by IP Prefix")
        prefix_input = st.text_input(
            "Enter IP prefix (e.g., 216.1.81.0/24)", key="prefix_search"
        )

        if st.button("Search Prefix", key="search_prefix_btn"):
            if prefix_input:
                try:
                    result = service.search_by_prefix(prefix_input)
                    if result is not None:
                        st.subheader("Result:")
                        col1, col2 = st.columns(2)

                        if len(result) > 1:
                            st.subheader(f"Found {len(result)} results:")
                            st.dataframe(result)
                        else:
                            result = result.iloc[0]
                            with col1:
                                st.write("**Prefix:**", result["prefix"])
                                # st.write(
                                #     f"**Origin ASN:** {result['origin_asn']}",
                                # )
                                # st.write("**RPKI Status:**", result["rpki_status"])
                                # st.write("**Tags:**", result["tag_list"])
                                # if result["ski"]:
                                #     st.write("**RC:**", result["ski"])
                                # else:
                                #     st.write("**RC:**", "N/A")
                            with col2:
                                for col in result.index:
                                    if col == "prefix":
                                        continue
                                    st.write(f"**{col}**:", result[col])
                    else:
                        st.warning("No matching prefix found.")
                except ValueError:
                    st.error("Invalid IP prefix format.")
            else:
                st.warning("Please enter an IP prefix.")

    # Organization Search Tab
    with tab2:
        st.header("Search by Organization")
        org_input = st.text_input("Enter organization name", key="org_search")

        if st.button("Search Organization", key="search_org_btn"):
            if org_input:
                results = service.search_by_organization(org_input)
                if not results.empty:
                    proc_org_input = string_cleaning_lvl0_str(org_input)
                    if proc_org_input in service.org_size_dict:
                        st.subheader("Result:")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Organization:**", org_input)
                            st.write("**Tags:**", service.org_size_dict[proc_org_input])
                        with col2:
                            pass
                    st.subheader(f"Found {len(results)} results:")
                    st.dataframe(results)
                else:
                    st.warning("No matching organizations found.")
            else:
                st.warning("Please enter an organization name.")

    # Show sample data
    with st.expander("View Sample Data", expanded=False):
        st.subheader("Sample Records")
        df = service.df_pfx2org.sample(10, random_state=7).reset_index(drop=True)
        st.dataframe(df, use_container_width=True)

        st.subheader("Dataset Schema")
        schema_info = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            schema_info.append(
                {
                    "Column": col,
                    "Data Type": dtype,
                    "Null Values": null_count,
                    "Sample Value": str(df[col].iloc[0]) if len(df) > 0 else "N/A",
                }
            )

        schema_df = pd.DataFrame(schema_info)
        st.dataframe(schema_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
