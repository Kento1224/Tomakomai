from django.shortcuts import render, redirect
from django.utils import timezone
import pytz
import datetime
from .models import Money
from .forms import SpendingForm

import matplotlib.pyplot as plt
import calendar

from .utils import index_utils

from django.views import View

import os

import folium
import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
#from ..mysite.settings import GEOIP_PATH
# Create your views here.

plt.rcParams['font.family'] = 'MS PGothic'    #日本語の文字化け防止

TODAY = str(timezone.now()).split('-')

class MainView(View):

    def get(self,request, year=TODAY[0], month=TODAY[1]):
        money = Money.objects.filter(use_date__year=year,
                use_date__month=month).order_by('use_date')
        total = index_utils.calc_month_pay(money)
        index_utils.format_date(money)    # <- その月の支出の合計をついでに計算

        next_year, next_month = index_utils.get_next(year, month)
        prev_year, prev_month = index_utils.get_prev(year, month)

        m = visualize_locations()
        m2 = visualize_locations2(year,month)

        form = SpendingForm()
        context = {'year' : year, 
                'month' : month,
                'prev_year' : prev_year,
                'prev_month' : prev_month,
                'next_year' : next_year,
                'next_month' : next_month,
                'money' : money,
                'total' : total,
                'form' : form,
                'map':m,
                'map2':m2
                }

        draw_graph(year, month) 
        draw_circle(year,month)

        return render(request, 'money/index.html', context)

    def post(self, request, year=TODAY[0], month=TODAY[1]):
        data = request.POST
        use_date = data['use_date']
        cost = data['cost']
        detail = data['detail']
        category = data['category']
        location = data['location']

        use_date = timezone.datetime.strptime(use_date, "%Y/%m/%d")

        tokyo_timezone = pytz.timezone('Asia/Tokyo')
        use_date = tokyo_timezone.localize(use_date)
        use_date += datetime.timedelta(hours=9)
        Money.objects.create(
                use_date = use_date,
                detail = detail,
                cost = int(cost),
                category = category,
                location = location,
                )
        return redirect(to='/money/{}/{}'.format(year, month))

def draw_graph(year, month):    #追加
    money = Money.objects.filter(use_date__year=year,
            use_date__month=month).order_by('use_date')
    last_day = calendar.monthrange(int(year), int(month))[1] + 1
    day = [i for i in range(1, last_day)]
    cost = [0 for i in range(len(day))]
    for m in money:
        cost[int(str(m.use_date).split('-')[2])-1] += int(m.cost)
    plt.figure(figsize=(5,5),dpi=50)
    plt.bar(day, cost, color='#00bfff', edgecolor='#0000ff')
    plt.grid(True)
    plt.xlim([0, 31])
    plt.xlabel('日付', fontsize=16,fontname="MS Gothic")
    plt.ylabel('支出額(円)', fontsize=16,fontname="MS Gothic")

    #staticフォルダの中にimagesというフォルダを用意しておきその中に入るようにしておく
    barpath=os.path.join(BASE_DIR,'money/static/images/bar_{}_{}.svg'.format(year, month))
    plt.savefig(barpath,
            transparent=True)
    return None

def draw_circle(year, month):    #追加
    money = Money.objects.filter(use_date__year=year,
            use_date__month=month).order_by('use_date')
    #last_day = calendar.monthrange(int(year), int(month))[1] + 1
    #day = [i for i in range(1, last_day)]
    #cost = [0 for i in range(len(day))]
    dic_category={}
    for m in money:
        #cost[int(str(m.use_date).split('-')[2])-1] += int(m.cost)
        if m.category in dic_category:
            dic_category[m.category] += int(m.cost)
        else:
            dic_category[m.category] = int(m.cost)

    plt.rcParams['font.family'] = 'MS Gothic'    
    plt.figure(figsize=(5,5),dpi=50)
    plt.pie(dic_category.values(), labels=dic_category.keys())
    #plt.grid(True)
    #plt.xlim([0, 31])
    #plt.xlabel('日付', fontsize=16,fontname="MS Gothic")
    #plt.ylabel('支出額(円)', fontsize=16,fontname="MS Gothic")

    #staticフォルダの中にimagesというフォルダを用意しておきその中に入るようにしておく
    circlepath=os.path.join(BASE_DIR,'money/static/images/circle_{}_{}.svg'.format(year, month))
    plt.savefig(circlepath,
            transparent=True)
    return None 

def visualize_locations(zoom=11):
    """日本を拡大した地図に、pandasデータフレームのlatitudeおよびlongitudeカラムをプロットする。
    """
    filepath=os.path.join(BASE_DIR,'money/geoip/Tomakomaiv20401.csv')
    df=pd.read_csv(filepath)    	
    # 図の大きさを指定する。
    f = folium.Figure(width=1000, height=500)

    # 初期表示の中心の座標を指定して地図を作成する。
    center_lat=42.63408
    center_lon=141.606
    m = folium.Map([center_lat,center_lon], zoom_start=zoom).add_to(f)
        
    # データフレームの全ての行のマーカーを作成する。
    for i in range(0,len(df)):
        folium.Circle(location=[df["緯度"][i],df["経度"][i]],
                      #radius = 0,
                      radius = int(df["合計"][i].replace(',',''))*0.17,
                      #popup=df["町名"][i],
                      color  ="blue",
                      #opacity=0.2,
                      weight=0.3,
                      fill=True,
                      popup="""
                      <i>町名: </i><b>{}　　　　　　</b>
                      <i>人口: </i><b>{}　　　</b>
                      <i>男性: </i><b>{}　　　</b>
                      <i>女性: </i><b>{}　　　</b>
                      <i>世帯: </i><b>{}　　　</b>""".format(df["町名"][i],df["合計"][i],df["男"][i],df["女"][i],df["世帯"][i])
                      ).add_to(m)
    m = m._repr_html_()
    return m

def visualize_locations2(year,month):
    money = Money.objects.filter(use_date__year=year,
            use_date__month=month).order_by('use_date')
    dic_location={}
    for m in money:
        #cost[int(str(m.use_date).split('-')[2])-1] += int(m.cost)
        if m.category in dic_location:
            dic_location[m.location] += int(m.cost)
        else:
            dic_location[m.location] = int(m.cost)        

    filepath=os.path.join(BASE_DIR,'money/geoip/Tomakomaiv20401.csv')
    df=pd.read_csv(filepath)  
    #df=pd.read_csv('money/geoip/Tomakomaiv20401.csv')    	
    
    f = folium.Figure(width=1000, height=500)

    # 初期表示の中心の座標を指定して地図を作成する。
    center_lat=42.63408
    center_lon=141.606
    m = folium.Map([center_lat,center_lon], zoom_start=11).add_to(f)

    for k,v in dic_location.items():
        folium.Circle(location=[float(df.loc[df['町名']==k,'緯度'].values),float(df.loc[df['町名']==k,'経度'].values)],
                      radius = v*0.5,
                      #radius = int(df.loc[df['町名']==k,'合計'].values.replace(',',''))/6,
                      #popup=df["町名"][i],
                      color  ="red",
                      #opacity=0.2,
                      weight=0.3,
                      fill=True,
                      popup="""
                      <i>町名: </i><b>{}　　　　　　　</b>
                      <i>人口: </i><b>{}　　　</b>
                      <i>取引金額: </i><b>{}　円</b>
                      """.format(k,int(df.loc[df['町名']==k,'合計'].values.tolist()[0].replace(',','')),v)
                      ).add_to(m)
    m = m._repr_html_()
    return m

    #text_day = ",".join(list(map(str, day)))
    #text_cost = ",".join(list(map(str, cost)))
    #json_template = (
    #    """var json = {
    #    type: 'bar',
    #    data: {
    #       labels: [
    #"""
    #    + str(text_day)
    #    + """
    #        ],
    #        datasets: [{
    #            label: '支出',
    #            data: [
    #"""
    #    + str(text_cost)
    #    + """
    #            ],
    #            borderWidth: 2,
    #            strokeColor: 'rgba(0,0,255,1)',
    #            backgroundColor: 'rgba(0,191,255,0.5)'
    #        }]
    #    },
    #    options: {
    #        scales: {
    #            xAxes: [{
    #                ticks: {
    #                    beginAtZero:true
    #                },
    #                scaleLabel: {
    #                    display: true,
    #                    labelString: '日付',
    #                    fontsize: 18
    #                }
    #            }],
    #           yAxes: [{
    #                ticks: {
    #                    beginAtZero:true
    #                },
    #                scaleLabel: {
    #                    display: true,
    #                    labelString: '支出額 (円)',
    #                    fontsize: 18
    #                }
    #            }]
    #        },
    #        responsive: true
    #    }
    #}
    #"""
    #)
    #with open(
    #    os.path.dirname(os.path.abspath(__file__)) + "/static/money/js/data.js",
    #    "w",
    #) as f:
    #    f.write(json_template)



