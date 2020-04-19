from django.shortcuts import render, get_object_or_404

from .models import Issue, Question, Customer,Solve
from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup
from urllib.request import urlopen

from collections import defaultdict
import re
# Create your views here.
def home_page(request):
    return render(request, "home.html")

# issue 나열 페이지
def issue_page(request):
    issue = Issue.objects.order_by('pk')

    sesson_2_url = "https://github.com/leewoongi/Algorithm/issues/"

    issue_crwaling(sesson_2_url)

    return render(request, 'issue.html', {'issue':issue})

# issue 크롤링 함수
def issue_crwaling(sesson_url):
    url = sesson_url
    html = urlopen(url)
    source = html.read()
    html.close()

    soup = BeautifulSoup(source, "html.parser")
    r = re.compile('issue_[0-9]+_link')
    issue = (soup.find_all('a', {'id' : r}))

    for t in issue:
        tmp = str(t.get_text())
        obj, created = Issue.objects.get_or_create(issue = tmp, defaults = {'issue' : tmp})


#해당 issue 페이지
def detail_page(request, issue_id):
    issue = get_object_or_404(Issue,pk=issue_id)
    
    sesson_2_url = "https://github.com/leewoongi/Algorithm/issues/"
    
    detail_crwaling(issue, sesson_2_url)
   
    questions = issue.question_set.all()
    customers = issue.customer_set.all()

    return render(request,'detail.html', {'issue' : issue , 'questions' : questions,'customers':customers })


#해당 issue 에 대한 문제 크롤링 함수
def detail_crwaling(issue,sesson_url):
    print(sesson_url)
    tmp_issue = str(issue)
    issue_split = tmp_issue.split(' ')

    issue_num = issue_split[2:]
    issue_num = (",".join(issue_num))[1:]

    url = sesson_url + str(issue_num)
    html = urlopen(url)
    source = html.read() 
    html.close()

    soup = BeautifulSoup(source, 'html.parser')

    questions = soup.find_all('td' , {'class' : "d-block comment-body markdown-body js-comment-body"})
    questions = questions[0]
    questions = questions.get_text().split("\n")

    #print(questions)
    #이슈에 대한 문제 목록
    question_set = issue.question_set
    
    index= 1
    for q  in questions:
        #print(index)
        obj, create = question_set.get_or_create(question = questions[index] , question_link = questions[index +1],
                                                    defaults = {'question' : questions[index], 'question_link' : questions[index+1]})
        index+=2
        if index >= len(questions) - 1:
            break

    #이제 문제를 푼 사람들 크롤링
    #users =soup.find_all('div' ,{'class':"TimelineItem-body", 'id':"ref-commit"})
    users = soup.select('div[class="AvatarStack-body"]')
    users_list=[]
    for i in users :
        users_list.append(i['aria-label'])

    solves = soup.find_all('div', {'class' : "commit-message" })

    #문제 푼사람 {'이름' : set(문제 이름)} 으로 생성
    users_dict = defaultdict(set)

    for index in range(0,len(users)):
        users_dict[users_list[index]].add(solves[index].get_text())

    #이슈에 대한 문제 푼 사람들 customer_set 생성
    customers = issue.customer_set
    
    for user in users_dict:
        #이름 없으면 생성 O 있으면 생성 X
        obj, create = customers.get_or_create(name = user, defaults ={'name' : user})

        customer = get_object_or_404(Customer, pk = obj.id)

        #이름에 대한 문제 제목 solve_set 생성
        solve = customer.solve_set
        for solves in users_dict[obj.name]:
            solve.get_or_create(problem_solve = solves , defaults = {'problem_solve' : solves})
        

def back_page(request):
    issue = Issue.objects
    problems = issue.question_set.all()
    return render(request, 'back.html', {'issue': issue, 'problems':problems})
