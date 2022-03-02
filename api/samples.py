from models import User,Staff,Customer

User.objects.create(login_id='ZC001',password='customer')
User.objects.create(login_id='ZA001',password='admin')
User.objects.create(login_id='ZS001',password='staff')
Staff.objects.create(login_id='ZS001')
Customer.objects.create(login_id='ZC001',password='customer')