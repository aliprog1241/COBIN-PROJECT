from django.db.models import Sum, Count, F
from .models import Account, Admin, Rider, Driver, Car, RideRequest, Ride, Payment


def query_1():
    q = Payment.objects.aggregate(income=Sum('amount'))
    return q


def query_2(x):
    q = Payment.objects.filter(ride__request__rider__id=x).aggregate(payment_sum=Sum('amount'))
    return q


def query_3():
    q = Driver.objects.filter(car__car_type='A').distinct().count()
    return q


def query_4():
    q = RideRequest.objects.filter(ride__isnull=True)
    return q


def query_5(t):
    q = Rider.objects.annotate(total=Sum('riderequest__ride__payment__amount')) \
                     .filter(total__gte=t)
    return q


def query_6():
    q = Account.objects.filter(driver__isnull=False) \
        .annotate(n=Count('driver__car')) \
        .order_by('-n', 'last_name') \
        .first()
    return q


def query_7():
    q = Rider.objects.filter(riderequest__ride__car__car_type='A') \
                     .annotate(n=Count('riderequest__ride', filter=F('riderequest__ride__car__car_type')=='A')) \
                     .distinct()
    return q


def query_8(x):
    q = Driver.objects.filter(car__model__gte=x) \
                      .values('account__email') \
                      .distinct()
    return q


def query_9():
    q = Driver.objects.annotate(n=Count('car__ride'))
    return q


def query_10():
    q = Driver.objects.values('account__first_name') \
                      .annotate(n=Count('car__ride')) \
                      .values(first_name=F('account__first_name')) \
                      .annotate(n=Sum('n'))
    return q


def query_11(c, n):
    q = Driver.objects.filter(car__color=c, car__model__gte=n).distinct()
    return q


def query_12(c, n):
    q = Driver.objects.filter(car__color=c).filter(car__model__gte=n).distinct()
    return q


def query_13(n, m):
    q = Ride.objects.filter(car__owner__account__first_name=n,
                            request__rider__account__first_name=m) \
                    .aggregate(sum_duration=Sum(F('dropoff_time') - F('pickup_time')))
    return q
