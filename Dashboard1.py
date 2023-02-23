import sqlite3
import seaborn as sns
import time
import numpy as np
import altair as alt
import streamlit as st
import pandas as pd
import sqlite3 as sql
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

#------------------------------------------------------------ Sidebar ------------------------------------------------------------


st.sidebar.title("Dashboards")
page = st.sidebar.selectbox("Wähle ein Dashboard:", ["Benzindatensatz", "Amazonreviews", "Twitterposts"])

#------------------------------------------------------------ Tankstellen ------------------------------------------------------------

# Create the main content
if page == "Benzindatensatz":
    st.title("Benzindatensatz")
    tankPreise = sql.connect("data/benzin.sqlite")

    # Query the data
    data = pd.read_sql_query("SELECT * FROM benzin", tankPreise)
    # Disconnect from the database
    tankPreise.close()
    # Display the DataFrame in the app


    current_data = st.selectbox("Nach Spritart filtern:", ["Alle", "Diesel", "Super95"])

    st.text("Datensatz der Tankstellen")
    st.dataframe(data)

    data["datum"] = pd.to_datetime(data["datum"], format="%d.%m.%Y")
    data["Diesel"] = data["Diesel"].astype(float)
    data["Super95"] = data["Super95"].astype(float)

    data = data[data.Diesel != 0]
    data = data[data.Super95 != 0]

    spritday = data[data.datum == '2022-09-29']
    spritday = spritday[spritday.Diesel != 0]
    spritday = spritday[spritday.Super95 != 0]

    if current_data == "Alle":



        sns.jointplot(data=data, x="Diesel", y="Super95", kind="scatter", hue="bundesland")
        st.pyplot()


        st.text("Entwicklung der Dieselpreise(rot) und Benzinpreise(grün)")
        zeit1 = alt.Chart(data).mark_line().encode(
            alt.X('datum:T'),
            alt.Y('average(Super95):Q', scale=alt.Scale(domain=(1.6, 2.0))),
            color=alt.value("green")

        )
        zeit = alt.Chart(data).mark_line().encode(
            alt.X('datum:T'),
            alt.Y('average(Diesel):Q', scale=alt.Scale(domain=(1.6, 2.0))),
            color=alt.value("red")
        )
        st.altair_chart(zeit1 + zeit, use_container_width=True)


    elif current_data == "Diesel":

        sns.displot(data["Diesel"], bins=20)
        st.pyplot()

        sns.violinplot(data=data, x=data["Diesel"], color="red")
        st.pyplot()

        diesel = alt.Chart(data).mark_line().encode(
            alt.X('datum:T'),
            alt.Y('average(Diesel):Q', scale=alt.Scale(domain=(1.6, 2))),
            alt.Color('bundesland:N')
        ).interactive()
        st.altair_chart(diesel, use_container_width=True)



    elif current_data == "Super95":

        sns.displot(data["Super95"], bins=20)
        st.pyplot()

        sns.violinplot(data=data, x=data["Super95"], color="red")
        st.pyplot()

        benzin = alt.Chart(data).mark_line().encode(
            alt.X('datum:T'),
            alt.Y('average(Super95):Q', scale=alt.Scale(domain=(1.6, 2))),
            alt.Color('bundesland:N')
        ).interactive()
        st.altair_chart(benzin, use_container_width=True)


#------------------------------------------------------------ Amazonreviews ------------------------------------------------------------

elif page == "Amazonreviews":
    st.title("Amazonreviews")
    # Read the CSV file into a DataFrame
    amazon = pd.read_csv("data/Badehaube.csv", sep=";")
    amazonOhneTitelUndFeatures = amazon.drop(["titel", "features"], axis=1)
    # Display the DataFrame in the app

    current_data = st.selectbox("Nach Bewertungen filtern:", ["Alle Bewertungen", "1 Stern", "2 Sterne", "3 Sterne", "4 Sterne", "5 Sterne"])

    st.text("Datensatz der Amazonreviews")

    if current_data == "Alle Bewertungen":
        st.title("Alle Bewertungen")
        st.dataframe(amazon)


        st.text("Allgemeine Veranschaulichung Bewertungen")
        Bewertungen = alt.Chart(amazon).mark_bar().encode(
            alt.X('bewertungen:N'),
            alt.Y('count(bewertungen):Q'),
        )
        st.altair_chart(Bewertungen, use_container_width=True)


        st.text("Worldcloud zu allen Reviews")
        nltk.download('stopwords')
        bewertungenWordcloud = " ".join(text for text in amazon["reviews"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)

        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            bewertungenWordcloud)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "1 Stern":
        st.title("1 Stern Bewertungen: " + str(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 1].shape[0]))
        st.dataframe(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 1])

        st.text("Worldcloud zu 1 Stern Reviews")
        nltk.download('stopwords')
        bewertungenWordcloud = " ".join(text for text in amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 1]["reviews"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)

        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            bewertungenWordcloud)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "2 Sterne":
        st.title("2 Sterne Bewertungen: " + str(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 2].shape[0]))
        st.dataframe(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 2])

        st.text("Worldcloud zu 2 Stern Reviews")
        nltk.download('stopwords')
        bewertungenWordcloud = " ".join(text for text in amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 2]["reviews"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)

        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            bewertungenWordcloud)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "3 Sterne":
        st.title("3 Sterne Bewertungen: " + str(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 3].shape[0]))
        st.dataframe(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 3])

        st.text("Worldcloud zu 3 Stern Reviews")
        nltk.download('stopwords')
        bewertungenWordcloud = " ".join(text for text in amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 3]["reviews"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)

        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            bewertungenWordcloud)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "4 Sterne":
        st.title("4 Sterne Bewertungen: " + str(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 4].shape[0]))
        st.dataframe(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 4])

        st.text("Worldcloud zu 4 Stern Reviews")
        nltk.download('stopwords')
        bewertungenWordcloud = " ".join(text for text in amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 4]["reviews"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)

        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            bewertungenWordcloud)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "5 Sterne":
        st.title("5 Sterne Bewertungen: " + str(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 5].shape[0]))
        st.dataframe(amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 5])

        st.text("Worldcloud zu 5 Stern Reviews")
        nltk.download('stopwords')
        bewertungenWordcloud = " ".join(text for text in amazonOhneTitelUndFeatures[amazonOhneTitelUndFeatures.bewertungen == 5]["reviews"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)

        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            bewertungenWordcloud)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()


#------------------------------------------------------------ Twitter -----------------------------------------------------------------

else:
    st.title("Twitterposts")

    # Read the CSV file into a DataFrame
    twitter = pd.read_csv("data/tweets2.csv")
    twitter.drop(columns=["Unnamed: 0"], inplace=True)
    twitter.drop(columns=["index"], inplace=True)
    twitter = twitter[twitter['text'] != "https"]


    current_data = st.selectbox("Nach Partei filtern:", ["Alle", "FPÖ", "Grüne", "NEOS", "ÖVP", "SPÖ"])

    if current_data == "Alle":
        st.title("Alle Tweets: " + str(twitter.shape[0]))
        st.dataframe(twitter)

        st.text("Verteilung der Stimmung")
        sns.stripplot(data=twitter, x="partei", y="score", hue="Stimmung")
        st.pyplot()

        st.text("Stimmung der Tweets für alle Parteien")
        twitter = alt.Chart(twitter).mark_bar().encode(
            x='Stimmung:N',
            y='count(Stimmung):Q',
            column="partei:N",
            color="partei:N"
        )
        st.altair_chart(twitter)

    elif current_data == "FPÖ":
        st.title("FPÖ Tweets: " + str(twitter[twitter.partei == "FPÖ"].shape[0]))
        twitterFPOE = twitter[twitter.partei == "FPÖ"]
        st.dataframe(twitterFPOE)

        sns.stripplot(data=twitter[twitter.partei == "FPÖ"], x="partei", y="score", hue="Stimmung")
        st.pyplot()

        st.text("Verteilung der Stimmung der jeweiligen Partei")
        twitter = alt.Chart(twitterFPOE).mark_bar().encode(
            x='count(Stimmung):Q',
            y='Stimmung:N',
            color="Stimmung:N"
        )
        st.altair_chart(twitter)

        st.text("Worldcloud zu FPÖ Tweets")
        nltk.download('stopwords')
        parteienWordcloud = " " .join(text for text in twitterFPOE["text"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp", "Grüne", "Gruene", "Grünen", "FPOE", "FPÖ", "SPÖ", "SPOE", "OEVP", "ÖVP", "NEOS", "ja", "un", "d", "le", "v"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)
        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            parteienWordcloud)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "Grüne":
        st.title("Grüne Tweets: " + str(twitter[twitter.partei == "Grüne"].shape[0]))
        twitterGrüne = twitter[twitter.partei == "Grüne"]
        st.dataframe(twitterGrüne)

        sns.stripplot(data=twitter[twitter.partei == "Grüne"], x="partei", y="score", hue="Stimmung")
        st.pyplot()

        st.text("Verteilung der Stimmung der jeweiligen Partei")
        twitter = alt.Chart(twitterGrüne).mark_bar().encode(
            x='count(Stimmung):Q',
            y='Stimmung:N',
            color="Stimmung:N"
        )
        st.altair_chart(twitter)

        st.text("Worldcloud zu Grünen Tweets")
        nltk.download('stopwords')
        parteienWordcloud = " " .join(text for text in twitterGrüne["text"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp", "Grüne", "Gruene", "Grünen", "FPOE", "FPÖ", "SPÖ", "SPOE", "OEVP", "ÖVP", "NEOS", "un", "d", "le", "v", "gt", "n"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)


        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            parteienWordcloud)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "NEOS":
        st.title("NEOS Tweets: " + str(twitter[twitter.partei == "NEOS"].shape[0]))
        twitterNEOS = twitter[twitter.partei == "NEOS"]
        st.dataframe(twitterNEOS)

        sns.stripplot(data=twitter[twitter.partei == "NEOS"], x="partei", y="score", hue="Stimmung")
        st.pyplot()

        st.text("Verteilung der Stimmung der jeweiligen Partei")
        twitter = alt.Chart(twitterNEOS).mark_bar().encode(
            x='count(Stimmung):Q',
            y='Stimmung:N',
            color="Stimmung:N"
        )
        st.altair_chart(twitter)

        st.text("Worldcloud zu NEOS Tweets")
        nltk.download('stopwords')
        parteienWordcloud = " " .join(text for text in twitterNEOS["text"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp", "Grüne", "Gruene", "Grünen", "FPOE", "FPÖ", "SPÖ", "SPOE", "OEVP", "ÖVP", "NEOS"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)
        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            parteienWordcloud)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "ÖVP":
        st.title("ÖVP Tweets: " + str(twitter[twitter.partei == "ÖVP"].shape[0]))
        twitterOEVP = twitter[twitter.partei == "ÖVP"]
        st.dataframe(twitterOEVP)

        sns.stripplot(data=twitter[twitter.partei == "ÖVP"], x="partei", y="score", hue="Stimmung")
        st.pyplot()

        st.text("Verteilung der Stimmung der jeweiligen Partei")
        twitter = alt.Chart(twitterOEVP).mark_bar().encode(
            x='count(Stimmung):Q',
            y='Stimmung:N',
            color="Stimmung:N"
        )
        st.altair_chart(twitter)

        st.text("Worldcloud zu ÖVP Tweets")
        nltk.download('stopwords')
        parteienWordcloud = " " .join(text for text in twitterOEVP["text"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp", "Grüne", "Gruene", "Grünen", "FPOE", "FPÖ", "SPÖ", "SPOE", "OEVP", "ÖVP", "NEOS"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)
        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            parteienWordcloud)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif current_data == "SPÖ":
        st.title("SPÖ Tweets: " + str(twitter[twitter.partei == "SPÖ"].shape[0]))
        twitterSOE = twitter[twitter.partei == "SPÖ"]
        st.dataframe(twitterSOE)

        sns.stripplot(data=twitter[twitter.partei == "SPÖ"], x="partei", y="score", hue="Stimmung")
        st.pyplot()

        st.text("Verteilung der Stimmung der jeweiligen Partei")
        twitter = alt.Chart(twitterSOE).mark_bar().encode(
            x='count(Stimmung):Q',
            y='Stimmung:N',
            color="Stimmung:N"
        )
        st.altair_chart(twitter)

        st.text("Worldcloud zu SPÖ Tweets")
        nltk.download('stopwords')
        parteienWordcloud = " " .join(text for text in twitterSOE["text"])
        german_stopwords = stopwords.words('german')
        additional_stopwords = ["https", "t", "co", "a", "amp", "Grüne", "Gruene", "Grünen", "FPOE", "FPÖ", "SPÖ", "SPOE", "OEVP", "ÖVP", "NEOS", "N"]
        german_stopwords.extend(additional_stopwords)
        german_stopwords = set(german_stopwords)
        wordcloud = WordCloud(stopwords=german_stopwords, background_color="white", width=2400, height=1600).generate(
            parteienWordcloud)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()






