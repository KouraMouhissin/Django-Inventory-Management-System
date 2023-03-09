from django.shortcuts import render, HttpResponse, redirect
from . import models
from .forms import AddProductForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

@login_required
def dashboard_index(request):
    return render(request,'dashboard/index.html',context={'title':'Tableau De Bord'})




    
#add_products
@login_required
def add_products(request):
    form = AddProductForm()

    if request.method == 'POST':
        form = AddProductForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            context = {
                'result' : 'Nouveau Produit Ajouter avec succes',
                'title':'Ajout De Produits',
            }
            return render(request,'dashboard/result.html',context=context)

        else:
            context = {
                'result' : 'ERROR',
                'title':'Ajout De Produits',
            }
            return render(request,'dashboard/result.html',context=context)

    context = {
        'form' : form,
        'title':'Ajout De Produits',
        }

    return render(request,'dashboard/add_product.html',context=context)





# search_available_products
@login_required
def search_available_products(request):
    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        
        if form.is_valid():
            search_product = form.cleaned_data['search_product']
            
            all_products = models.Available_product_table.objects.filter(product_name = search_product).values()  
            #print(all_products)
            context = {
                'all_products' : all_products,
                'title' : 'Resultat De Recherche',
            }
            
            return render(request,'dashboard/view_available_products.html',context=context)


    context = {
        'form' : form,
        'title':'Recherche De Produit',
        }

    return render(request,'dashboard/search_product.html',context=context)






# view_available_products 
@login_required
def view_available_products(request):

    all_products = models.Available_product_table.objects.all()
    context = {
        'all_products' : all_products,
        'title' : 'Tous Les Produits',
        }
            
    return render(request,'dashboard/view_available_products.html',context=context)





# sell_available_products
@login_required
def sell_available_products(request):

    if request.method == 'POST':
        sell_product_id = request.POST['product_id']
        sell_qty = int(request.POST['sellqty'])
        
        sell_product = models.Available_product_table.objects.filter(id = sell_product_id).values()
        sell_product = sell_product[0]

        if  sell_qty <= sell_product['product_quantity']:
            product = models.Sold_product_table(
                product_id = sell_product['id'], 
                product_name = sell_product['product_name'],
                product_price = sell_product['product_price'],
                product_quantity = sell_qty,
            )
            product.save()

            # UPDATE Available_product_table
            remaning_qty = sell_product['product_quantity'] - sell_qty

            update_product = models.Available_product_table.objects.get(id = sell_product_id)
            update_product.product_quantity = remaning_qty
            update_product.save()
            
            context = {
                'result' : 'Produit vendu avec succes!',
                'title':'Vendre Des Produits',
            }
            return render(request,'dashboard/result.html',context=context)

        else:
            context = {
                'result' : 'La quantité de ce produit est epuise veuillez le recharger',
                'title':'Vendre Des Produits',
            }
            return render(request,'dashboard/result.html',context=context)
        

    all_products = models.Available_product_table.objects.all()
    context = {
        'all_products' : all_products,
        'title' : 'Vendre Des Produits',
        }
            
    return render(request,'dashboard/sell_products.html',context=context)






# view_sold_products
@login_required
def view_sold_products(request):
    all_sold_products = models.Sold_product_table.objects.all()
    context = {
        'all_sold_products' : all_sold_products,
        'title' : 'Les Produits Vendu',
        }
            
    return render(request,'dashboard/view_sold_products.html',context=context)






@login_required
def users(request):
    form = UserCreationForm

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            context = {
                'result' : 'Nouveau Utilisateur Ajouter avec succes',
                'title':'Add User',
            }
            return render(request,'dashboard/result.html',context=context)

        else:
            context = {
                'result' : 'ERROR - Does not meet the requirements!',
                'title':'Add User',
            }
            return render(request,'dashboard/result.html',context=context)

    context = {
        'form' : form,
        'title':'Add User',
        }

    return render(request,'dashboard/user.html',context=context)
