from django.shortcuts import render
from .models import Products, Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.
from django.http import HttpResponse

def index(request):
    #  product= Products.objects.all()
    All_prod=[]
    catprods= Products.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Products.objects.filter(category=cat)
        n = len(prod)
        n_slides = n // 4 + ceil((n / 4) - (n // 4))
        All_prod.append([prod, range(1, n_slides), n_slides])
    danish ={'All_prod':All_prod } 
    return render(request, 'shop/index.html', danish)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank=False
    if request.method=="POST":
        name = request.POST.get('name', ' ')
        email = request.POST.get('email', ' ')
        phone = request.POST.get('phone', ' ')
        desc = request.POST.get('desc', ' ')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
        
        

    return render(request,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request,'shop/search.html')

def product(request,myid):
    product = Products.objects.filter(id=myid)
    return render(request,'shop/prodview.html',{'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsjson', '')
        name = request.POST.get('name', ' ')
        email = request.POST.get('email', ' ')
        phone = request.POST.get('phone', ' ')
        address = request.POST.get('address', ' ')
        address2 = request.POST.get('address2', ' ')
        city = request.POST.get('city', ' ')
        state = request.POST.get('state', ' ')
        zip_code = request.POST.get('zip_code', ' ')
        order = Orders(items_json=items_json, name=name, email=email, phone=phone, address=address, address2=address2, city=city, state=state, zip_code=zip_code)
        order.save()
        update= OrderUpdate(order_id= order.order_id, update_desc="The order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
        
    return render(request,'shop/checkout.html')