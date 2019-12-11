from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .options import borough_options, bedroom_options, price_options

from .models import Listing

def index(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }

  return render(request, 'listings/listing.html', context)

def search(request):
  queryset_list = Listing.objects.order_by('-list_date')

  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  if 'neighborhood' in request.GET:
    neighborhood = request.GET['neighborhood']
    if neighborhood:
      queryset_list = queryset_list.filter(neighborhood__iexact=neighborhood)

  if 'borough' in request.GET:
    borough = request.GET['borough']
    if borough:
      queryset_list = queryset_list.filter(city__iexact=borough)

  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__gte=bedrooms)

  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'borough_options': borough_options,
    'bedroom_options': bedroom_options,
    'price_options': price_options,
    'listings': queryset_list,
    'values': request.GET
  }
  return render(request, 'listings/search.html', context)
