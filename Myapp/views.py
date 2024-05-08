import base64
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from Myapp.models import *


def login(request):
    return render(request,'adminlogin.html')

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    res=Login.objects.filter(username=username,password=password)
    if res.exists():
        res1 = Login.objects.get(username=username, password=password)
        request.session['lid']=res1.id
        if res1.type=="admin":
            return HttpResponse('''<script>alert('Login Successfull');window.location="/myapp/admin_home/"</script>''')
        elif res1.type=="shop":
            s=Shop.objects.get(LOGIN_id=request.session['lid'])
            request.session['sphoto']=s.photo
            request.session['sname']=s.shop_name
            return HttpResponse('''<script>alert('Login Successfull');window.location="/myapp/shop_home/"</script>''')
        elif res1.type=="staff":
            return HttpResponse('''<script>alert('Login Successfull');window.location="/myapp/staff_home/"</script>''')
        else:
             return HttpResponse('''<script>alert('Ivalid username or password');window.location="/myapp/login/"</script>''')

    else:
        return HttpResponse('''<script>alert('Ivalid username or password');window.location="/myapp/login/"</script>''')



def admin_home(request):
    return render(request,'admin_index1.html')
def shop_home(request):
    sp=request.session['sphoto']
    sn=request.session['sname']

    return render(request,'shop_index.html',{'sp':sp,'sn':sn})
def staff_home(request):
    return render(request,'staffhome.html')
def shop_register(request):
   return render(request,'Reg.html')
def shop_register_post(request):
    name=request.POST['textfield']
    email=request.POST['textfield2']
    phone=request.POST['textfield3']
    place=request.POST['textfield4']
    owner_name=request.POST['textfield5']
    license_no=request.POST['textfield6']
    photo=request.FILES['fileField']
    post=request.POST['textfield7']
    pin=request.POST['textfield8']
    district=request.POST['textfield9']
    password=request.POST['textfield10']
    confirm_password=request.POST['textfield11']


    lobj=Login()
    lobj.username=email
    lobj.password=password
    lobj.type="shop"
    lobj.save()


    fs=FileSystemStorage()
    date=datetime.now().strftime("%Y%m%d%H%M%S")+photo.name
    fn=fs.save(date,photo)
    path=fs.url(date)

    sobj=Shop()
    sobj.LOGIN=lobj
    sobj.shop_name=name
    sobj.email=email
    sobj.shop_phone=phone
    sobj.shop_place=place
    sobj.owner_name=owner_name
    sobj.shop_license_no=license_no
    sobj.photo=path
    sobj.post=post
    sobj.pin=pin
    sobj.district=district
    sobj.status='pending'
    sobj.save()





    return HttpResponse('''<script>alert('Registeration successfull');window.location="/myapp/login/"</script>''')
def view_shop(request):
    sp=Shop.objects.filter(status="pending")
    return render(request, 'view_shop.html',{'data':sp})

def view_shop_search(request):
    search=request.POST['search']
    res=Shop.objects.filter(shop_name__icontains=search)
    return render(request, 'view_shop.html', {'data': res})


def view_shop_approve(request,id):
    res=Login.objects.filter(id=id).update(type="shop")
    res1=Shop.objects.filter(LOGIN__id=id).update(status="approved")
    return HttpResponse('''<script>alert('Approves successfull');window.location="/myapp/view_shop/"</script>''')

def view_shop_reject(request,id):
    res=Login.objects.filter(id=id).update(type="block")
    res1=Shop.objects.filter(LOGIN__id=id).update(status="rejected")
    return HttpResponse('''<script>alert('Shop verification Rejected');window.location="/myapp/view_shop/"</script>''')


def view_approved_shop(request):
    res=Shop.objects.filter(status="approved")
    return render(request,'view_approve_shop.html',{'data':res})

def view_rejected_shop(request):
    res=Shop.objects.filter(status="rejected")
    return render(request,'view_reject_shop.html',{'data':res})


def add_staff(request):
    return  render(request,'Add_staff.html')
def add_staff_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    gender = request.POST['radio']
    place = request.POST['textfield4']
    Adhar_no = request.POST['textfield5']
    district = request.POST['textfield6']
    post = request.POST['textfield7']
    pin = request.POST['textfield8']
    photo = request.FILES['fileField']
    # import random
    # new_pass=random.randint(00000000,99999999)
    password = request.POST['textfield10']
    confirm_password = request.POST['textfield11']
    type=request.POST['type']
    stobj = Login()
    stobj.username = email
    stobj.password = password
    stobj.type = type
    stobj.save()

    fs = FileSystemStorage()
    date = "staff/"+datetime.now().strftime("%Y%m%d%H%M%S") + photo.name
    fn = fs.save(date, photo)
    path = fs.url(date)

    s=Staff()
    s.SHOP=Shop.objects.get(LOGIN=request.session['lid'])
    s.LOGIN=stobj
    s.name=name
    s.email=email
    s.phone=phone
    s.gender=gender
    s.place=place
    s.aadhar_no=Adhar_no
    s.district=district
    s.post=post
    s.pin=pin
    s.photo=path
    s.type=type
    s.save()
    return HttpResponse('''<script>alert('Registeration successfull');window.location="/myapp/view_staff/"</script>''')


def view_staff(request):
    stff = Staff.objects.filter(SHOP__LOGIN_id=request.session['lid'])
    return render(request,'view_staff.html',{'data': stff})
def view_staff_search(request):
    search = request.POST['search']
    res = Staff.objects.filter(name__icontains=search)
    return render(request, 'view_staff.html', {'data': res})
def shop_index(request):
    return render(request, 'shop_index.html')
def edit_staff(request,id):
    stff = Staff.objects.get(id=id)
    return render(request,'Edit_staff.html',{'data':stff})
def edit_staff_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    gender = request.POST['radio']
    print(gender)
    place = request.POST['textfield4']
    Adhar_no = request.POST['textfield5']
    district = request.POST['textfield6']
    post = request.POST['textfield7']
    pin = request.POST['textfield8']
    id = request.POST['id']
    if "fileField" in request.FILES:
        photo = request.FILES['fileField']

        fs = FileSystemStorage()
        date = "staff/" + datetime.now().strftime("%Y%m%d%H%M%S") + photo.name
        fn = fs.save(date, photo)
        path = fs.url(date)

        s = Staff.objects.get(id=id)
        s.SHOP = Shop.objects.get(LOGIN=request.session['lid'])
        s.name = name
        s.email = email
        s.phone = phone
        s.gender = gender
        s.place = place
        s.aadhar_no = Adhar_no
        s.district = district
        s.post = post
        s.pin = pin
        s.photo = path
        s.save()
        return HttpResponse('''<script>alert('Updation successfull');window.location="/myapp/view_staff/"</script>''')
    else:
        s = Staff.objects.get(id=id)
        s.SHOP = Shop.objects.get(LOGIN=request.session['lid'])
        s.name = name
        s.email = email
        s.phone = phone
        s.gender = gender
        s.place = place
        s.aadhar_no = Adhar_no
        s.district = district
        s.post = post
        s.pin = pin
        s.save()
        return HttpResponse('''<script>alert('Updation successfull');window.location="/myapp/view_staff/"</script>''')


def delete_staff(request,id):
    stff = Staff.objects.get(id=id).delete()

    return HttpResponse('''<script>alert('Deleted successfull');window.location="/myapp/view_staff/"</script>''')
def add_device(request):
    return render(request, 'Add_device.html')
def add_device_post(request):
    name = request.POST['textfield']
    brand=request.POST['brand']
    photo = request.FILES['fileField']
    desc=request.POST['textfield2']
    rent_amount=request.POST['textfield3']

    fs = FileSystemStorage()
    date = "staff/" + datetime.now().strftime("%Y%m%d%H%M%S") + photo.name
    fn = fs.save(date, photo)
    path = fs.url(date)

    d=Device()
    d.SHOP = Shop.objects.get(LOGIN=request.session['lid'])
    d.name=name
    d.brand=brand
    d.photo = path
    d.description=desc
    d.rent_amount=rent_amount
    d.save()
    return HttpResponse('''<script>alert('Added successfully');window.location="/myapp/view_device/"</script>''')
def view_device(request):
    dev = Device.objects.filter(SHOP__LOGIN_id=request.session['lid'])
    return render(request,'view_device.html',{'data': dev})
def view_device_search(request):
    search = request.POST['search']
    res = Device.objects.filter(name__icontains=search)
    return render(request, 'view_device.html', {'data': res})
def edit_device(request,id):
    dev = Device.objects.get(id=id)
    return render(request, 'Edit_device.html', {'data': dev})
def edit_device_post(request):
    name = request.POST['textfield']
    brand=request.POST['brand']
    id = request.POST['id']
    desc = request.POST['textfield2']
    rent_amount = request.POST['textfield3']
    if "fileField" in request.FILES:
        photo = request.FILES['fileField']

        fs = FileSystemStorage()
        date = "staff/" + datetime.now().strftime("%Y%m%d%H%M%S") + photo.name
        fn = fs.save(date, photo)
        path = fs.url(date)

        d = Device.objects.get(id=id)
        d.SHOP = Shop.objects.get(LOGIN=request.session['lid'])
        d.name = name
        d.brand=brand
        d.photo = path
        d.description = desc
        d.rent_amount = rent_amount
        d.save()
        return HttpResponse('''<script>alert('Updation successfull');window.location="/myapp/view_device/"</script>''')
    else:
        d = Device.objects.get(id=id)
        d.SHOP = Shop.objects.get(LOGIN=request.session['lid'])
        d.name = name
        d.brand=brand
        d.description = desc
        d.rent_amount = rent_amount
        d.save()
        return HttpResponse('''<script>alert('Updation successfull');window.location="/myapp/view_device/"</script>''')

def delete_device(request, id):
    dev = Device.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location="/myapp/view_device/"</script>''')
def logout(request):
    return render(request,'adminlogin.html')






#
def user_login(request):
    username=request.POST['name']
    password=request.POST['password']
    print(request.POST)
    res = Login.objects.filter(username=username, password=password)
    if res.exists():
        res1 = Login.objects.get(username=username, password=password)
        if res1.type == "user":
            lid=res1.id
            nn=User.objects.get(LOGIN_id=lid)
            return JsonResponse({'status': 'ok','lid':str(lid),'type':res1.type,'name':nn.name,'photo':nn.photo,'email':nn.email})

        if res1.type=="DeliveryStaff":
            lid=res1.id
            mm=Staff.objects.get(LOGIN_id=lid)
            # if mm.type == 'Delivery Staff':
            return JsonResponse({'status': 'ok', 'lid': str(lid), 'type': res1.type, 'name': mm.name, 'photo': mm.photo, 'email': mm.email})
            # return JsonResponse({'status': 'No'})

        else:
            return JsonResponse({'status': 'No'})
    else:
          return JsonResponse({'status':'No'})


def user_register(request):
    name=request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    pin = request.POST['pin']
    post = request.POST['post']
    district = request.POST['district']
    photo=request.POST['photo']
    gender = request.POST['gender']
    password = request.POST['password']
    confirm_password = request.POST['confirmpassword']

    date=datetime.now().strftime("%Y%m%d-%H%M%S")
    a=base64.b64decode(photo)
    fh=open("C:\\Users\\VYSHNAV\\PycharmProjects\\Electronic_Rental_system\\media\\user\\"+date+".jpg","wb")
    path='/media/user/'+date+'.jpg'
    fh.write(a)
    fh.close()

    uobjl = Login()
    uobjl.username = email
    uobjl.password = password
    uobjl.type = "user"
    uobjl.save()

    if password == confirm_password:
        uobj = User()
        uobj.LOGIN = uobjl
        uobj.name = name
        uobj.email = email
        uobj.phone = phone
        uobj.place = place
        uobj.photo = path
        uobj.post = post
        uobj.pin = pin
        uobj.district = district
        uobj.gender = gender
        uobj.save()
    return JsonResponse({'status': 'ok'})

def user_view_profile(request):
    lid=request.POST['lid']
    nn=User.objects.get(LOGIN_id=lid)
    return JsonResponse({'status':'ok','name':nn.name,'photo':nn.photo,'email':nn.email,'phone':nn.phone,'post':nn.post,'pin':nn.pin,'district':nn.district,'gender':nn.gender,'place':nn.place})

def user_edit_profile(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    pin = request.POST['pin']
    post = request.POST['post']
    district = request.POST['district']
    gender = request.POST['gender']
    photo = request.POST['photo']
    lid=request.POST['lid']
    uobj = User.objects.get(LOGIN_id=lid)

    if len(photo)>1:


        date = datetime.now().strftime("%Y%m%d-%H%M%S")
        a = base64.b64decode(photo)
        fh = open("C:\\Users\\VYSHNAV\\PycharmProjects\\Electronic_Rental_system\\media\\user\\" + date + ".jpg", "wb")
        path = '/media/user/' + date + '.jpg'
        fh.write(a)
        fh.close()
        uobj.photo = path
        uobj.save()

    uobj.name = name
    uobj.email = email
    uobj.phone = phone
    uobj.place = place
    uobj.post = post
    uobj.pin = pin
    uobj.district = district
    uobj.gender = gender
    uobj.save()


    return JsonResponse({'status': 'ok'})

def deliverystaff_view_profile(request):
    lid=request.POST['lid']
    nn=Staff.objects.get(LOGIN_id=lid)
    return JsonResponse({'status':'ok','name':nn.name,'photo':nn.photo,'email':nn.email,'phone':nn.phone,'aadhar_no':nn.aadhar_no,'post':nn.post,'pin':nn.pin,'district':nn.district,'gender':nn.gender,'place':nn.place})
def deliverystaff_edit_profile(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    aadhar_no=request.POST['aadhar_no']
    place = request.POST['place']
    pin = request.POST['pin']
    post = request.POST['post']
    district = request.POST['district']
    gender = request.POST['gender']
    photo = request.POST['photo']
    lid=request.POST['lid']

    if len(photo)>1:


        date = datetime.now().strftime("%Y%m%d-%H%M%S")
        a = base64.b64decode(photo)
        fh = open("C:\\Users\\VYSHNAV\\PycharmProjects\\Electronic_Rental_system\\media\\user\\" + date + ".jpg", "wb")
        path = '/media/user/' + date + '.jpg'
        fh.write(a)
        fh.close()
        sobj = Staff.objects.get(LOGIN_id=lid)

        sobj.photo = path
        sobj.name = name
        sobj.email = email
        sobj.phone = phone
        sobj.aadhar_no = aadhar_no
        sobj.place = place
        sobj.post = post
        sobj.pin = pin
        sobj.district = district
        sobj.gender = gender
        sobj.save()
        sobj.save()


    else:
        sobj = Staff.objects.get(LOGIN_id=lid)

        sobj.name = name
        sobj.email = email
        sobj.phone = phone
        sobj.aadhar_no = aadhar_no
        sobj.place = place
        sobj.post = post
        sobj.pin = pin
        sobj.district = district
        sobj.gender = gender
        sobj.save()
        return JsonResponse({'status': 'ok'})

def user_view_shop(request):
    sh=Shop.objects.filter(status="approved")
    sm=[]
    for i in sh:
        sm.append({
            'id':i.id,
            'shop_name':i.shop_name,
            'photo':i.photo,
            'shop_phone':i.shop_phone,
            'Shop_place':i.shop_place,
            'owner_name':i.owner_name,
            'email':i.email,
        })
    return JsonResponse({'status': 'ok', 'data':sm})
def user_view_device(request):
    ss=request.POST['shop_id']
    sh=Device.objects.filter(SHOP_id=ss).order_by('-id')
    sm=[]
    for i in sh:
        sm.append({
            'id':i.id,
            'device_name':i.name,
            'brand':i.brand,
            'photo':i.photo,
            'description':i.description,
            'Rent_amount':i.rent_amount,
        })
    return JsonResponse({'status': 'ok', 'data':sm})

def user_order_device(request):
    sh=request.POST['lid']
    sm=request.POST['iid']
    # amount=request.POST['price']
    ab=Booking()
    ab.DEVICE=Device.objects.get(id=sm)
    ab.USER=User.objects.get(LOGIN_id=sh)
    ab.status='Pending'
    from datetime import datetime
    ab.date=datetime.now().today()
    ab.save()

    p=Payment()
    p.USER=User.objects.get(LOGIN_id=sh)
    p.Booking=ab
    p.status='Paid'
    p.date=datetime.now().today()
    p.save()

    o=Booking.objects.filter(id=p.Booking.id).update(status='Paid')


    return JsonResponse({'status': 'ok'})

def user_change_password(request):
    lid = request.POST['lid']
    old_password = request.POST['old']
    new_password = request.POST['newp']
    c_password = request.POST['cp']
    res=Login.objects.filter(id=lid,password=old_password)
    if res.exists():
        res=Login.objects.get(id=lid,password=old_password)
        res.password=new_password
        res.save()
        return JsonResponse({'status': 'ok'})

    else:
        return JsonResponse({'status':'no'})

def staff_view_profile(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff_profile.html", {'data':ff})

def staff_view_profile_post(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff_profile.html", {'data':ff})

def staff_edit_profile(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff_profile.html/", {'data':ff})


def staff_edit_profile_post(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    gender = request.POST['r1']
    place = request.POST['place']
    Adhar_no = request.POST['adhar_no']
    district = request.POST['district']
    post = request.POST['post']
    pin = request.POST['pin']

    s = Staff.objects.get(LOGIN_id=request.session['lid'])

    if 'photo' in request.FILES:
        photo = request.FILES['photo']

        from datetime import datetime
        d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
        f = FileSystemStorage()
        f.save(d, photo)
        path = f.url(d)
        s.photo = path
        s.save()
    else:
        s.name = name
        s.email = email
        s.phone = phone
        s.gender = gender
        s.place = place
        s.aadhar_no = Adhar_no
        s.district = district
        s.post = post
        s.pin = pin
        # s.photo = path
        s.save()
    # l = Login.objects.get(id=request.session['lid'])
    # l.username = email
    # l.password = password
    # l.save()

        return HttpResponse('''<script>alert("Profile Edited");window.location="/myapp/staff_view_profile/"</script>''')

def view_users(request):
    # if request.session['log'] == "lin":
        a=User.objects.all().order_by('-id')
        return render(request,"view_users.html",{'data':a})
    # else:
    #     return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def view_users_post(request):
    # if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = User.objects.filter(name__contains=search)
        return render(request, "view_users.html", {'data': a})
    # else:
    #     return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")
def user_view_booking_details(request):
    lid = request.POST['lid']
    nn = Booking.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in nn:
        lat=''
        long=''
        delstaff='Not Yet Assigned'
        if Allocation.objects.filter(Booking=i).exists():
            alloc=Allocation.objects.filter(Booking=i)[0]
            delstaff=alloc.STAFF.name
            if location.objects.filter(Login_id=alloc.STAFF.LOGIN_id).exists():
                loc = location.objects.filter(Login_id=alloc.STAFF.LOGIN_id)[0]
                lat=loc.lattitude
                long=loc.longitude

        l.append({
            'id': i.id,
            'device_name': i.DEVICE.name,
            'brand': i.DEVICE.brand,
            'photo': i.DEVICE.photo,
            'Rent_amount': i.DEVICE.rent_amount,
            'status':i.status,
            'date':i.date,
            'lat':lat,
            'long':long,
            'delstaff':delstaff,
        })
    return JsonResponse({'status': 'ok', 'data':l})
    # return JsonResponse({'status': 'ok', 'status':nn.status,'date':nn.date})
def shop_booking_details(request):
    nn=Booking.objects.filter(DEVICE__SHOP__LOGIN_id=request.session['lid']).order_by('-id')
    return render(request, 'view_bookingdetails_shop.html', {'data': nn})

def view_shop_bookingdetails_search(request):
    search = request.POST['search']
    res = Booking.objects.filter(DEVICE__brand=search)
    return render(request, 'view_bookingdetails_shop.html', {'data': res})
def delete_bookingdetails(request,id):
    book = Booking.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location="/myapp/shop_booking_details/"</script>''')
def deliverystaff_change_password(request):
    lid = request.POST['lid']
    old_password = request.POST['old']
    new_password = request.POST['newp']
    c_password = request.POST['cp']
    res=Login.objects.filter(id=lid,password=old_password)
    if res.exists():
        res=Login.objects.get(id=lid,password=old_password)
        res.password=new_password
        res.save()
        return JsonResponse({'status': 'ok'})

    else:
        return JsonResponse({'status':'no'})
def staff_payment_status(request):
    nn=Payment.objects.all()
    return render(request, 'view_paymentstatus.html', {'data': nn})
def view_paymentstatus_search(request):
    search = request.POST['search']
    res = Payment.objects.filter(DEVICE__brand=search)
    return render(request, 'view_paymentstatus.html', {'data': res})
def staff_booking_details(request):
    nn=Booking.objects.filter(DEVICE__SHOP__LOGIN_id=request.session['lid']).order_by('-id')
    return render(request, 'view_bookingdetails_staff.html', {'data': nn})
def view_staff_bookingdetails_search(request):
    search = request.POST['search']
    res = Booking.objects.filter(DEVICE__brand=search)
    return render(request, 'view_bookingdetails_staff.html', {'data': res})
def delete_bookingdetails_staff(request,id):
    book = Booking.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location="/myapp/shop_booking_details/"</script>''')
def assign_order(request,id):
    print(request.session['lid'])
    ss=Staff.objects.filter(type='Delivery Staff',SHOP__LOGIN_id=request.session['lid'])
    return render(request,'assign_order.html',{'data':ss,"id":id})
def assign_order_post(request):
    bid=request.POST['id']
    sid=request.POST['radio']
    aa=Allocation.objects.filter(STAFF_id=sid).exclude(status='pending')
    if aa.exists():

        return HttpResponse(
            '''<script>alert('Selected Staff already Assigned');window.location="/myapp/shop_booking_details/"</script>''')
    else:

     obj = Allocation()
     obj.Booking_id = bid
     obj.STAFF_id = sid
     obj.date = datetime.now().date()
     obj.status = 'pending'
     obj.save()
     return HttpResponse(
        '''<script>alert('Delivery Staff Assigned');window.location="/myapp/shop_booking_details/"</script>''')


def update_location(request):
    lid = request.POST['lid']

    lattitude=request.POST['lattitude']
    longtiude=request.POST['longitude']
    loc=location()
    if location.objects.filter(Login_id=lid).exists():
        loc = location.objects.filter(Login_id=lid)[0]
    loc.lattitude=lattitude
    loc.longitude=longtiude
    loc.Login_id=lid
    loc.save()
    return JsonResponse({'status':'ok'})
def view_orders_assigned(request):
    lid=request.POST['lid']
    allocation=Allocation.objects.filter(STAFF__LOGIN_id=lid,status='pending').order_by('-id')
    l=[]
    for i in allocation:
        l.append({
            'id': i.id,
            'bid':i.Booking.id,
            'device_name': i.Booking.DEVICE.name,
            'brand': i.Booking.DEVICE.brand,
            'photo': i.Booking.DEVICE.photo,
            'Rent_amount': i.Booking.DEVICE.rent_amount,
            # 'status':i.status,
            'date':i.date,
            'name':i.Booking.USER.name,
            'email':i.Booking.USER.email,
            'phone':i.Booking.USER.phone,
            'place':i.Booking.USER.place,
        })
    return JsonResponse({'status': 'ok', 'data': l})

def shop_profile_view(request):
        ff = Shop.objects.get(LOGIN_id=request.session['lid'])
        return render(request, "shop_profile.html", {'data': ff})

def shop_view_profile_post(request):
        ff = Shop.objects.get(LOGIN_id=request.session['lid'])
        return render(request, "shop_profile.html", {'data': ff})

def shop_edit_profile(request):
        ff = Shop.objects.get(LOGIN_id=request.session['lid'])
        return render(request, "shop_profile.html", {'data': ff})

def shop_edit_profile_post(request):
        name = request.POST['shop_name']
        email = request.POST['email']
        phone = request.POST['shop_phone']
        owner_name = request.POST['owner_name']
        place = request.POST['shop_place']
        license_no = request.POST['shop_license_no']
        district = request.POST['district']
        post = request.POST['post']
        pin = request.POST['pin']

        s = Shop.objects.get(LOGIN_id=request.session['lid'])

        if 'photo' in request.FILES:
            photo = request.FILES['photo']

            from datetime import datetime
            d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
            f = FileSystemStorage()
            f.save(d, photo)
            path = f.url(d)
            s.photo = path
            s.save()
        else:
            s.shop_name = name
            s.email = email
            s.shop_phone = phone
            s.owner_name = owner_name
            s.shop_place = place
            s.shop_license_no = license_no
            s.district = district
            s.post = post
            s.pin = pin
            # s.photo = path
            s.save()
            # l = Login.objects.get(id=request.session['lid'])
            # l.username = email
            # l.password = password
            # l.save()

            return HttpResponse(
                '''<script>alert("Profile Edited");window.location="/myapp/shop_profile_view/"</script>''')

def update_work_status(request):
    sid=request.POST['sid']
    bid=request.POST['bid']
    nn=Allocation.objects.filter(id=sid).update(status='Delivered')
    mm=Booking.objects.filter(id=bid).update(status="Delivered")
    return JsonResponse({'status': 'ok'})

def view_work_status(request):
    lid=request.POST['lid']
    allocation=Allocation.objects.filter(STAFF__LOGIN_id=lid,status='Delivered').order_by('-id')
    l=[]
    for i in allocation:
        l.append({
            'id': i.id,
            'device_name': i.Booking.DEVICE.name,
            'brand': i.Booking.DEVICE.brand,
            'photo': i.Booking.DEVICE.photo,
            'Rent_amount': i.Booking.DEVICE.rent_amount,
            # 'status':i.status,
            'date':i.date,
            'name':i.Booking.USER.name,
            'email':i.Booking.USER.email,
            'phone':i.Booking.USER.phone,
            'place':i.Booking.USER.place,
        })
    return JsonResponse({'status': 'ok', 'data': l})
# def shop_name(request):
#     ss = Shop.objects.filter(SHOP__LOGIN_id=request.session['lid'])
#     return render(request,'staff_profile.html')
#
def user_send_complaint(request):
    Lid = request.POST['lid']
    complaint = request.POST['complaint']
    # Status=['Pending']
    # Reply=['Pending']
    c = Complaint()
    c.complaint = complaint
    c.status = 'Pending'
    c.reply = 'Pending'
    from datetime import datetime
    c.date = datetime.now().today()
    c.USER = User.objects.get(LOGIN=Lid)
    c.save()
    return JsonResponse({"status":"ok"})

def viewcomplaint(request):
    # if request.session['log'] == "lin":
    a = Complaint.objects.filter().order_by('-id')
    return render(request, 'view_complaints.html', {'data': a})
    # else:
    #     return HttpResponse("<script>alert('Your Loged Out'); window.location='/myapp/login/'</script>")
def view_comlaint_post(request):
    # if request.session['log'] == "lin":
    Fromdate = request.POST['textfield1']
    Todate = request.POST['textfield2']
    a = Complaint.objects.filter(date__range=[Fromdate, Todate]).order_by('-id')
    return render(request, 'view_complaints.html', {'data': a})

    # else:
    #     return HttpResponse("<script>alert('Your Loged Out'); window.location='/myapp/login/'</script>")
def send_reply(request,id):
    # if request.session['log'] == "lin":
        return render(request, 'send_reply.html',{'id':id})
    # else:
    #     return HttpResponse("<script>alert('Your Loged Out'); window.location='/myapp/login/'</script>")

def sendreply_POST(request):
    # if request.session['log'] == "lin":
        reply=request.POST["textfield"]
        id=request.POST['id']
        Complaint.objects.filter(id=id).update(reply=reply,status='Replied')
        return HttpResponse("<script>alert('Replied'); window.location='/myapp/viewcomplaint/'</script>")
    # else:
    #     return HttpResponse("<script>alert('Your Loged Out'); window.location='/myapp/login/'</script>")


def viewreply_POST(request):
    lid = request.POST['lid']
    a=Complaint.objects.filter(USER__LOGIN_id=lid).order_by('-date')
    l=[]
    for i in a:
        l.append({'id':i.id,'complaint':i.complaint,'status':i.status,'reply':i.reply,'date':i.date})
    return JsonResponse({"status":"ok",'data':l})

def user_send_feedback(request):
    Lid = request.POST['lid']
    feedback = request.POST['feedback']
    # Status=['Pending']
    # Reply=['Pending']
    c = Feedback()
    c.feedback = feedback
    c.status = 'Pending'
    c.reply = 'Pending'
    from datetime import datetime
    c.date = datetime.now().today()
    c.USER = User.objects.get(LOGIN=Lid)
    c.save()
    return JsonResponse({"status":"ok"})
def view_feedback(request):
    # if request.session['log'] == "lin":
    a = Feedback.objects.filter().order_by('-id')
    return render(request, 'view_feedbacks.html', {'data': a})
def view_feedback_post(request):
    # if request.session['log'] == "lin":
    Fromdate = request.POST['textfield1']
    Todate = request.POST['textfield2']
    a = Feedback.objects.filter(date__range=[Fromdate, Todate]).order_by('-id')
    return render(request, 'view_feedbacks.html', {'data': a})
def view_deliverystaff_assigned(request,id):
    ff=Allocation.objects.get(Booking=id)
    return render(request, "view_deliverystaff_assigned.html", {'data':ff,'id':id})