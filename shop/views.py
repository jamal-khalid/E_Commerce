from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from paytmchecksum import PaytmChecksum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login, logout



Merchant_key="YOUR-MERCHANT-KEY"

def index(request):
    allProd=[]
    catProds=Product.objects.values('categary','id')
    cats={item['categary'] for item in catProds}
    for cat in cats:
        prod=Product.objects.filter(categary=cat)
        n=len(prod)
        nSlides=(n//4)+ ceil((n/4)-(n//4))
        allProd.append([prod , range(1,nSlides),nSlides])
    params={'allProd':allProd}
    return render (request , 'shop/index.html',params)

def searchMatch(query , item):
    # return true if query matches the items 
    if query in item.description.lower() or query in item.product_name.lower() or query in item.categary.lower():
        return True
    elif query in item.description or query in item.product_name or query in item.categary:
        return True
    elif query in item.product_name:
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search','')
    allProd=[]
    catProds=Product.objects.values('categary','id')
    cats={item['categary'] for item in catProds}
    for cat in cats:
        Myprod=Product.objects.filter(categary=cat)
        prod=[item for item in Myprod if searchMatch(query,item)]
        n=len(prod)
        nSlides=(n//4)+ ceil((n/4)-(n//4))
        if len(prod)!=0:
            allProd.append([prod , range(1,nSlides),nSlides])
    params={'allProd':allProd,'msg':''}
    if len(allProd)==0 or len(query)>4:
        params={'msg':'please fill the valid sentenes.  You have typed something wrong '}
    return render(request , 'shop/index.html',params)


def about(request):
    return render (request , 'shop/about.html')

def contact(request):
    thank=False
    if request.method=='POST':
        name=request.POST.get('name', 'default')
        email=request.POST.get('email' ,'default')
        phone=request.POST.get('phone','default')
        desc=request.POST.get('desc','default')
        contact=Contact(name=name , email=email , phone=phone,desc=desc)
        contact.save()
        thank=True
    return render(request , 'shop/contact.html',{'thank':thank})

def productView(request ,myid):
    product=Product.objects.filter(id=myid)
    return render(request , 'shop/product.html' , {'product':product[0]})

def tracker(request):
    if request.method=='POST':
        orderId=request.POST.get('orderId','')
        email=request.POST.get('email','')
        print(email)
        try:
            order=Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                print('inside')
                update = OrderUpdate.objects.filter(order_id=orderId)
                print(update,'data')
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.time_stamp})
                response=json.dumps({'status':'succes','updates':updates,'itemsjson': order[0].items_json} ,default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noItem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

        

    return render(request , 'shop/tracker.html')

def checkout(request):
    if request.method=='POST':
        items_json=request.POST.get('itemsjson','')
        amount=request.POST.get('amount','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone',default="")
        adress=request.POST.get('adress1','')+" "+request.POST.get('adress2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        pin_code=request.POST.get('pincode','')


        order=Orders(items_json=items_json , name=name , email=email , phone=phone,adress=adress,city=city,state=state,pin_code=pin_code,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="Your Order Has Been Placed ")
        update.save()
        thank=True
        id=order.order_id
        params={'thank':thank , 'id':id}
        # return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    #     param_dict = {
    #     "MID": "YOUR-MERCHANT-ID",
    #     "ORDER_ID": str(order.order_id),
    #     "CUST_ID": email,
    #     "TXN_AMOUNT": str(amount),
    #     "CHANNEL_ID": "WEB",
    #     "INDUSTRY_TYPE_ID": "Retail",
    #     "WEBSITE": "WEBSTAGING",
    #     "CALLBACK_URL": 'http://127.0.0.1:8000/shop/handlepayment/'
    # }
        
        # param_dict['CHECKSUMHASH'] = PaytmChecksum.generateSignature(param_dict, Merchant_key)
        # return render(request , 'shop/paytm.html',{'param_dict':param_dict})
        return render (request,'shop/checkout.html' ,params)
    return render(request , 'shop/checkout.html')


def cartpage(request):
    return render(request , 'shop/cart.html')

# @csrf_exempt
# def handlepayment(request):
#     form=request.POST
#     response_dict={}
#     for i in form.keys():
#         response_dict[i]=form[i]
#         if i=='CHECKSUMHASH':
#             checksum=form[i]
#     verify=Checksum.verify_checksum(response_dict,Merchant_key , checksum)
#     if verify:
#         if response_dict['RESPONSE']=='01':
#             print('order successfull')
#         else:
#             print('order not successfull because '+response_dict['REPMSG'])
#     return render(request , 'shop/paymentstatus.html',{'response':response_dict})

def handleSignup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1!=pass2:
            messages.error(request ,"Your password Is Wrong Fill again")
            return redirect('index')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request ,"You Profile Has been Succesfully Created In Jamal_services. Please LogIn")

        return redirect('index')

    else:
        return HttpResponse('error 404')
    
def handleLogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginusername , password=loginpassword)
        if user is not None:
            login(request ,user)
            messages.success(request , "Welcome You Have Successfully Logged In Jamal_Services")
            return redirect('index')
        
        else:
            messages.error(request ,"Invalid Credentials . Please Try Again..")
            return redirect('index')
        
    else:
        return HttpResponse('404 Record Not found')

def LogOut(request):
    logout(request)
    messages.success(request ,"You Have Logged Out Succesfully ")
    return redirect('index')

