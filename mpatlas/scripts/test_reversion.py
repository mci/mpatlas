import reversion
from django.db import connection, transaction
from reversion.models import Revision
from mpa.models import Mpa, Contact, WikiArticle, VersionMetadata

@transaction.commit_on_success
def test():
    with reversion.create_revision():        
        mpa = Mpa.objects.get(pk=3)
        mpa.summary = 'TEST'
        mpa.save()
        reversion.set_comment("Test comment.")

@transaction.commit_on_success
def test2():    
    rcm = reversion.revision_context_manager
    rc = rcm.create_revision()
    #rcm.start(manage_manually=False)
    rcm.start(manage_manually=True)
    print rcm.is_active(), rcm.is_invalid(), rcm.is_managing_manually()
    mpa = Mpa.objects.get(pk=2)
    mpa.summary = 'Test1'
    mpa.save()
    rcm.set_comment('Test comment')
    rcm.end()
    return (mpa, rcm, rc)

mpa, rcm, rc = test2()
print mpa.summary
print reversion.get_for_object(mpa)