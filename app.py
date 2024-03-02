import streamlit as st
import pandas as pd
import cardsort as cs
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title="Card Sorting Analysis")

st.header('Analyse your card sorting data', divider='rainbow')
st.write("*This app provides a UI for the main functions of the [cardsort](https://cardsort.readthedocs.io/en/latest/) Python package. Feel free to contribute to improving this app by leaving feedback or contributing code on GitHub ([app](https://github.com/katoss/cardsort-analysis-ui) | [Python package](https://github.com/katoss/cardsort))* :sparkles:")

st.write("Card sorting is a user research method that can help you create user-friendly information architectures for websites. See [here](https://www.nngroup.com/articles/card-sorting-definition/) for an introduction to card sorting.")

st.header('Upload your dataset')
file = st.file_uploader(label = "**Accepted input:** .csv files in 'Casolysis Data' format. As generated, for example, by [kardSort](https://kardsort.com/).", help="Columns: 'card_id', 'card_label', 'category_id', 'category_label', 'user_id'")

if file:
    df = pd.read_csv(file)
    st.write('Data preview (first 5 lines)')
    st.write(df.head())
    st.header('Visualize your data')
    st.write("Visualize your data as a dendrogram using hierarchical cluster analysis. For an introduction to this method, see [here](https://www.nngroup.com/videos/ia-dendrogram/).")
    st.subheader('Parameters')
    linkage_option = st.radio(
        "Which linkage method would you like to use to calculate distance?",
        ["average", "complete", "single"],
        index = 0,
        help = "For an introduction to the different linkage methods, [see here](https://medium.com/@iqra.bismi/different-linkage-methods-used-in-hierarchical-clustering-627bde3787e8)."
    )
    count_option = st.radio(
        "Would you like to display distance labels as fraction or absolute value (= number of participants)?",
        ["absolute", "fraction"],
        index = 0,
        help="This choice impacts the labels on the x-axis of the dendrogram."
    )
    if count_option == "fraction":
        min = 0.00
        max = 1.01
        value = 0.75
        step = 0.05
    else:
        min = 0
        max = df['user_id'].max()
        value = round(2/3*max)
        step = 1
    threshold_option = st.number_input(
        "Please set the color threshold (absolute value or fraction depending on your choice above). Default = 2/3 distance.",
        min_value = min, 
        max_value = max,
        value = value,
        step = step,
        help="The threshold is the distance limit to which you want to consider (and thus color) clusters. You can determine this limit yourself, based on which clusters make sense to you. The closer to the left the branches merge, the more people grouped the respective cards together."
    )
    if st.button("Create dendrogram", type="primary"):
        dm = cs.get_distance_matrix(df)
        fig = cs.create_dendrogram(df,dm, count=count_option, linkage=linkage_option, color_threshold=threshold_option)
        st.pyplot(fig)

    st.header('Analyze user-generated cluster labels')
    card_selection = st.multiselect(
        'Select one or more cards to see which category labels participants chose for them. If the output is empty, no participant grouped this exact selection of cards together.',
        sorted(df['card_label'].unique())
    )
    if st.button("Extract labels", type="primary"):
        list = card_selection
        st.write(cs.get_cluster_labels(df,list))
        st.write("**What do the columns mean?** *user_id:* ID of each participant who grouped your card selection together; *cluster_label:* The label this participant gave to the cluster that contains the cards you selected; *cards:* All cards that the user grouped together under this label.")
