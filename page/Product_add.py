import base64
from fileinput import filename
from uuid import UUID
from flask import *
from flask_login import *
from numpy import require
from flask_sqlalchemy import *

from configuration import website, user_database
from forms import LoginForm, ShopForm, ProductForm
from model.shop import Shop
from model.user import User
from model.product import Product
 
 
def product_add(Shop_Form, Product_Form):
    selling_shop = Shop.query.filter_by(uid = current_user.get_id(), name = Product_Form.shop_name.data).first()

    if selling_shop is None:
        flash("商店不存在", category="product add errors")
        return render_template(
                                'nav.html', 
                                shop_product = Shop.query.join(Shop, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                                shop_form = Shop_Form,
                                product_form = Product_Form,
                                user = User.query.filter_by(id=current_user.get_id()).first(), 
                                has_shop=Shop.query.filter_by(uid=current_user.get_id())
                            )
    product = Product.query.filter_by(name=Product_Form.name.data, sid = selling_shop.sid).first()
    if product is not None:
        flash("商品已經存在", category="product add errors")
        return render_template(
                                'nav.html', 
                                shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                                shop_form = Shop_Form, 
                                product_form = Product_Form,
                                user = User.query.filter_by(id=current_user.get_id()).first(), 
                                has_shop=Shop.query.filter_by(uid=current_user.get_id())
                            )
    else:
        images = base64.b64encode(request.files['picture'].read())
        new_product = Product(selling_shop.sid, Product_Form.name.data, Product_Form.quantity.data, Product_Form.price.data, images)
        user_database.session.add(new_product)
        user_database.session.commit()
        flash("商品新增成功",category="product add success")
        return render_template(
                                'nav.html', 
                                shop_product = Shop.query.join(Product, Shop.sid == Product.sid and Shop.pid == current_user.get_id()).add_columns(Product.name, Product.pid, Product.price, Product.quantity, Product.picture),
                                shop_form = Shop_Form, 
                                product_form = Product_Form,
                                user = User.query.filter_by(id=current_user.get_id()).first(), 
                                has_shop=Shop.query.filter_by(uid=current_user.get_id())
                            )