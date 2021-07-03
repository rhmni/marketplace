from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings



def bank_number_validate(value):
    if len(str(value)) != settings.BANK_NUMBER_LENGTH:
        raise ValidationError(f'bank number must be {settings.BANK_NUMBER_LENGTH} digit')


class Store(models.Model):
    founder = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={
            'is_seller': True,
        },
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    register_date = models.DateTimeField(null=True, blank=True)
    wallet = models.PositiveBigIntegerField(default=0)
    bank_number = models.PositiveBigIntegerField(validators=[bank_number_validate])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.register_date = datetime.now()

        super(Store, self).save(*args, **kwargs)


class StoreCheckout(models.Model):
    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name='checkouts',
    )
    pay_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    bank_number = models.PositiveBigIntegerField(
        validators=[bank_number_validate],
        null=True,
        blank=True,
    )
    amount = models.PositiveBigIntegerField()

    def __str__(self):
        return self.store.name

    def clean(self):

        if not settings.MIN_CHECKOUT <= self.store.wallet:
            raise ValidationError(
                f'amount of your wallet store must more or equal than {settings.MIN_CHECKOUT} toman it is {self.store.wallet}'
            )

        if not settings.MIN_CHECKOUT <= self.amount <= settings.MAX_CHECKOUT:
            raise ValidationError({
                'amount': f'your amount must between {settings.MIN_CHECKOUT} and {settings.MAX_CHECKOUT} toman'}
            )

        if self.amount > self.store.wallet:
            raise ValidationError({
                'amount': f'your amount must be less or equal your wallet it is {self.store.wallet} toman'}
            )

    def save(self, *args, **kwargs):

        if not self.bank_number:
            self.bank_number = self.store.bank_number

        if not self.pay_date:
            self.pay_date = datetime.now()

        if not self.pk:
            self.store.wallet -= self.amount
            self.store.save()

        super(StoreCheckout, self).save(*args, **kwargs)
