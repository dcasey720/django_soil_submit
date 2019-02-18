from django.db import models
from django.utils import timezone
from geoposition import Geoposition
from geoposition.fields import GeopositionField

# Create your models here.

class Sample(models.Model):
    TEST_CHOICES = ((('1'),('Soil 1-SS Basic')),
                    (('2'),('Soil 2-SS Dairy/Beef/Sheep/Horses')),
                    (('3'),('Soil 3-SS Sheep/Tillage')),
                    (('4'),('Soil 4-SS Tillage')),
                    (('5'),('Soil 5-SS Horticulture')),
                    (('6'),('Soil 6-SS Tillage/Grassland (S1 + Mg)')),
                    (('7'),('Soil 7-SS Organic Matter')),
                    (('8'),('Soil 8-SS Tillage (S6 + S7)')),
                    (('9'),('Soil 9-SS Tillage (S4 + S7)')))

    SOIL_TYPES = ((('GW'),('Well-graded gravel, fine to coarse gravel')),
                  (('GP'),('Poorly graded gravel')),
                  (('GM'),('Silty gravel')),
                  (('GC'),('Clayey gravel')),
                  (('SW'),('Well-graded sand, fine to coarse sand')),
                  (('SP'),('Poorly graded sand')),
                  (('SM'),('Silty sand')),
                  (('SC'),('Clayey sand')),
                  (('ML'),('Silt')),
                  (('CL'),('Clay of low plasticity, lean clay')),
                  (('OL'),('Organic silt, organic clay')),
                  (('MH'),('Silt of high plasticity, elastic silt')),
                  (('CH'),('Clay of high plasticity, fat clay')),
                  (('OH'),('Organic clay, organic silt')),
                  (('Pt'),('Peat')))

    LAND_USES = ((('B'), ('Beef')),
                 (('D'), ('Dairy')),
                 (('G'), ('Grassland')),
                 (('H'), ('Horticulture')),
                 (('S'), ('Sheep')),
                 (('T'), ('Tillage')))

    STATUS_CHOICES = ((('Submitted'),('Submitted')),
                      (('Received'),('Received')),
                      (('Testing'),('Testing')),
                      (('Complete'),('Complete')))

    username = models.CharField(max_length=50, blank=False)
    location = GeopositionField()
    sample_ref = models.CharField(max_length=50, blank=False)
    analysis_req = models.CharField(max_length=50, choices=TEST_CHOICES, blank=True)
    customer_ref = models.CharField(max_length=50, blank=True)
    soil_type = models.CharField(max_length=2, choices=SOIL_TYPES, blank=True, default='')
    land_use = models.CharField(max_length=1, choices=LAND_USES, blank=True, default='')
    other_comments = models.CharField(max_length=50, blank=True)
    sample_condition = models.CharField(max_length=50, blank=True)
    sample_date = models.DateField(default=timezone.now())
    submit_date = models.DateField(blank=True)
    recieved_date = models.DateField(blank=True, null=True)
    test_start_date = models.DateField(blank=True, null=True)
    test_end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Submitted')

    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.sample_ref, self.status)

class ResultsLineItem(models.Model):
    sample = models.ForeignKey(Sample, null=False)
    p_morgan_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    k_morgan_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    lr_ph_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    ph_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    mg_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    cu_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    zn_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    er_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    mn_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    organic_result = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    def __str__(self):
        return "{0} {1} @ {2}".format(self.p_morgan_result, self.k_morgan_result, self.lr_ph_result)