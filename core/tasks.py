from celery import shared_task 
from user.models import User
from referral.models import ReferralRelationship


@shared_task
def count_points():
    users = User.objects.all()
    print('count-points')
    for user in users:
        user.points = 0
        user.save()
        parent = ReferralRelationship.objects.filter(employee=user.id).first()
        n = ReferralRelationship.objects.filter(employer=user.id).count()
        print(f'user:{user} referral_relationship:{parent}')
        if n == 0:
            continue
        n+=1
        user.points += 1
        user.save()
        n -= 1
        
        if parent:
            while n > 0:
                profile = User.objects.filter(pk=parent.employer.id).first()
                profile.points += 1
                profile.save()
                n-= 1
                parent = ReferralRelationship.objects.filter(employee=profile.id).first()
                if not parent:
                    profile.points += n 
                    profile.save()
                    n -= n
                else:
                    profile = User.objects.filter(pk=parent.employer.id).first()
                    profile.points += 1
                    profile.save()
        else:
            user.points += n
            user.save()
                
