from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='template')

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'aml'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        userType = userDetails.get('user-type')

        if userType == 'bank':
            BankId = userDetails.get('bank-id')
            if BankId:  # Check if BankId is not None or empty
                Name = userDetails.get('bank-name')
                Branch = userDetails.get('bank-branch')
                Address = userDetails.get('bank-address')
                ContactNumber = userDetails.get('bank-contact-number')
                Email = userDetails.get('bank-email')
                UserName = userDetails.get('bank-username')
                Password = userDetails.get('bank-password')
                
                cur = mysql.connection.cursor()
                try:
                    cur.execute("INSERT INTO aml_bankdetails (bank_id, bank_name, bank_branch, bank_address, bank_contactnumber, bank_emailid, bank_username, bank_password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (BankId, Name, Branch, Address, ContactNumber, Email, UserName, Password))
                    mysql.connection.commit()
                    return redirect('/success')  # Redirect to success page after successful registration
                except mysql.connection.IntegrityError as e:
                    print(f"Error inserting bank details: {e}")
                    mysql.connection.rollback()
            else:
                print("Bank ID is missing.")

        elif userType == 'customer':
            CustomerId = userDetails.get('customer-id')
            CustomerName = userDetails.get('customer-name')
            CustomerDob = userDetails.get('customer-dob')
            CustomerAddress = userDetails.get('customer-address')
            CustomerNationality = userDetails.get('customer-nationality')
            CustomerAccountDetails = userDetails.get('customer-account-details')
            CustomerEmail = userDetails.get('customer-email')
            CustomerUsername = userDetails.get('customer-username')
            CustomerPassword = userDetails.get('customer-password')

            # Inserting data into the aml_customeraccountdetails table
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO aml_customeraccountdetails 
                (customerid, customer_name, customer_dob, customer_address, customer_nationality, 
                customer_accountdetails, customer_emailid, customer_username, customer_password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, 
                (CustomerId, CustomerName, CustomerDob, CustomerAddress, CustomerNationality, 
                 CustomerAccountDetails, CustomerEmail, CustomerUsername, CustomerPassword))
            mysql.connection.commit()
            cur.close()

            return redirect('/success')  # Redirect to success page after registration

    return 'Registration failed. Please try again.'

@app.route('/success')
def success():
    return 'Registration successful'


if __name__ == '__main__':
    app.run(debug=True)
