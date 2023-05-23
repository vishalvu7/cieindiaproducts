import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render , redirect

from pharmapp.models import Product

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Menu

# Create your views here.

user = "admin"
passw = "password"

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if(username == user and password == passw):
            
            request.session['admin'] = "yes"
            products = Product.objects.all()

            return render(request, 'admindashboard.html', {'Product':products})
           
        return render(request, 'adminlogin.html')
    else:
        if 'admin' in request.session:
            try:
                products = Product.objects.all()
                root_parents = Menu.objects.filter(parent__isnull=True)
                root_parents_with_children = []
                
                
                
                
                
                root_menus = Menu.objects.filter(parent=None)
                menus = Menu.objects.all().order_by('parent_id')
                for root_menu in root_menus:
                    root_menu.children.set(root_menu.children.all())

                menu_tree = []
                for root_menu in root_menus:
                    menu_tree.append(get_menu_tree(root_menu))
                    
                    
                parent = Menu.objects.first()
                children = parent.children.all()[:1]
                context = {'parent': parent, 'children': children}
                
                
                

                for parent in root_parents:
                    children = parent.children.first()
                    root_parents_with_children.append((parent, children))

                return render(request, 'admindashboard.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children,"menuss":menus})
            except:
                return render(request, 'admindashboard.html')
        return render(request, 'adminlogin.html')

def home(request):
    
    if 'admin' in request.session:
    
        if request.method == 'POST':
            try:
                name = request.POST['name']
                description = request.POST['description']
                image = request.FILES['image']
                
                parent_id = request.POST.get('parent')
                # parent_other = request.POST.get('parent_other')
            

                product = Product(name=name, description=description,category=parent_id, image=image)
                product.save()
                products = Product.objects.all()
                root_parents = Menu.objects.filter(parent__isnull=True)
                root_parents_with_children = []

                for parent in root_parents:
                    children = parent.children.first()
                    root_parents_with_children.append((parent, children))

                return render(request, 'admindashboard.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children})
            except:
                return HttpResponse('Product not found...')
        
        
        else:
            
            
            root_menus = Menu.objects.filter(parent=None)
            menus = Menu.objects.all().order_by('parent_id')
            for root_menu in root_menus:
                root_menu.children.set(root_menu.children.all())

            menu_tree = []
            for root_menu in root_menus:
                menu_tree.append(get_menu_tree(root_menu))
                
                
            parent = Menu.objects.first()
            children = parent.children.all()[:1]
            context = {'parent': parent, 'children': children}
            
            products = Product.objects.all()
                    
            root_parents = Menu.objects.filter(parent__isnull=True)
            root_parents_with_children = []

            for parent in root_parents:
                children = parent.children.first()
                root_parents_with_children.append((parent, children))

            return render(request, 'admindashboard.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})
        
    else:
        return render(request, 'adminlogin.html')
        
    
    
    
def updateProduct(request):
    if 'admin' in request.session:
    
        if request.method == 'POST':
            
            try:
                
                productid = request.POST['productid']
                name = request.POST['name']
                description = request.POST['description']
                image = request.FILES['image']
                
                try:
                    singleproduct = Product.objects.get(id=productid)
                    singleproduct.name = name
                    singleproduct.description = description
                    singleproduct.image = image
                    singleproduct.save()
                except:
                    print("Product not found!")
            
                
                products = Product.objects.all()
                        
                root_parents = Menu.objects.filter(parent__isnull=True)
                root_parents_with_children = []

                for parent in root_parents:
                    children = parent.children.first()
                    root_parents_with_children.append((parent, children))

                return render(request, 'admindashboard.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children})
                
            except:
                products = Product.objects.all()         
                root_parents = Menu.objects.filter(parent__isnull=True)
                root_parents_with_children = []

                for parent in root_parents:
                    children = parent.children.first()
                    root_parents_with_children.append((parent, children))

                return render(request, 'admindashboard.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children})
                
        
        else:
            
            products = Product.objects.all()
            
                    
            root_parents = Menu.objects.filter(parent__isnull=True)
            root_parents_with_children = []

            for parent in root_parents:
                children = parent.children.first()
                root_parents_with_children.append((parent, children))

            return render(request, 'admindashboard.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children})

    else:
        return render(request, 'adminlogin.html')



def deleteProduct(request):
    
    if 'admin' in request.session:
    
        
        if request.method == 'POST':
            
            try:
                productid = request.POST['productdeleteid']
                print("Product id printing")
                print(productid)
                delPro = Menu.objects.get(id=productid)
                delPro.delete()
            except:
                print("Product not found")
        
            products = Product.objects.all()
                        
            root_parents = Menu.objects.filter(parent__isnull=True)
            root_parents_with_children = []

            for parent in root_parents:
                children = parent.children.first()
                root_parents_with_children.append((parent, children))

            return render(request, 'admindashboard.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children})
        
        else:
        
            products = Product.objects.all()
                            
            root_parents = Menu.objects.filter(parent__isnull=True)
            root_parents_with_children = []

            for parent in root_parents:
                children = parent.children.first()
                root_parents_with_children.append((parent, children))

            return render(request, 'admindashboard.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children})
        
        
    else:
        return render(request, 'adminlogin.html')
    
    
    
    
def userHome(request):
    try:
        
        products = Product.objects.all()
        root_menus = Menu.objects.filter(parent=None)
        menus = Menu.objects.all().order_by('parent_id')
        for root_menu in root_menus:
            root_menu.children.set(root_menu.children.all())

        menu_tree = []
        for root_menu in root_menus:
            menu_tree.append(get_menu_tree(root_menu))
            
            
        parent = Menu.objects.first()
        children = parent.children.all()[:1]
        context = {'parent': parent, 'children': children}
        return render(request, 'userhome.html',{"Product":products,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})
    except:
        return render(request, 'userhome.html')
def userproductonclick(request):
    products = Product.objects.all()
    root_menus = Menu.objects.filter(parent=None)
    menus = Menu.objects.all().order_by('parent_id')
    for root_menu in root_menus:
        root_menu.children.set(root_menu.children.all())

    menu_tree = []
    for root_menu in root_menus:
        menu_tree.append(get_menu_tree(root_menu))
        
        
    parent = Menu.objects.first()
    children = parent.children.all()[:1]
    context = {'parent': parent, 'children': children}
    return render(request, 'userproducts.html',{"Product":products,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})





def viewAdminProduct(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if(username == user and password == passw):
            
            request.session['admin'] = "yes"
            products = Product.objects.all()

            return render(request, 'viewadminproducts.html', {'Product':products})
           
        return render(request, 'adminlogin.html')
    else:
        if 'admin' in request.session:
            products = Product.objects.all()
            root_parents = Menu.objects.filter(parent__isnull=True)
            root_parents_with_children = []

            for parent in root_parents:
                children = parent.children.first()
                root_parents_with_children.append((parent, children))

            return render(request, 'viewadminproducts.html', {'Product':products,"children":children,"root_parents_with_children":root_parents_with_children})
        return render(request, 'adminlogin.html')





def sendEmail(request):
    
    if request.method == 'POST':
        
        try:
            
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            sub = request.POST.get('subject')
            
            subject = eval(sub)
            print("priting type of subject")
            print(type(subject))
            
            result = ""
            try:
                for index in subject:
                    result += "- " + "Product Name" + ": " + str(index["name"]) + "\n"
                    result += "- " + "Description" + ": " + str(index["description"]) + "\n"
                    result += "- " + "Quantity" + ": " + str(index["quantity"]) + "\n"
                    
                    result = result + ",    "
            except:
                print("empty list")
            print(result)
            print(type(result))
            
            
            subject =  'Product Quotation'
            message = 'hello, you have products specifications from '+name+'('+email+', contact-'+contact+') ' + result
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['vishalvu7@gmail.com']   
            send_mail( subject, message, email_from, recipient_list ) 
            messages.success(request, 'Email Sent Successfully...')  
            
        
            
            response_data = {'message': 'Data processed successfully'}
            print('email sent')
            return redirect('userhome')
        except:
            print('unable to send email')
            messages.error(request, "could not send email, please try again later...")
            
            return redirect('userhome')
    else:
        
        return redirect('userhome')







def get_menu_tree(menu, level=0, max_depth=30):
    result = {'name': menu.name, 'level': level, 'children': []}
    if level < max_depth:
        for child in menu.children.all():
            result['children'].append(get_menu_tree(child, level + 1, max_depth))
    return result


def createProductCategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        parent_other = request.POST.get('parent_other')

        parent = None
        if parent_id and parent_id != '__other__':
            parent = Menu.objects.get(id=parent_id)

        if parent_other:
            parent = Menu.objects.create(name=parent_other)

        menu = Menu.objects.create(name=name, parent=parent)
        menus = Menu.objects.all().order_by('parent_id')

        return redirect("admin")

    else:
        root_menus = Menu.objects.filter(parent=None)
        menus = Menu.objects.all().order_by('parent_id')
        for root_menu in root_menus:
            root_menu.children.set(root_menu.children.all())

        menu_tree = []
        for root_menu in root_menus:
            menu_tree.append(get_menu_tree(root_menu))
            
            
        parent = Menu.objects.first()
        children = parent.children.all()[:1]
        context = {'parent': parent, 'children': children}
        
  
        

        
        return render(request, 'addcategory.html', {'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})



    

def aboutUs(request):
    try:
        products = Product.objects.all()
        root_menus = Menu.objects.filter(parent=None)
        menus = Menu.objects.all().order_by('parent_id')
        for root_menu in root_menus:
            root_menu.children.set(root_menu.children.all())

        menu_tree = []
        for root_menu in root_menus:
            menu_tree.append(get_menu_tree(root_menu))
            
            
        parent = Menu.objects.first()
        children = parent.children.all()[:1]
        context = {'parent': parent, 'children': children}
        return render(request, 'aboutus.html',{"Product":products,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})
    except:
        return render(request, 'aboutus.html')
    
    
    
    
def products_by_category(request,menu_name):
    if request.method == 'GET':
        # menu_name = request.GET.get('catname')
        print("Product category name")
        print(menu_name)
    
    
        products = Product.objects.filter(category=menu_name)


        try:
            
            root_menus = Menu.objects.filter(parent=None)
            menus = Menu.objects.all().order_by('parent_id')
            for root_menu in root_menus:
                root_menu.children.set(root_menu.children.all())

            menu_tree = []
            for root_menu in root_menus:
                menu_tree.append(get_menu_tree(root_menu))
                
                
            parent = Menu.objects.first()
            children = parent.children.all()[:1]
            context = {'parent': parent, 'children': children}
            return render(request, 'userhome.html',{"Product":products,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})
        except:
             return render(request, 'userhome.html')
    
    
    
    
    
    
def logOut(request):
    if request.method == 'POST':
        del request.session['admin']
        return redirect('admin')
    else:
        pass