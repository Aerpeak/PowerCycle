from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

# ---------------- APP CONFIG ----------------

app = Flask(__name__, template_folder='Template', static_folder='Template/static')
app.secret_key = "Mak"

UPLOAD_FOLDER = 'Template/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "powercycle"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# ---------------- PUBLIC PAGES ----------------

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            l.ListingID,
            l.ListingTitle,
            l.Price,
            l.Location,
            u.FirstName,
            u.LastName,
            li.ImagePath
        FROM listing l
        JOIN user u ON l.SellerID = u.UserID
        LEFT JOIN listing_image li
            ON l.ListingID = li.ListingID AND li.isPrimary = 1
        WHERE l.isCurrent = 1
    """)
    items = cursor.fetchall()
    cursor.close()
    return render_template('index.html', items=items)





# ---------------- HOME PAGE ----------------

@app.route('/home')
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            l.ListingID,
            l.ListingTitle,
            l.Price,
            l.Location,
            u.FirstName,
            u.LastName,
            li.ImagePath
        FROM listing l
        JOIN user u ON l.SellerID = u.UserID
        LEFT JOIN listing_image li
            ON l.ListingID = li.ListingID AND li.isPrimary = 1
        WHERE l.isCurrent = 1
          AND l.item_count > 0   --  hides sold out items
    """)
    items = cursor.fetchall()
    cursor.close()

    return render_template('Home.html', items=items)


# ---------------- AUTH ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT *
            FROM user
            WHERE Email = %s
        """, (email,))
        user = cursor.fetchone()
        cursor.close()

        if not user or user['Password'] != password:
            flash('Incorrect email or password', 'danger')
            return redirect(url_for('login'))

        session['user_id'] = user['UserID']
        session['user_type'] = user['UserType']
        session['first_name'] = user['FirstName']
        session['last_name'] = user['LastName']

        # 🔑 ROLE BASED REDIRECT
        if user['UserType'] == 'Admin':
            return redirect(url_for('admin_dashboard'))

        return redirect(url_for('home'))

    return render_template('Log_in.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first = request.form.get('first')
        last = request.form.get('last')
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE Email=%s", (email,))
        if cursor.fetchone():
            cursor.close()
            flash('Email already registered', 'warning')
            return redirect(url_for('register'))

        cursor.execute("""
            INSERT INTO user (FirstName, LastName, Email, Password)
            VALUES (%s, %s, %s, %s)
        """, (first, last, email, password))
        mysql.connection.commit()
        cursor.close()

        flash('Account created — please log in', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')



#----------------- LOGOUT ----------------

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('home'))

#  ---------------- ADMIN ----------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if not admin_only():
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM user")
    total_users = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS sellers FROM user WHERE UserType='Seller'")
    sellers = cursor.fetchone()['sellers']

    cursor.execute("SELECT COUNT(*) AS buyers FROM user WHERE UserType='Buyer'")
    buyers = cursor.fetchone()['buyers']

    cursor.execute("SELECT COUNT(*) AS listings FROM listing")
    listings = cursor.fetchone()['listings']

    cursor.close()

    return render_template(
        'AdminDashboard.html',
        total_users=total_users,
        sellers=sellers,
        buyers=buyers,
        listings=listings
    )



# ---------------- VIEW USERS (ADMIN) ----------------

@app.route('/admin/users')
def admin_users():
    if session.get('user_type') != 'Admin':
        flash('Admin access only', 'danger')
        return redirect(url_for('home'))

    search = request.args.get('q', '').strip()

    cursor = mysql.connection.cursor()

    if search:
        cursor.execute("""
            SELECT *
            FROM user
            WHERE
                FirstName LIKE %s
                OR LastName LIKE %s
                OR Email LIKE %s
                OR UserType LIKE %s
            ORDER BY Created_at DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("""
            SELECT *
            FROM user
            ORDER BY Created_at DESC
        """)

    users = cursor.fetchall()
    cursor.close()

    return render_template(
        'AdminUsers.html',
        users=users,
        search=search
    )

# ---------------- VIEW LISTINGS (ADMIN) ----------------
@app.route('/admin/listing')
def admin_listing():
    if session.get('user_type') != 'Admin':
        flash('Admin access only', 'danger')
        return redirect(url_for('home'))

    search = request.args.get('q', '').strip()
    cursor = mysql.connection.cursor()

    if search:
        cursor.execute("""
            SELECT
                l.ListingID,
                l.ListingTitle,
                l.ListingDescription,
                l.Location,
                l.`Condition`,
                l.item_count,
                l.Price,
                l.isCurrent,
                u.FirstName,
                u.LastName
            FROM listing l
            JOIN user u ON l.SellerID = u.UserID
            WHERE
                l.ListingTitle LIKE %s
                OR l.ListingDescription LIKE %s
                OR l.Location LIKE %s
                OR l.`Condition` LIKE %s
                OR u.FirstName LIKE %s
                OR u.LastName LIKE %s
            ORDER BY l.Created_at DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("""
            SELECT
                l.ListingID,
                l.ListingTitle,
                l.ListingDescription,
                l.Location,
                l.`Condition`,
                l.item_count,
                l.Price,
                l.isCurrent,
                u.FirstName,
                u.LastName
            FROM listing l
            JOIN user u ON l.SellerID = u.UserID
            ORDER BY l.Created_at DESC
        """)

    listings = cursor.fetchall()
    cursor.close()

    return render_template(
        'Manage_Listing.html',
        listings=listings,
        search=search
    )


# ---------------- DELETE USER (ADMIN) ----------------

@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if not admin_only():
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM user WHERE UserID=%s", (user_id,))
    mysql.connection.commit()
    cursor.close()

    flash('User and all related data deleted', 'success')
    return redirect(url_for('admin_users'))


#---------------- VIEW SELLER LISTINGS (ADMIN) ----------------
@app.route('/admin/seller/<int:seller_id>/listings')
def admin_seller_listings(seller_id):
    if session.get('user_type') != 'Admin':
        flash('Admin access only', 'danger')
        return redirect(url_for('home'))

    search = request.args.get('q', '').strip()
    cursor = mysql.connection.cursor()

    if search:
        cursor.execute("""
            SELECT
                l.ListingID,
                l.ListingTitle,
                l.ListingDescription,
                l.Location,
                l.`Condition`,
                l.item_count,
                l.Price,
                l.isCurrent
            FROM listing l
            WHERE l.SellerID = %s
              AND (
                    l.ListingTitle LIKE %s
                    OR l.ListingDescription LIKE %s
                    OR l.Location LIKE %s
                    OR l.`Condition` LIKE %s
              )
            ORDER BY l.Created_at DESC
        """, (
            seller_id,
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("""
            SELECT
                l.ListingID,
                l.ListingTitle,
                l.ListingDescription,
                l.Location,
                l.`Condition`,
                l.item_count,
                l.Price,
                l.isCurrent
            FROM listing l
            WHERE l.SellerID = %s
            ORDER BY l.Created_at DESC
        """, (seller_id,))

    listings = cursor.fetchall()
    cursor.close()

    return render_template(
        'AdminSellerListings.html',
        listings=listings,
        search=search
    )


# ---------------- DELETE LISTING (ADMIN) ----------------

@app.route('/admin/listing/delete/<int:listing_id>', methods=['POST'])
def admin_delete_listing(listing_id):
    if not admin_only():
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM listing WHERE ListingID=%s", (listing_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Listing deleted', 'success')
    return redirect(request.referrer)





def admin_only():
    if session.get('user_type') != 'Admin':
        flash('Admin access only', 'danger')
        return False
    return True

# ---------------- SELLER PROMOTION ----------------

@app.route('/become-seller', methods=['GET', 'POST'])
def become_seller():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE user SET UserType='Seller' WHERE UserID=%s",
                       (session['user_id'],))
        mysql.connection.commit()
        cursor.close()

        session['user_type'] = 'Seller'
        flash('You are now a seller!', 'success')
        return redirect(url_for('home'))

    return render_template('BecomeSeller.html')

# ---------------- SELLER DASHBOARD ----------------

@app.route('/my-listings')
def my_listings():
    if session.get('user_type') != 'Seller':
        flash('Seller access only', 'danger')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()

    # Get seller listings
    cursor.execute("""
        SELECT 
            ListingID,
            ListingTitle,
            ListingDescription,
            `Condition`,
            Price,
            item_count,
            isCurrent
        FROM listing
        WHERE SellerID = %s AND isCurrent = 1
    """, (session['user_id'],))
    listings = cursor.fetchall()

    for listing in listings:
        # Get orders for this listing
        cursor.execute("""
            SELECT 
                o.OrderID,
                oi.Quantity,
                t.TransactionStatus,
                t.BuyerConfirmed,
                u.FirstName,
                u.LastName
            FROM `order` o
            JOIN orderitem oi ON o.OrderID = oi.OrderID
            JOIN transaction t ON o.OrderID = t.OrderID
            JOIN user u ON o.BuyerID = u.UserID
            WHERE oi.ListingID = %s
        """, (listing['ListingID'],))

        orders = cursor.fetchall()
        listing['orders'] = orders

        #  IMPORTANT FLAG
        listing['has_completed_transaction'] = any(
            o['TransactionStatus'] == 'Completed'
            for o in orders
        )

    cursor.close()
    return render_template('MyListing.html', listings=listings)


# ---------------- ADD LISTING ----------------

@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if session.get('user_type') != 'Seller':
        flash('Seller access only', 'danger')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT CategoryID, CategoryName FROM category")
    categories = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        item_count = request.form['item_count']
        description = request.form['description']
        condition = request.form['condition']
        location = request.form['location']
        category_id = request.form['category_id']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO listing (
                SellerID,
                CategoryID,
                ListingTitle,
                Location,
                `Condition`,
                Price,
                ListingDescription,
                item_count,
                Created_at,
                Updated_at,
                isCurrent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NULL, 1)
        """, (
            session['user_id'],
            category_id,
            title,
            location,
            condition,
            price,
            description,
            item_count
        ))

        listing_id = cursor.lastrowid

        images = request.files.getlist('images[]')
        for index, image in enumerate(images):
            if image and image.filename:
                filename = f"{listing_id}_{index}_{secure_filename(image.filename)}"
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                cursor.execute("""
                    INSERT INTO listing_image (ListingID, ImagePath, isPrimary)
                    VALUES (%s, %s, %s)
                """, (listing_id, filename, 1 if index == 0 else 0))

        mysql.connection.commit()
        cursor.close()

        flash('Listing added successfully', 'success')
        return redirect(url_for('home'))

    return render_template('AddItem.html', categories=categories)

# ---------------- EDIT LISTING (VERSIONED) ----------------

@app.route('/edit-listing/<int:listing_id>', methods=['GET', 'POST'])
def edit_listing(listing_id):
    if session.get('user_type') != 'Seller':
        flash('Seller access only', 'danger')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT *
        FROM listing
        WHERE ListingID=%s AND SellerID=%s AND isCurrent=1
    """, (listing_id, session['user_id']))
    old_item = cursor.fetchone()

    if not old_item:
        cursor.close()
        flash('Listing not found', 'danger')
        return redirect(url_for('my_listings'))

    cursor.execute("SELECT CategoryID, CategoryName FROM category")
    categories = cursor.fetchall()

    if request.method == 'POST':
        cursor.execute("UPDATE listing SET isCurrent=0 WHERE ListingID=%s", (listing_id,))

        cursor.execute("""
            INSERT INTO listing (
                SellerID,
                CategoryID,
                ListingTitle,
                Location,
                `Condition`,
                Price,
                ListingDescription,
                item_count,
                Created_at,
                Updated_at,
                isCurrent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 1)
        """, (
            session['user_id'],
            request.form['category_id'],
            request.form['title'],
            request.form['location'],
            request.form['condition'],
            request.form['price'],
            request.form['description'],
            request.form['item_count'],
            old_item['Created_at']
        ))

        mysql.connection.commit()
        cursor.close()
        flash('Listing updated', 'success')
        return redirect(url_for('my_listings'))

    cursor.close()
    return render_template('EditListing.html', item=old_item, categories=categories)

# ---------------- DELETE LISTING (VERSIONED) ----------------

@app.route('/delete-listing/<int:listing_id>')
def delete_listing(listing_id):
    if session.get('user_type') != 'Seller':
        flash('Seller access only', 'danger')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT *
        FROM listing
        WHERE ListingID=%s AND SellerID=%s AND isCurrent=1
    """, (listing_id, session['user_id']))
    old_item = cursor.fetchone()

    if not old_item:
        cursor.close()
        flash('Listing not found', 'danger')
        return redirect(url_for('my_listings'))

    cursor.execute("UPDATE listing SET isCurrent=0 WHERE ListingID=%s", (listing_id,))

    cursor.execute("""
        INSERT INTO listing (
            SellerID,
            CategoryID,
            ListingTitle,
            Location,
            `Condition`,
            Price,
            ListingDescription,
            item_count,
            Created_at,
            Updated_at,
            isCurrent
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 0)
    """, (
        session['user_id'],
        old_item['CategoryID'],
        old_item['ListingTitle'],
        old_item['Location'],
        old_item['Condition'],
        old_item['Price'],
        old_item['ListingDescription'],
        old_item['item_count'],
        old_item['Created_at']
    ))

    mysql.connection.commit()
    cursor.close()
    flash('Listing deleted', 'success')
    return redirect(url_for('my_listings'))


# ---------------- VIEW LISTING ----------------    
@app.route('/listing/<int:listing_id>')
def view_listing(listing_id):
    cursor = mysql.connection.cursor()

    # Get listing details
    cursor.execute("""
        SELECT 
            l.ListingID,
            l.ListingTitle,
            l.Price,
            l.Location,
            l.`Condition`,
            l.ListingDescription,
            l.item_count,
            u.FirstName,
            u.LastName
        FROM listing l
        JOIN user u ON l.SellerID = u.UserID
        WHERE l.ListingID = %s AND l.isCurrent = 1
    """, (listing_id,))
    
    item = cursor.fetchone()

    already_ordered = False

    if 'user_id' in session:
        cursor.execute("""
            SELECT oi.OrderItemID
            FROM orderitem oi
            JOIN `order` o ON oi.OrderID = o.OrderID
            WHERE o.BuyerID = %s
            AND oi.ListingID = %s
            AND o.isCurrent = 1
        """, (session['user_id'], listing_id))

        already_ordered = cursor.fetchone() is not None


    if not item:
        cursor.close()
        flash('Listing not found', 'danger')
        return redirect(url_for('home'))

    # Get images
    cursor.execute("""
        SELECT ImagePath
        FROM listing_image
        WHERE ListingID = %s
        ORDER BY isPrimary DESC
    """, (listing_id,))
    
    images = cursor.fetchall()
    cursor.close()

    return render_template(
        'ViewListing.html',
        listing=item,
        images=images,
        already_ordered=already_ordered
    )


#-------- PLACE ORDER  ----------------
@app.route('/order/<int:listing_id>', methods=['POST'])
def place_order(listing_id):
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

    quantity = int(request.form.get('quantity', 1))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT ListingID, SellerID, Price, item_count
        FROM listing
        WHERE ListingID=%s AND isCurrent=1
    """, (listing_id,))
    listing = cursor.fetchone()

    if not listing:
        cursor.close()
        flash('Listing not found', 'danger')
        return redirect(url_for('home'))

    # Prevent buying own item
    if listing['SellerID'] == session['user_id']:           # no feedback if the seller is buying his/her own listing ex. "You cannot purchase your own listing"
        cursor.close()
        flash('You cannot purchase your own listing', 'danger')
        return redirect(url_for('view_listing', listing_id=listing_id))

    # Validate quantity
    if quantity < 1 or quantity > listing['item_count']:
        cursor.close()
        flash('Invalid quantity selected', 'danger')
        return redirect(url_for('view_listing', listing_id=listing_id))

    total_price = listing['Price'] * quantity

    # Check if user already has an active order for this listing
    cursor.execute("""
        SELECT oi.OrderItemID
        FROM orderitem oi
        JOIN `order` o ON oi.OrderID = o.OrderID
        WHERE o.BuyerID = %s
        AND oi.ListingID = %s
        AND o.isCurrent = 1
    """, (session['user_id'], listing_id))

    existing_order = cursor.fetchone()

    if existing_order:
        cursor.close()
        flash('You have already placed an order for this item.', 'warning')
        return redirect(url_for('view_listing', listing_id=listing_id))


    # Create order
    cursor.execute("""
        INSERT INTO `order` (BuyerID, TotalAmount)
        VALUES (%s, %s)
    """, (session['user_id'], total_price))
    order_id = cursor.lastrowid

    # Create order item with quantity
    cursor.execute("""
        INSERT INTO orderitem (OrderID, ListingID, Quantity)
        VALUES (%s, %s, %s)
    """, (order_id, listing_id, quantity))

    # create transaction record
    cursor.execute("""
        INSERT INTO transaction (OrderID)
        VALUES (%s)
    """, (order_id,))


    mysql.connection.commit()
    cursor.close()

    flash('Order placed successfully', 'success')
    return redirect(url_for('my_orders'))


#---------------- VIEW ORDERS ----------------
@app.route('/my-orders')
def my_orders():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    if session.get('user_type') == 'Seller':
        cursor.execute("""
            SELECT 
                o.OrderID,
                l.ListingTitle,
                oi.Quantity,
                l.Price,
                u.FirstName,
                u.LastName,
                t.TransactionStatus,
                t.BuyerConfirmed,
                o.Created_at
            FROM `order` o
            JOIN orderitem oi ON o.OrderID = oi.OrderID
            JOIN listing l ON oi.ListingID = l.ListingID
            JOIN user u ON l.SellerID = u.UserID
            JOIN transaction t ON o.OrderID = t.OrderID
            WHERE o.BuyerID = %s
            ORDER BY o.Created_at DESC
        """, (session['user_id'],))
    else:
        cursor.execute("""
            SELECT 
                o.OrderID,
                l.ListingTitle,
                oi.Quantity,
                l.Price,
                t.TransactionStatus,
                t.BuyerConfirmed,
                o.Created_at,
                u.FirstName,
                u.LastName
            FROM `order` o
            JOIN orderitem oi ON o.OrderID = oi.OrderID
            JOIN listing l ON oi.ListingID = l.ListingID
            JOIN transaction t ON o.OrderID = t.OrderID
            JOIN user u ON l.SellerID = u.UserID
            WHERE o.BuyerID = %s
            ORDER BY o.Created_at DESC
        """, (session['user_id'],))

    orders = cursor.fetchall()
    cursor.close()

    return render_template('orders.html', orders=orders)


#---------------- CANCEL ORDER ----------------
@app.route('/cancel-order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT o.OrderID
        FROM `order` o
        JOIN transaction t ON o.OrderID = t.OrderID
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        WHERE o.OrderID = %s
          AND t.TransactionStatus = 'Pending'
          AND (
                o.BuyerID = %s
                OR l.SellerID = %s
              )
    """, (order_id, session['user_id'], session['user_id']))

    order = cursor.fetchone()

    if not order:
        cursor.close()
        flash('Order not found or cannot be cancelled', 'danger')
        return redirect(request.referrer or url_for('home'))

    cursor.execute("""
        UPDATE transaction
        SET TransactionStatus = 'Cancelled',
            Updated_at = NOW()
        WHERE OrderID = %s
    """, (order_id,))

    mysql.connection.commit()
    cursor.close()

    flash('Order cancelled successfully', 'success')
    return redirect(request.referrer or url_for('home'))

#---------------- BUYER DASHBOARD ----------------
@app.route('/buyer-dashboard')
def buyer_dashboard():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    # 🔹 Pending orders
    cursor.execute("""
        SELECT 
            l.ListingTitle,
            oi.Quantity,
            o.Created_at
        FROM `order` o
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        JOIN transaction t ON o.OrderID = t.OrderID
        WHERE o.BuyerID = %s
          AND t.TransactionStatus = 'Pending'
    """, (session['user_id'],))
    pending_orders = cursor.fetchall()

    # 🔹 Completed orders
    cursor.execute("""
        SELECT 
            l.ListingTitle,
            oi.Quantity,
            t.Updated_at
        FROM `order` o
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        JOIN transaction t ON o.OrderID = t.OrderID
        WHERE o.BuyerID = %s
          AND t.TransactionStatus = 'Completed'
    """, (session['user_id'],))
    completed_orders = cursor.fetchall()

    # 🔹 Cancelled orders
    cursor.execute("""
        SELECT 
            l.ListingTitle,
            oi.Quantity,
            t.Updated_at
        FROM `order` o
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        JOIN transaction t ON o.OrderID = t.OrderID
        WHERE o.BuyerID = %s
          AND t.TransactionStatus = 'Cancelled'
    """, (session['user_id'],))
    cancelled_orders = cursor.fetchall()

    cursor.close()

    return render_template(
        'BuyerDashboard.html',
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        cancelled_orders=cancelled_orders,
        pending_count=len(pending_orders),
        completed_count=len(completed_orders),
        cancelled_count=len(cancelled_orders)
    )



#---------------- FILTER ORDERS BY STATUS ----------------
@app.route('/my-orders/<status>')
def my_orders_by_status(status):
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    if status == 'pending':
        condition = "o.isCurrent = 1"
    elif status == 'cancelled':
        condition = "o.isCurrent = 0"
    elif status == 'completed':
        condition = "0 = 1"  # placeholder
    else:
        flash('Invalid order status', 'danger')
        return redirect(url_for('buyer_dashboard'))

    cursor.execute(f"""
        SELECT 
            o.OrderID,
            o.TotalAmount,
            o.Created_at,
            l.ListingTitle,
            oi.Quantity
        FROM `order` o
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        WHERE o.BuyerID = %s AND {condition}
        ORDER BY o.Created_at DESC
    """, (session['user_id'],))

    orders = cursor.fetchall()
    cursor.close()

    return render_template(
        'orders.html',
        orders=orders,
        status=status.capitalize()
    )

#---------------- SELLER DASHBOARD ----------------
@app.route('/seller-dashboard')
def seller_dashboard():
    if session.get('user_type') != 'Seller':
        flash('Seller access only', 'danger')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()

    # ---------------- COUNTS ----------------
    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM transaction t
        JOIN `order` o ON t.OrderID = o.OrderID
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        WHERE l.SellerID = %s AND t.TransactionStatus = 'Pending'
    """, (session['user_id'],))
    pending_count = cursor.fetchone()['count']

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM transaction t
        JOIN `order` o ON t.OrderID = o.OrderID
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        WHERE l.SellerID = %s AND t.TransactionStatus = 'Completed'
    """, (session['user_id'],))
    completed_count = cursor.fetchone()['count']

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM transaction t
        JOIN `order` o ON t.OrderID = o.OrderID
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        WHERE l.SellerID = %s AND t.TransactionStatus = 'Cancelled'
    """, (session['user_id'],))
    cancelled_count = cursor.fetchone()['count']

    # ---------------- LISTS ----------------
    cursor.execute("""
        SELECT
            o.OrderID,
            l.ListingTitle,
            oi.Quantity,
            u.FirstName,
            u.LastName,
            o.Created_at,
            t.Updated_at
        FROM transaction t
        JOIN `order` o ON t.OrderID = o.OrderID
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        JOIN user u ON o.BuyerID = u.UserID
        WHERE l.SellerID = %s AND t.TransactionStatus = 'Pending'
        ORDER BY o.Created_at DESC
    """, (session['user_id'],))
    pending_orders = cursor.fetchall()

    cursor.execute("""
        SELECT
            o.OrderID,
            l.ListingTitle,
            oi.Quantity,
            u.FirstName,
            u.LastName,
            t.Updated_at
        FROM transaction t
        JOIN `order` o ON t.OrderID = o.OrderID
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        JOIN user u ON o.BuyerID = u.UserID
        WHERE l.SellerID = %s AND t.TransactionStatus = 'Completed'
        ORDER BY t.Updated_at DESC
    """, (session['user_id'],))
    completed_orders = cursor.fetchall()

    cursor.execute("""
        SELECT
            o.OrderID,
            l.ListingTitle,
            oi.Quantity,
            u.FirstName,
            u.LastName,
            t.Updated_at
        FROM transaction t
        JOIN `order` o ON t.OrderID = o.OrderID
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        JOIN user u ON o.BuyerID = u.UserID
        WHERE l.SellerID = %s AND t.TransactionStatus = 'Cancelled'
        ORDER BY t.Updated_at DESC
    """, (session['user_id'],))
    cancelled_orders = cursor.fetchall()

    cursor.close()

    return render_template(
        'SellerDashboard.html',
        pending_count=pending_count,
        completed_count=completed_count,
        cancelled_count=cancelled_count,
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        cancelled_orders=cancelled_orders
    )




#---------------- BUYER CONFIRM RECEIPT ----------------
@app.route('/confirm-received/<int:order_id>', methods=['POST'])
def buyer_confirm(order_id):
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    # ensure buyer owns this order
    cursor.execute("""
        SELECT t.TransactionID
        FROM transaction t
        JOIN `order` o ON t.OrderID = o.OrderID
        WHERE o.OrderID = %s AND o.BuyerID = %s
    """, (order_id, session['user_id']))

    transaction = cursor.fetchone()
    if not transaction:
        cursor.close()
        flash('Unauthorized action', 'danger')
        return redirect(url_for('my_orders'))

    cursor.execute("""
        UPDATE transaction
        SET BuyerConfirmed = 1,
            Updated_at = NOW()
        WHERE OrderID = %s
    """, (order_id,))

    # auto-complete if seller already confirmed
    cursor.execute("""
        UPDATE transaction
        SET TransactionStatus = 'Completed',
            Updated_at = NOW()
        WHERE OrderID = %s
          AND BuyerConfirmed = 1
          AND SellerConfirmed = 1
    """, (order_id,))

    mysql.connection.commit()
    cursor.close()

    flash('Marked as received', 'success')
    return redirect(url_for('my_orders'))


#---------------- SELLER CONFIRM DELIVERY ----------------  
@app.route('/confirm-delivered/<int:order_id>', methods=['POST'])
def seller_confirm(order_id):
    if session.get('user_type') != 'Seller':
        flash('Seller access only', 'danger')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()

    # Verify order belongs to seller
    cursor.execute("""
        SELECT 
            oi.ListingID,
            oi.Quantity
        FROM `order` o
        JOIN orderitem oi ON o.OrderID = oi.OrderID
        JOIN listing l ON oi.ListingID = l.ListingID
        WHERE o.OrderID = %s
          AND l.SellerID = %s
          AND l.isCurrent = 1
    """, (order_id, session['user_id']))

    order_data = cursor.fetchone()

    if not order_data:
        cursor.close()
        flash('Invalid transaction', 'danger')
        return redirect(url_for('my_listings'))

    listing_id = order_data['ListingID']
    quantity = order_data['Quantity']

    # Seller confirms
    cursor.execute("""
        UPDATE transaction
        SET SellerConfirmed = 1,
            Updated_at = NOW()
        WHERE OrderID = %s
    """, (order_id,))

    # Auto-complete if buyer already confirmed
    cursor.execute("""
        UPDATE transaction
        SET TransactionStatus = 'Completed',
            Updated_at = NOW()
        WHERE OrderID = %s
          AND BuyerConfirmed = 1
          AND SellerConfirmed = 1
    """, (order_id,))

    # Reduce stock ONLY (no new listing row!)
    cursor.execute("""
        UPDATE listing
        SET item_count = item_count - %s
        WHERE ListingID = %s
          AND isCurrent = 1
    """, (quantity, listing_id))

    mysql.connection.commit()
    cursor.close()

    flash('Transaction completed successfully', 'success')
    return redirect(url_for('my_listings'))



# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run(debug=True)