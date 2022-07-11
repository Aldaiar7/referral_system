from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from referral.models import ReferralRelationship, ReferralCode



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(instance.referral_token)
        ref_code = ReferralCode.objects.filter(token=instance.referral_token).first()
        ref = ReferralRelationship(employer=ref_code.user, employee=instance, refer_token=ref_code)
        ref.save()
        print(f'ref: {ref}')
        
