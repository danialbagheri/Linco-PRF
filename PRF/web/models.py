from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
from django.forms.models import model_to_dict
from datetime import timedelta, date, datetime, timezone

SHRINK_WRAP = (
    ('Standard Clear', 'Standard Clear'),
    ('Black', 'Black'),
    ('Security Tape', 'Security Tape'),
)
STATUS = (
    ('Saved', 'Saved'),
    ('Pending', 'Pending'),
    ('Open', 'Open'),
    ('Reviewing', 'Reviewing'),
    ('On-Hold', 'On-Hold'),
    ('Awaiting Information', 'Awaiting Information'),
    ('In progress', 'In progress'),
    ('Complete', 'Complete'),
)
PALLET_TYPE = (
    ('Standard', 'Standard'),
    ('Europe ', 'Europe'),
    ('Chap', 'Chap'),
    ('Heat Treated', 'Heat Treated'),
    ('Other', 'Other'),
)

class ModelDiffMixin(models.Model):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])
    class Meta:
        abstract = True

# from pif.models import Product, ProductVariant


class RequestType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Logs(models.Model):
    pass


class ModelChangeLogsModel(models.Model):
    '''
    Model to record all other models change logs
    '''
    user_id = models.BigIntegerField(null=False, blank=True, db_index=True) 
    table_name = models.CharField(max_length=132, null=True, blank=True)
    table_id = models.BigIntegerField(null=True, blank=True, db_index=True) 
    table_row = models.CharField(max_length=132, null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    action = models.CharField(max_length=16, null=False, blank=True)  # saved or deleted
    timestamp = models.DateTimeField(null=False, blank=True)

    class Meta:
        app_label = "web"
        db_table = "model_change_logs"

'''
Production list are now delayed for a
'''
# class ProductionList(models.Model):

#     product = models.ForeignKey(
#         ProductVariant, on_delete=models.SET_NULL, null=True, related_name="product_variant")
#     quantity = models.PositiveIntegerField()
#     mfg_date = models.DateField(
#         auto_now=False, blank=True, null=True, help_text="For coding only")
#     expiry_date = models.DateField(
#         auto_now=False, blank=True, null=True, help_text="For coding only")
#     notes = models.TextField()

#     def __str__(self):
#         return self.product.product_code


class ProductionList(ModelDiffMixin):
    '''
    Production list are now delayed for a
    '''
    product = models.CharField(max_length=200, blank=True, null=True,)
    quantity = models.PositiveIntegerField()
    mfg_date = models.DateField(
        auto_now=False, blank=True, null=True, help_text="For coding only")
    expiry_date = models.DateField(
        auto_now=False, blank=True, null=True, help_text="For coding only")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product



class ProductionJob(ModelDiffMixin):
    prf_number = models.IntegerField(null=True, unique=True)
    customer_name = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    requested_date = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    customer_address_id = models.CharField(
        max_length=80, blank=True, null=True)
    request_type = models.ManyToManyField(RequestType, blank=True)
    date_issued = models.DateField(auto_now_add=True)
    required_date = models.DateField(auto_now_add=False)
    expected_completion_date = models.DateField(
        auto_now_add=False, blank=True, null=True)
    completion_date = models.DateField(auto_now_add=False, blank=True, null=True)
    production_list = models.ManyToManyField(
        ProductionList, blank=True)
    pallet_type = models.CharField(
        max_length=30, choices=PALLET_TYPE, blank=True, null=True)
    expiry_date_format = models.CharField(
        max_length=30, blank=True, null=True)
    shrink_wrap = models.CharField(
        max_length=30, choices=SHRINK_WRAP, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=30, choices=STATUS, blank=True, null=True)
    address_label = models.BooleanField(default=False)


    @property
    def is_past_due(self):
        from_date = self.requested_date
        number_of_days = 3
        today = datetime.now(timezone.utc)
        to_date = from_date
        while number_of_days:
            to_date += timedelta(1)
            if to_date.weekday() < 5: # i.e. is not saturday or sunday
                number_of_days -= 1      
        if to_date < today and self.status == 'Pending':
            return True
        else:
            return False

    @property
    def is_late(self):
        from_date = self.requested_date
        number_of_days = 2
        today = datetime.now(timezone.utc)
        to_date = from_date
        while number_of_days:
            to_date += timedelta(1)
            if to_date.weekday() < 5: # i.e. is not saturday or sunday
                number_of_days -= 1      
        if to_date < today and self.status == 'Pending':
            return True
        else:
            return False
    
    def __str__(self):
        return str(self.prf_number)
