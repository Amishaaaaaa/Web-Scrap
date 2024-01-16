from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
#import logging
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    url_home = "https://www.flickchart.com/Charts.aspx?perpage=250"
    rr = requests.get(url_home)
    soupp = bs(rr.content,'html.parser')
    form = soupp.find("form", {"id": "aspnetForm"})
    movie_titles=[]
    movie_codes=[]

    if form:
        div1 = form.find("div" , {"id":"containerBg"})
        div2 = div1.find("div")
        div3 = div2.find("div", {"id": "main-content-container"})
        div4 = div3.find("div")
        div5 = div4.find("div",{"id":"chart"})
        div6 = div5.find("div" , {"itemtype":"http://schema.org/ItemList"})
        Movielist = []

        for entry in div6.find_all("div", {"class":"chartEntry"}):
            movie_title = entry.find("h2", {"class":"movieTitle"}).a.find("span", itemprop="name").text
            movie_link = (entry.find("h2", {"class":"movieTitle"}).a['href'])[7:]
            movie_titles.append(movie_title)
            movie_codes.append(movie_link)
        movie={"Movie_name" : movie_titles, "Movie_code": movie_codes}
        Movielist.append(movie)
    return render_template("index.html", Movielist = Movielist[0])

@app.route("/review", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            url = "https://www.flickchart.com/movie/" + str(searchString)
            r = requests.get(url)
            soup = bs(r.content, 'html.parser')
            form_table = soup.find("form", {"id" : "aspnetForm"})
            inner8 = None
            reviews = []

            if form_table:
                form_firstDiv = form_table.find("div", {"id" : "containerBg"})
                if form_firstDiv:
                    inner1 = form_firstDiv.find("div")
                    if inner1:
                        inner2 = inner1.find("div")
                        if inner2:
                            inner3 = inner2.find("div", { "id" : "main-content-container"})
                            if inner3:
                                inner4 = inner3.find("div")
                                if inner4:
                                    inner5 = inner4.find("div", { "id" : "mcenterColumn"})
                                    if inner5:
                                        inner6 = inner5.find("div", {"id": "FC-comments"})
                                        if inner6:
                                            inner7 = inner6.find("div", {"id": "commentList"})
                                            if inner7:
                                                inner8 = inner7.findAll("div" , {"class" : "thread"}) #inner8 is a list of all "thread" class   

                    else:
                        print("thoda dhyan se dekh")
                else:
                    print("no such id")
            
            
            if inner8:
                totalUsers = 0
                username = []
                date = []
                review = []

                for i in inner8:
                    totalUsers += 1
                    userName = i.div.div.p.find_all("a" , {"class" : "name"})[0].text
                    username.append(userName)
                    comment = i.div.find_all('p', {"class" : "commentText"})[0].text.replace('\r\n\t\t\t\t\t\t\t', '')
                    review.append(comment)
                    timestamp = (i.div.div.p.find_all("span" , {"class" : "timestamp"})[0].text)[3:]
                    date.append(timestamp)
                    
                movie_review = {"Username" : username, "DateofReview" : date, "Review" : review}
                reviews.append(movie_review)
                if review:
                    return render_template('result.html', reviews = reviews[0])
                else:
                    print("empty me aaya hu")    
                    return render_template('empty.html')
                
            else:
                print("inner8 is not defined")
                return render_template('empty.html')
            
        except Exception as e:
            #logging.info(e)
            return 'something is wrong'
        
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)
