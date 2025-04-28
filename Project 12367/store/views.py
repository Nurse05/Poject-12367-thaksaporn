from django.shortcuts import render, redirect
from .models import Product, Order
from .forms import CheckoutForm

# ฟังก์ชันแสดงรายการสินค้า
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# ฟังก์ชันเพิ่มสินค้าลงในตะกร้า
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

# ฟังก์ชันแสดงรายละเอียดตะกร้าสินค้า
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })
    return render(request, 'store/cart_detail.html', {'cart_items': cart_items, 'total': total})

# ฟังก์ชันลบสินค้าออกจากตะกร้า
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')

# ฟังก์ชันการสั่งซื้อ (Checkout)
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    # คำนวณราคารวมและรายละเอียดสินค้าที่อยู่ในตะกร้า
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # รับข้อมูลจากฟอร์ม
            full_name = form.cleaned_data['full_name']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            
            # บันทึกออเดอร์ในฐานข้อมูล
            order = Order.objects.create(
                full_name=full_name,
                address=address,
                phone_number=phone_number,
                total=total,
            )

            # ลบตะกร้าสินค้าออกจาก session
            del request.session['cart']

            # แสดงหน้าขอบคุณพร้อมหมายเลขออเดอร์
            return render(request, 'store/thank_you.html', {'full_name': full_name, 'order_id': order.id})

    else:
        form = CheckoutForm()

    # ส่งข้อมูลราคาสินค้าและฟอร์มไปยัง template
    return render(request, 'store/Location.html', {
        'cart_items': cart_items, 
        'total': total, 
        'form': form
    })

# ฟังก์ชันแสดงหน้า Thank You (หลังจากยืนยันการสั่งซื้อ)
def thank_you(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'store/thank_you.html', {'order': order})

# ฟังก์ชันการอัพเดตสถานะออเดอร์
def update_order_status(request, order_id, status):
    order = Order.objects.get(id=order_id)
    order.status = status
    order.save()
    return redirect('order_detail', order_id=order.id)
