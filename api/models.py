from distutils.command.upload import upload
from operator import mod
from statistics import mode
from tokenize import blank_re
from django.db import models
from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import math
import datetime


class Customer(models.Model):
    cust_id = models.CharField(max_length=10, primary_key=True)
    cust_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=13, unique=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=8)
    address = models.TextField(max_length=250)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.cust_name}"


class Work(models.Model):
    options = (("full", "FULL"), ("half", "HALF"), ("10half", "10HALF"))
    work_id = models.CharField(max_length=10, primary_key=True)
    work_name = models.CharField(max_length=50)
    wage_type = models.CharField(choices=options, max_length=10)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.work_name}"


class Staff(models.Model):
    salary_options = (("monthly", "MONTHLY"), ("wage", "WAGE"))
    work_options = (
        ("tailor", "TAILOR"),
        ("aari", "AARI"),
        ("embroidery", "EMBROIDERY"),
        ("photo", "PHOTO"),
    )
    staff_id = models.CharField(max_length=10, primary_key=True)
    staff_name = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=13, null=True)
    address = models.TextField(max_length=250, null=True)
    city = models.CharField(max_length=50, null=True)
    salary_type = models.CharField(max_length=20, choices=salary_options, null=True)
    salary = models.IntegerField(null=True, blank=True)
    acc_no = models.CharField(max_length=16, null=True)
    bank = models.CharField(max_length=300, null=True)
    ifsc = models.CharField(max_length=20, null=True)
    work_type = models.CharField(max_length=20, choices=work_options, null=True)
    photo = models.ImageField(default="", blank=True, null=True)

    def __str__(self):
        return f"{self.staff_name}"

    # def save(self, *args, **kwargs):
    #     # Opening the uploaded image
    #     im = Image.open(self.photo)

    #     output = BytesIO()

    #     x, y = im.size
    #     x2, y2 = math.floor(x - 50), math.floor(y - 20)
    #     im = im.resize((x2, y2), Image.ANTIALIAS)

    #     # Resize/modify the image
    #     # im = im.resize((300, 300), Image.ANTIALIAS)

    #     # after modifications, save it to the output
    #     im.save(output, format="JPEG", quality=30)
    #     output.seek(0)

    #     # change the imagefield value to be the newley modifed image value
    #     self.photo = InMemoryUploadedFile(
    #         output,
    #         "ImageField",
    #         "%s.jpg" % self.photo.name.split(".")[0],
    #         "image/jpeg",
    #         sys.getsizeof(output),
    #         None,
    #     )

    #     super(Staff, self).save(*args, **kwargs)


class Order(models.Model):
    pickup_options = (("self", "SELF"), ("courier", "COURIER"), ("others", "OTHERS"))
    order_id = models.CharField(max_length=10, primary_key=True, default="")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default="")
    booking_date_time = models.DateTimeField(auto_now=True)
    due_date = models.DateField()
    order_image = models.ImageField(blank=True)
    material_image = models.ImageField(blank=True)
    order_voice_inst = models.CharField(max_length=10, blank=True)
    pickup_type = models.CharField(max_length=20, choices=pickup_options)
    total_amount = models.IntegerField(null=True, blank=True)
    advance_amount = models.IntegerField(null=True, blank=True)
    courier_amount = models.IntegerField(null=True, blank=True)
    courier_address = models.TextField(null=True, blank=True)
    balance_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.order_id} {self.customer}"


class GenCols(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default='',null = True,blank = True,db_constraint = False)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, default='',null = True,blank = True,db_constraint = False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default='',null = True,blank = True,db_constraint = False)
    class Meta:
        abstract = True


class OrderWork(models.Model):
    order_id = models.CharField(max_length=20, default="")
    work_id = models.CharField(max_length=20, default="")
    work_name = models.CharField(max_length=100, default="")
    order_work_item = models.CharField(max_length=20, default="")
    quantity = models.CharField(max_length=20, default="")
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.order_id} {self.work_id}"


class OrderMaterial(models.Model):
    order_id = models.CharField(max_length=20, default="")
    material_id = models.CharField(max_length=20, default="")
    material_name = models.CharField(max_length=100, default="")
    quantity = models.CharField(max_length=20, default="")
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.order_id} {self.material_id}"


class Material(models.Model):
    measurement_options = (("number", "NUMBER"), ("inch", "INCH"), ("meter", "METER"))
    material_id = models.CharField(max_length=10, primary_key=True,blank = True)
    material_name = models.CharField(max_length=100)
    measurement = models.CharField(max_length=20, choices=measurement_options)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.material_name} {self.measurement}"


class OrderWorkStaffAssign(models.Model):
    stage_options = (
        ("cutting", "CUTTING"),
        ("stitching", "STITCHING"),
        ("hook", "HOOK"),
        ("overlock", "OVERLOCK"),
        ("complete_final_stage", "COMPLETE FINAL STAGE"),
    )

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, default="", db_constraint=False
    )
    work = models.ForeignKey(
        Work, on_delete=models.CASCADE, null= True, db_constraint=False
    )
    order_work_label = models.CharField(
        max_length=15, default="", null=True, blank=True
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        default="",
        blank=True,
        null=True,
        db_constraint=False,
    )
    assign_stage = models.CharField(
        max_length=50, choices=stage_options, blank=True, null=True
    )
    assign_date_time = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class OrderMaterialLocation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default="")
    material_location = models.CharField(max_length=20)
    location_placed_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} {self.material_location}"


class OrderWorkStaffTaken(models.Model):
    stage_options = (
        ("cutting", "CUTTING"),
        ("stitching", "STITCHING"),
        ("hook", "HOOK"),
        ("overlock", "OVERLOCK"),
        ("complete_final_stage", "COMPLETE FINAL STAGE"),
    )
    # order = models.ForeignKey(
    #     Order,
    #     on_delete=models.CASCADE,
    #     default="",
    # )
    # staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default='')
    # work = models.ForeignKey(Work, on_delete=models.CASCADE, default='',blank=True,null=True)
    orderworkstaffassign = models.ForeignKey(
        OrderWorkStaffAssign,
        on_delete=models.CASCADE,
        default="",
        blank=True,
        null=True,
    )
    taken_stage = models.CharField(
        max_length=50, choices=stage_options, blank=True, null=True
    )
    taken_date_time = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return f"({self.taken_date_time})"


class OrderWorkStaffStatusCompletion(models.Model):
    stage_options = (
        ("cutting", "CUTTING"),
        ("stitching", "STITCHING"),
        ("hook", "HOOK"),
        ("overlock", "OVERLOCK"),
        ("complete_final_stage", "COMPLETE FINAL STAGE"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default="")
    orderworkstaffassign = models.ForeignKey(
        OrderWorkStaffAssign, on_delete=models.CASCADE, default=""
    )
    work_staff_completion_stage = models.CharField(
        max_length=50, choices=stage_options, blank=True, null=True
    )
    work_completed_date_time = models.DateTimeField(
        auto_now=False, blank=True, null=True
    )
    work_staff_comp_app_date_time = models.DateTimeField(
        auto_now=False, blank=True, null=True
    )
    work_staff_completion_approved = models.BooleanField(default=False)
    order_next_stage_assign = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order}"


class StaffWorkWage(GenCols):
    work_staff_approval_date_time = models.DateTimeField(null=True, blank=True)
    completion_date_time = models.DateTimeField(null=True, blank=True)
    wage = models.IntegerField(default=0, blank=True, null=True)
    wage_given = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.staff} {self.wage}"


class StaffWageGivenStatus(GenCols):
    order_ids = models.CharField(max_length=200, null=True, blank=True)
    wage_from_date = models.DateField()
    wage_to_date = models.DateField()
    wage_given_date = models.DateField(auto_now_add=True)
    total_wage_given = models.IntegerField()
    wage_payment_reference_no = models.CharField(max_length=50)
    wage_payment_reference_image = models.ImageField()

    def __str__(self):
        return f'{self.id}'

class OrderPickupCourier(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    address = models.TextField(blank=True, null=True)
    courier_request_date = models.DateField()
    courier_amount = models.IntegerField()
    eligible_for_courier = models.BooleanField()
    courier_company = models.CharField(max_length=50)
    courier_date = models.DateField()
    courier_reference_no = models.CharField(max_length=50)
    courier_reference_image = models.ImageField()

    def __str__(self):
        return f"{self.order} {self.courier_reference_no}"


class OrderPickupOther(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    other_pickup_request_date = models.DateTimeField()
    eligible_for_delivery_others = models.BooleanField()
    other_delivery_date = models.DateField()
    pickup_person_name = models.CharField(max_length=50)
    pickup_person_mobile = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.order} {self.pickup_person_name} {self.pickup_person_mobile}"


class OrderPayment(models.Model):
    payment_options = (("self", "SELF"), ("others", "OTHERS"), ("Online", "ONLINE"))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    payment_mode = models.CharField(max_length=20, choices=payment_options)
    payment_date_time = models.DateTimeField(auto_now=True)
    order_payment_reference_no = models.CharField(max_length=20)
    order_payment_reference_image = models.ImageField()

    def __str__(self):
        return f"{self.order} {self.payment_mode} {self.order_payment_reference_no}"


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default="")
    amount_paid = models.IntegerField()
    delivery_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} {self.amount_paid}"


class OrderAlter(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    alter_amount = models.IntegerField()
    alter_booking_date_time = models.DateTimeField()
    alter_due_date_time = models.DateTimeField()
    alter_inst_image = models.ImageField()
    alter_inst_voice = models.FileField()

    def __str__(self):
        return f"{self.order}"


class User(models.Model):
    role_options = (
        ("customer", "CUSTOMER"),
        ("staff", "STAFF"),
        ("admin", "ADMIN"),
        ("proprietor", "PROPRIETOR"),
    )
    login_id = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=20)
    mobile = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=20, choices=role_options)

    def __str__(self):
        return f"{self.login_id} ({self.mobile})"


class TmpWork(models.Model):
    order_id = models.CharField(max_length=10)
    cust_id = models.CharField(max_length=10)
    work_id = models.CharField(max_length=10)
    work_name = models.CharField(max_length=50, default="")
    quantity = models.CharField(max_length=5)
    amount = models.IntegerField(null=True, blank=True)

    total = models.IntegerField()

    def __str__(self):
        return f"{self.order_id}"


class TmpMaterial(models.Model):
    order_id = models.CharField(max_length=10)
    cust_id = models.CharField(max_length=10)
    material_id = models.CharField(max_length=10)
    material_name = models.CharField(max_length=50, default="")
    quantity = models.CharField(max_length=5)
    amount = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.material_name}"


class UploadFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="files")

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.file)

        output = BytesIO()

        x, y = im.size
        x2, y2 = math.floor(x - 50), math.floor(y - 20)
        im = im.resize((x2, y2), Image.ANTIALIAS)

        # Resize/modify the image
        # im = im.resize((300, 300), Image.ANTIALIAS)

        # after modifications, save it to the output
        im.save(output, format="JPEG", quality=30)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.file = InMemoryUploadedFile(
            output,
            "ImageField",
            "%s.jpg" % self.file.name.split(".")[0],
            "image/jpeg",
            sys.getsizeof(output),
            None,
        )

        super(UploadFile, self).save(*args, **kwargs)


class Product(models.Model):
    product_id = models.CharField(max_length=10,primary_key=True)
    product_name = models.CharField(max_length=100)
    picture = models.ImageField(null=True, blank=True, upload_to="product")
    new_arrival = models.BooleanField(default=False)
    display = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return f"{self.product_name}"

    def save(self, *args, **kwargs):
        try:
            # Opening the uploaded image
            im = Image.open(self.picture)

            output = BytesIO()

            x, y = im.size
            x2, y2 = math.floor(x - 50), math.floor(y - 20)
            im = im.resize((x2, y2), Image.ANTIALIAS)

            # Resize/modify the image
            # im = im.resize((300, 300), Image.ANTIALIAS)

            # after modifications, save it to the output
            im.save(output, format="JPEG", quality=30)
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.picture = InMemoryUploadedFile(
                output,
                "ImageField",
                "%s.jpg" % self.picture.name.split(".")[0],
                "image/jpeg",
                sys.getsizeof(output),
                None,
            )

            super(Product, self).save(*args, **kwargs)
        except Exception as e:
            pass


# class ModelName(models.Model):
#     pass
#     def __str__(self):
#         return f'{0}'

# custid
# orderid
# mobile
# picktype
# pickup person 