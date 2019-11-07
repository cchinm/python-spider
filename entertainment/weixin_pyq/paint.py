from wordcloud import WordCloud

def paint(data):
    wc = WordCloud(font_path="simhei.ttf", background_color='White', max_words=50)
    wc.generate_from_frequencies(data)
    wc.to_file("wc.jpg")


