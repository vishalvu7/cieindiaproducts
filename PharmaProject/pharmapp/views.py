import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render , redirect

from pharmapp.models import Product

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Category, SubCategory

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
                categories = Category.objects.all()
                subcategories = SubCategory.objects.all()
               

                products = Product.objects.all()
                return render(request, 'admindashboard.html', {'Product':products,'categories': categories, 'subcategories': subcategories})
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
                parent_name = request.POST.get('parent')
                # parent_other = request.POST.get('parent_other')    

                product = Product(name=name, description=description,category=parent_name, image=image)
                product.save()
                products = Product.objects.all()
                
                categories = Category.objects.all()
                subcategories = SubCategory.objects.all()              

                return render(request, 'admindashboard.html', {'Product':products,'categories': categories, 'subcategories': subcategories})
            except:
                return HttpResponse('Product not found...')
        
        
        else:
            
            
            categories = Category.objects.all()
            subcategories = SubCategory.objects.all()
            
            products = Product.objects.all()
            
                

            return render(request, 'admindashboard.html', {'Product':products,'categories': categories, 'subcategories': subcategories})
        
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
                        
               
                categories = Category.objects.all()
                subcategories = SubCategory.objects.all()
            
                return render(request, 'admindashboard.html', {'Product':products,'categories': categories, 'subcategories': subcategories})
                
            except:
                products = Product.objects.all()         
                categories = Category.objects.all()
                subcategories = SubCategory.objects.all()

                return render(request, 'admindashboard.html', {'Product':products,'categories': categories, 'subcategories': subcategories})
                
        
        else:
            
            products = Product.objects.all()
            
                    
            root_parents = Category.objects.filter(parent__isnull=True)
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
                delPro = Product.objects.get(id=productid)
                delPro.delete()
            except:
                print("Product not found")
        
            products = Product.objects.all()
                        
            

            return render(request, 'admindashboard.html', {'Product':products})
        
        else:
        
            products = Product.objects.all()
                            
            

            return render(request, 'admindashboard.html', {'Product':products})
        
        
    else:
        return render(request, 'adminlogin.html')


def update_category(request, category_id, children_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(SubCategory, id=children_id)

    if request.method == 'POST':
        name = request.POST['name']
        category.name = name
        category.save()
        subcatname = request.POST['subcategory']
        subcategory.name = subcatname
        subcategory.save()
        return redirect('viewadminproducts')  # Redirect back to the admin page
    
    else:
        return render(request, 'editcategory.html', {'category': category,'subcategory': subcategory})



    
    
def delete_category(request, category_id):
    if request.method == 'POST':
        print("my category id")
        print(category_id)
        category = Category.objects.get(id=category_id)

        if category.subcategories.exists():
            return redirect('viewadminproducts')  

       
        category.delete()
        return redirect('viewadminproducts')
    else:
        root_parents_with_children = []
        categories = Category.objects.all()

        for parent in categories:
            children = parent.subcategories.first()
            root_parents_with_children.append((parent, children))
        return render(request, 'viewadminproducts.html', {'root_parents_with_children': root_parents_with_children})
def userHome(request):
    try:
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()
        products = Product.objects.all()
        
        return render(request, 'userhome.html', {
            'Product': products,
            'parent_categories': categories,
            'subcategories': subcategories
        })
    except:
        return render(request, 'userhome.html')
    
def userproductonclick(request):
    products = Product.objects.all()
    root_menus = Category.objects.filter(parent=None)
    menus = Category.objects.all().order_by('parent_id')
    for root_menu in root_menus:
        root_menu.children.set(root_menu.children.all())

    menu_tree = []
    for root_menu in root_menus:
        menu_tree.append(get_menu_tree(root_menu))
        
        
    parent = Category.objects.first()
    children = parent.children.all()[:1]
    context = {'parent': parent, 'children': children}
    return render(request, 'userproducts.html',{"Product":products,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})




def viewAdminProduct(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == user and password == passw:
            request.session['admin'] = "yes"
            products = Product.objects.all()

            return render(request, 'viewadminproducts.html', {'Product': products})
           
        return render(request, 'adminlogin.html')
    else:
        if 'admin' in request.session:
            try:
                categories = Category.objects.filter(subcategories__isnull=False).distinct()
                root_parents_with_children = []

                for parent in categories:
                    children = parent.subcategories.all()
                    root_parents_with_children.append((parent, children))
                    
               

                return render(request, 'viewadminproducts.html', {'root_parents_with_children': root_parents_with_children})
            except:
                return render(request, 'viewadminproducts.html')
        return render(request, 'adminlogin.html')



# def viewAdminProduct(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         if username == user and password == passw:
#             request.session['admin'] = "yes"
#             products = Product.objects.all()

#             return render(request, 'viewadminproducts.html', {'Product': products})
           
#         return render(request, 'adminlogin.html')
#     else:
#         if 'admin' in request.session:
#             try:
#                 root_parents_with_children = []
#                 categories = Category.objects.all()

#                 for parent in categories:
#                     children = parent.subcategories.first()
#                     root_parents_with_children.append((parent, children))

#                 return render(request, 'viewadminproducts.html', {'root_parents_with_children': root_parents_with_children})
#             except:
#                 return render(request, 'viewadminproducts.html')
#         return render(request, 'adminlogin.html')




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
        parent_subcategory_id = request.POST.get('parent_subcategory')

        if parent_id == "__other__":
            parent_subcategory = SubCategory.objects.get(name=parent_other)
            subcategory = SubCategory(name=name, parent_subcategory=parent_subcategory)
            subcategory.save()
        else:
            if parent_id:
                parent_category = Category.objects.get(id=parent_id)
                if parent_subcategory_id:
                    parent_subcategory = SubCategory.objects.get(id=parent_subcategory_id)
                else:
                    parent_subcategory = None
            else:
                parent_category = None
                parent_subcategory = None

            if parent_category:
                subcategory = SubCategory(name=name, parent_category=parent_category, parent_subcategory=parent_subcategory)
                subcategory.save()
            elif parent_subcategory:
                subcategory = SubCategory(name=name, parent_subcategory=parent_subcategory)
                subcategory.save()
            else:
                category = Category(name=name)
                category.save()

        return redirect("admin")  # Replace "admin" with your desired redirect URL

    else:
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()

        return render(request, 'addcategory.html', {'categories': categories, 'subcategories': subcategories})






    

def aboutUs(request):
    try:
        products = Product.objects.all()
        root_menus = Category.objects.filter(parent=None)
        menus = Category.objects.all().order_by('parent_id')
        for root_menu in root_menus:
            root_menu.children.set(root_menu.children.all())

        menu_tree = []
        for root_menu in root_menus:
            menu_tree.append(get_menu_tree(root_menu))
            
            
        parent = Category.objects.first()
        children = parent.children.all()[:1]
        context = {'parent': parent, 'children': children}
        return render(request, 'aboutus.html',{"Product":products,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})
    except:
        return render(request, 'aboutus.html')
    


def products_by_category(request,menu_name):
    if request.method == 'GET':
        # menu_name = request.GET.get('catname')
    
    
        products = Product.objects.filter(category=menu_name)


        try:
            
            categories = Category.objects.all()
            subcategories = SubCategory.objects.all()
               

            return render(request, 'userhome.html', {'Product':products,'categories': categories, 'subcategories': subcategories})
            
        except:
             return render(request, 'userhome.html')    
    
    
# def products_by_category(request,menu_name):
#     if request.method == 'GET':
#         # menu_name = request.GET.get('catname')
    
    
#         products = Product.objects.filter(category=menu_name)


#         try:
            
#             root_menus = Category.objects.filter(parent=None)
#             menus = Category.objects.all().order_by('parent_id')
#             for root_menu in root_menus:
#                 root_menu.children.set(root_menu.children.all())

#             menu_tree = []
#             for root_menu in root_menus:
#                 menu_tree.append(get_menu_tree(root_menu))
                
                
#             parent = Category.objects.first()
#             children = parent.children.all()[:1]
#             context = {'parent': parent, 'children': children}
#             return render(request, 'userhome.html',{"Product":products,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})
#         except:
#              return render(request, 'userhome.html')
    
    
    
    
    
    
def logOut(request):
    if request.method == 'POST':
        del request.session['admin']
        return redirect('admin')
    else:
        pass
    
    
    
def feedBack(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            
            subject =  'Product Quotation'
            message = 'hello, you have feedback from '+name+'('+email+') ' + '\n' + message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]   
            send_mail( subject, message, email_from, recipient_list ) 
            messages.error(request, 'Email Sent Successfully...')  
            
            return render(request, 'userfeedback.html')
            
        except:
            messages.error(request, 'Unable to send feedback...')  
            
            
            return render(request, 'userfeedback.html')
    else:
        
        try:
            
            products = Product.objects.all()
            root_menus = Category.objects.filter(parent=None)
            menus = Category.objects.all().order_by('parent_id')
            for root_menu in root_menus:
                root_menu.children.set(root_menu.children.all())

            menu_tree = []
            for root_menu in root_menus:
                menu_tree.append(get_menu_tree(root_menu))
                
                
            parent = Category.objects.first()
            children = parent.children.all()[:1]
            context = {'parent': parent, 'children': children}
            return render(request, 'userfeedback.html',{"Product":products,'menu_tree': menu_tree,"menuss":menus,'parent': parent,'children': children})
        except:
            return render(request, 'userfeedback.html')
        
def ourPresence(request):
    return render(request, 'ourpresence.html')