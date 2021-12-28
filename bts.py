import pandas as pd
import re
import numpy as np
import plotly_express as px
import streamlit as st
from matplotlib import pyplot as plt
from datetime import datetime

st.set_page_config(page_title="dashboard",
                    page_icon=":bar_chart:",
                    layout="wide")


def style_negative(v, props=''):
    if isinstance(v,str):
        return None
    else:
        return props if v < 0 else None

now = datetime.now()



fname = "tv_vs_pop_hist_rec.csv"
columns = ['DATE','POP SOFTWARE NAME','TV_SOFTWARE_NAME','LICENSE_REQUIRED','POP QTY','TV QTY','VARIANCE']
   
tv_vs_pop_hist_rec = pd.read_csv(fname)
tv_vs_pop_hist_rec['DATE'] = tv_vs_pop_hist_rec['DATE'].astype('str')

tv_vs_pop_hist_rec['TV_SOFTWARE_NAME'].fillna('',inplace=True)
tv_vs_pop_hist_rec['LICENSE_REQUIRED'].fillna('',inplace=True)

st.sidebar.header("Please enter Date")
date = st.sidebar.multiselect(
        "Select the Date for BTS INVENTORY COUNT LICENSE AND NO LICENSE:",
        options=tv_vs_pop_hist_rec["DATE"].unique(),
        default=tv_vs_pop_hist_rec["DATE"].unique()
        
)
st.sidebar.header("Please enter License Required")
license = st.sidebar.multiselect(
        "Select the License for: "
        "BTS INVENTORY COUNT LICENSE AND NO LICENSE:",
        options=tv_vs_pop_hist_rec["LICENSE_REQUIRED"].unique(),
        default=tv_vs_pop_hist_rec["LICENSE_REQUIRED"].unique()
        
)


df_selection = tv_vs_pop_hist_rec.query(
    "DATE == @date & LICENSE_REQUIRED == @license "
)


SWCNT = 7
NCOLS = 2

if SWCNT % NCOLS > 0:
    NROWS = SWCNT//NCOLS + 1
else:
    NROWS = SWCNT//NCOLS

HEIGHT = SWCNT*2
WIDTH = 15

# get the date of the latest 5 TV reports ordered ascending
newest_5_weeks = df_selection.sort_values('DATE')['DATE'].unique()[-5:]
newest_date = newest_5_weeks.max()

top_sw_by_qty = df_selection[df_selection['DATE'] == newest_date].sort_values(
    'TV QTY',ascending=False).head(SWCNT)['TV_SOFTWARE_NAME']
top_sw_by_qty = list(top_sw_by_qty.str.replace('(','\(').str.replace(')','\)').str.replace('+','\+'))


fig, axes = plt.subplots(nrows=NROWS, ncols=NCOLS, figsize=(WIDTH,HEIGHT), tight_layout=True)
fig.suptitle(f'TOP {SWCNT} SOFTWARE\nBY TEAMVIEWER INVENTORY COUNT', y=1, fontsize=20)
plt.subplots_adjust(wspace=0.05,  # horizontal padding
                    hspace=0.3)   # vertical padding

cntr = 0
for x in range(NROWS):
    for y in range(NCOLS):
        if cntr == SWCNT:
            axes[x,y].axis('off')
            break
        product = top_sw_by_qty[cntr].upper()
#         filter = tv_vs_pop_hist_rec['TV SOFTWARE NAME'].str.contains( product,flags=re.IGNORECASE)
        newest_5_filter = df_selection.apply(lambda row: 
                                True if (row['DATE'] >= newest_5_weeks.min()) and\
                                        (re.search(product,row['TV_SOFTWARE_NAME'],flags=re.IGNORECASE))\
                                                     else False, axis=1)
        plot_data = df_selection[newest_5_filter].set_index('DATE')
        plot_data.plot(kind='barh',ax=axes[x,y], align='center', width=.7,color=['mediumaquamarine','steelblue','sandybrown'])
        product = re.sub(r'\\','',product)
        axes[x,y].legend(loc='upper right')
        axes[x,y].set_title(product.upper(),fontdict={'fontsize':14})
        axes[x,1].set(yticklabels=[])
        axes[x,y].set_ylabel('TEAMVIEWER INVENTORY DATE',fontdict={'fontsize':12})
        axes[x,1].set_ylabel('')
        cntr += 1

plt.savefig(f"top {SWCNT} by tv count.jpg", dpi=300, bbox_inches='tight')

# display related dataframe
filter = df_selection['TV_SOFTWARE_NAME']!=''
hist_dates = df_selection['DATE'].unique()
hist_dates = hist_dates[-3:]  # build table with 5 weeks worth of data
sw_names = df_selection.loc[filter,'TV_SOFTWARE_NAME'].unique()
summary_df = pd.DataFrame({'SW NAME':sw_names})

for d in hist_dates:

    col_date = d[4:6] + '-' + d[6:]
    columns = ['SW NAME',f'POPQ {col_date}',f'TVQ {col_date}',f'VAR {col_date}']
    
    filter = df_selection.apply(lambda row: True if (row['DATE'] == d) and 
                                      (row['TV_SOFTWARE_NAME'] != '') else False,axis=1)
    temp_df = df_selection.loc[filter,['TV_SOFTWARE_NAME','POP QTY','TV QTY','VARIANCE']]
    temp_df.columns = columns
    
    summary_df = summary_df.merge(temp_df, on='SW NAME', how='outer')

summary_df.reset_index(drop=True,inplace=True)
columns = summary_df.columns
sort_col = list(columns[-2:-1])

summ_df = summary_df.sort_values(sort_col,ascending=False).reset_index(drop=True).astype(str)
summ_df.head(SWCNT).style.format(thousands=',',na_rep='',precision=0)\
             .applymap(style_negative,props='color:red;')


dt_string = '20211220'

fname1 = "tv_vs_pop_obsolet.csv"
columns = ['DATE','Software_Tag','License_Required','TV_Qty']
   
tv_vs_pop_obsolet = pd.read_csv(fname1)
tv_vs_pop_obsolet['DATE'] = tv_vs_pop_obsolet['DATE'].astype('str')

tv_vs_pop_obsolet['Software_Tag'].fillna('',inplace=True)
tv_vs_pop_obsolet['License_Required'].fillna('',inplace=True)
tv_vs_pop_obsolet['TV_Qty'].astype(str)

st.sidebar.header("Please enter Date")
date = st.sidebar.multiselect(
        "Select the Date :",
        options=tv_vs_pop_obsolet["DATE"].unique(),
        default=tv_vs_pop_obsolet["DATE"].unique()
        
)

st.sidebar.header("Please select license required")
license = st.sidebar.multiselect(
        "Select the software :",
        options=tv_vs_pop_obsolet["License_Required"].unique(),
        default=tv_vs_pop_obsolet["License_Required"].unique()
        
)


df_selection = tv_vs_pop_obsolet.query(
    "DATE == @date & License_Required == @license  "
)


SWCNT =  7 & 5 | 3

NCOLS = 2 

if SWCNT % NCOLS > 0:
    NROWS = SWCNT//NCOLS + 1
else:
    NROWS = SWCNT//NCOLS

HEIGHT = SWCNT*2
WIDTH = 15

# get the date of the latest 5 TV reports ordered ascending
newest_5_weeks = df_selection.sort_values('DATE')['DATE'].unique()[-5:]
newest_date = newest_5_weeks.max()

top_sw_by_qty1 = df_selection[df_selection['DATE'] == newest_date].sort_values(
    'TV_Qty',ascending=False).head(SWCNT)['Software_Tag']
top_sw_by_qty1 = list(top_sw_by_qty1.str.replace('(','\(').str.replace(')','\)').str.replace('+','\+'))


fig2, axes = plt.subplots(nrows=NROWS, ncols=NCOLS, figsize=(WIDTH,HEIGHT), tight_layout=True)
fig2.suptitle(f'TOP {SWCNT} SOFTWARE\nBY TEAMVIEWER INVENTORY COUNT (OBSOLETE) And UNAUTHORIZED SOFTWARE', y=1, fontsize=20)
plt.subplots_adjust(wspace=0.05,  # horizontal padding
                    hspace=0.3)   # vertical padding

cntr = 0
for x in range(NROWS):
    for y in range(NCOLS):
        if cntr == SWCNT:
            axes[x,y].axis('off')
            break
        product = top_sw_by_qty1[cntr].upper()
#         filter = tv_vs_pop_hist_rec['TV SOFTWARE NAME'].str.contains( product,flags=re.IGNORECASE)
        newest_5_filter = df_selection.apply(lambda row: 
                                True if (row['DATE'] >= newest_5_weeks.min()) and\
                                        (re.search(product,row['Software_Tag'],flags=re.IGNORECASE))\
                                                     else False, axis=1)
        plot_data1 = df_selection[newest_5_filter].set_index('DATE')
        plot_data1.plot(kind='barh',ax=axes[x,y], align='center', width=.7,color=['mediumaquamarine','steelblue','sandybrown'])
        product = re.sub(r'\\','',product)
        axes[x,y].legend(loc='upper right')
        axes[x,y].set_title(product.upper(),fontdict={'fontsize':14})
        axes[x,1].set(yticklabels=[])
        axes[x,y].set_ylabel('TEAMVIEWER INVENTORY DATE',fontdict={'fontsize':12})
        axes[x,1].set_ylabel('')
        cntr += 1

filt1 = df_selection['Software_Tag']!=''
hist_dates1 = df_selection['DATE'].unique()
hist_dates1 = hist_dates1[-5:]  # build table with 5 weeks worth of data
sw_names1 = df_selection.loc[filt1,'Software_Tag'].unique()
summary_df1 = pd.DataFrame({'Software_Tag':sw_names1})

for d in hist_dates1 :

    col_date = d[4:6] + '-' + d[6:]
    columns = ['Software_Tag',f'TV Qty {col_date}']
    
    filt1 = df_selection.apply(lambda row: True if (row['DATE'] == d) and 
                                      (row['Software_Tag'] != '') else False,axis=1)
    temp_df = df_selection.loc[filt1,['Software_Tag','TV_Qty']]
    temp_df.columns = columns

    
    
    summary_df1 = summary_df1.merge(temp_df, on='Software_Tag', how='outer')

summary_df1.reset_index(drop=True,inplace=True)
columns = summary_df1.columns
sort_col = list(columns[-1:])

summ_df1 = summary_df1.sort_values(sort_col,ascending=False).reset_index(drop=True).astype(str)




st.title(":bar_chart: BTS INVENTORY COUNT LICENSE AND NO LICENSE")
st.dataframe(summ_df)
st.pyplot(fig)
st.title(":bar_chart: BTS INVENTORY COUNT (OBSOLETE) AND OTHERS")
st.dataframe(summ_df1)
st.download_button(label='Donwload CSV',data=summ_df1.to_csv(),file_name=f'Inventory {license} {now}.csv')
st.pyplot(fig2)







hide_st_style = """
                <style>
                #MainMenu {visibility : hidden}
                footer {visibility : hidden}
                header{visibilty : hidden}

                </style>



                """
st.markdown(hide_st_style, unsafe_allow_html=True)