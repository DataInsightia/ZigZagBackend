# Generated by Django 4.0.2 on 2022-03-08 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cust_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('cust_name', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=13, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=8)),
                ('address', models.TextField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('material_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('material_name', models.CharField(max_length=100)),
                ('measurement', models.CharField(choices=[('number', 'NUMBER'), ('inch', 'INCH'), ('meter', 'METER')], max_length=20)),
                ('amount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(default='', max_length=10, primary_key=True, serialize=False)),
                ('booking_date_time', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateField()),
                ('order_image', models.ImageField(blank=True, upload_to='')),
                ('material_image', models.ImageField(blank=True, upload_to='')),
                ('order_voice_inst', models.CharField(blank=True, max_length=10)),
                ('pickup_type', models.CharField(choices=[('self', 'SELF'), ('courier', 'COURIER'), ('others', 'OTHERS')], max_length=20)),
                ('total_amount', models.IntegerField(blank=True, null=True)),
                ('advance_amount', models.IntegerField(blank=True, null=True)),
                ('balance_amount', models.IntegerField(blank=True, null=True)),
                ('customer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='', max_length=20)),
                ('material_id', models.CharField(default='', max_length=20)),
                ('quantity', models.CharField(default='', max_length=20)),
                ('amount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='', max_length=20)),
                ('work_id', models.CharField(default='', max_length=20)),
                ('order_work_item', models.CharField(default='', max_length=20)),
                ('quantity', models.CharField(default='', max_length=20)),
                ('amount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderWorkStaffAssign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_work_label', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('assign_stage', models.CharField(blank=True, choices=[('cutting', 'CUTTING'), ('stitching', 'STITCHING'), ('hook', 'HOOK'), ('overlock', 'OVERLOCK'), ('complete_final_stage', 'COMPLETE FINAL STAGE')], max_length=50, null=True)),
                ('assign_date_time', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('staff_name', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=13)),
                ('address', models.TextField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('salary_type', models.CharField(choices=[('monthly', 'MONTHLY'), ('wage', 'WAGE')], max_length=20)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('acc_no', models.CharField(max_length=16)),
                ('bank', models.CharField(max_length=300)),
                ('ifsc', models.CharField(max_length=20)),
                ('work_type', models.CharField(choices=[('tailor', 'TAILOR'), ('aari', 'AARI'), ('embroidery', 'EMBROIDERY'), ('photo', 'PHOTO')], max_length=20)),
                ('photo', models.ImageField(blank=True, default='', null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='TmpMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=10)),
                ('cust_id', models.CharField(max_length=10)),
                ('material_id', models.CharField(max_length=10)),
                ('material_name', models.CharField(default='', max_length=50)),
                ('quantity', models.CharField(max_length=5)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TmpWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=10)),
                ('cust_id', models.CharField(max_length=10)),
                ('work_id', models.CharField(max_length=10)),
                ('work_name', models.CharField(default='', max_length=50)),
                ('quantity', models.CharField(max_length=5)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_id', models.CharField(max_length=10, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=13, unique=True)),
                ('role', models.CharField(choices=[('customer', 'CUSTOMER'), ('staff', 'STAFF'), ('admin', 'ADMIN'), ('proprietor', 'PROPRIETOR')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('work_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('work_name', models.CharField(max_length=50)),
                ('wage_type', models.CharField(choices=[('full', 'FULL'), ('half', 'HALF'), ('10half', '10HALF')], max_length=10)),
                ('amount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaffWorkWage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_staff_approval_date_time', models.DateTimeField(blank=True, null=True)),
                ('completion_date_time', models.DateTimeField(blank=True, null=True)),
                ('wage', models.IntegerField(blank=True, default=0, null=True)),
                ('wage_given', models.BooleanField(blank=True, default=False, null=True)),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('staff', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.staff')),
                ('work', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.work')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffWageGivenStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wage_from_date', models.DateField()),
                ('wage_to_date', models.DateField()),
                ('wage_given_date', models.DateField()),
                ('total_wage_given', models.IntegerField()),
                ('wage_payment_reference_no', models.CharField(max_length=50)),
                ('wage_payment_reference_image', models.ImageField(upload_to='')),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('staff', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.staff')),
                ('work', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.work')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderWorkStaffTaken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taken_stage', models.CharField(blank=True, choices=[('cutting', 'CUTTING'), ('stitching', 'STITCHING'), ('hook', 'HOOK'), ('overlock', 'OVERLOCK'), ('complete_final_stage', 'COMPLETE FINAL STAGE')], max_length=50, null=True)),
                ('taken_date_time', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('orderworkstaffassign', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.orderworkstaffassign')),
            ],
        ),
        migrations.CreateModel(
            name='OrderWorkStaffStatusCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_staff_completion_stage', models.CharField(blank=True, choices=[('cutting', 'CUTTING'), ('stitching', 'STITCHING'), ('hook', 'HOOK'), ('overlock', 'OVERLOCK'), ('complete_final_stage', 'COMPLETE FINAL STAGE')], max_length=50, null=True)),
                ('work_completed_date_time', models.DateTimeField(blank=True, null=True)),
                ('work_staff_comp_app_date_time', models.DateTimeField(blank=True, null=True)),
                ('work_staff_completion_approved', models.BooleanField(default=False)),
                ('order_next_stage_assign', models.BooleanField(default=False)),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('orderworkstaffassign', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.orderworkstaffassign')),
                ('staff', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.staff')),
            ],
        ),
        migrations.AddField(
            model_name='orderworkstaffassign',
            name='staff',
            field=models.ForeignKey(blank=True, db_constraint=False, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.staff'),
        ),
        migrations.AddField(
            model_name='orderworkstaffassign',
            name='work',
            field=models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.CASCADE, to='api.work'),
        ),
        migrations.CreateModel(
            name='OrderPickupOther',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_pickup_request_date', models.DateTimeField()),
                ('eligible_for_delivery_others', models.BooleanField()),
                ('other_delivery_date', models.DateField()),
                ('pickup_person_name', models.CharField(max_length=50)),
                ('pickup_person_mobile', models.CharField(max_length=13)),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPickupCourier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('courier_request_date', models.DateField()),
                ('courier_amount', models.IntegerField()),
                ('eligible_for_courier', models.BooleanField()),
                ('courier_company', models.CharField(max_length=50)),
                ('courier_date', models.DateField()),
                ('courier_reference_no', models.CharField(max_length=50)),
                ('courier_reference_image', models.ImageField(upload_to='')),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_mode', models.CharField(choices=[('self', 'SELF'), ('others', 'OTHERS'), ('Online', 'ONLINE')], max_length=20)),
                ('payment_date_time', models.DateTimeField(auto_now=True)),
                ('order_payment_reference_no', models.CharField(max_length=20)),
                ('order_payment_reference_image', models.ImageField(upload_to='')),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMaterialLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_location', models.CharField(max_length=20)),
                ('location_placed_date_time', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('staff', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.staff')),
            ],
        ),
        migrations.CreateModel(
            name='OrderAlter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alter_amount', models.IntegerField()),
                ('alter_booking_date_time', models.DateTimeField()),
                ('alter_due_date_time', models.DateTimeField()),
                ('alter_inst_image', models.ImageField(upload_to='')),
                ('alter_inst_voice', models.FileField(upload_to='')),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.IntegerField()),
                ('delivery_date_time', models.DateTimeField()),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('staff', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.staff')),
            ],
        ),
    ]
