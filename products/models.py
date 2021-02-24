from django.db import models
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    #null=False, tidak memperbolehkan ada kolom yang kosong/tidak bernilai
    #blank=False, tidak memperbolehkan ada kolom yang tidak diisi oleh user
    #timestamp bertujuan untuk merekam waktu disaat data sedang disimpan/diperbarui
    #updated bertujuan untuk menampilkan waktu terkini sehingga memperlihatkan selisih waktu dari timestamp
    #slug bertujuan untuk membuat keywords url dan dihubungkan dengan strip, contohnya: ../tanaman-hias-anggrek-sonia/
    #active untuk mengaktifkan/menon-aktifkan product
    #tile untuk judul, description untuk deskripsi
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    price = models.IntegerField()
    # image = models.FileField(upload_to='products/images', max_length=100, null=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'slug')

    def get_absolute_url(self):
        return reverse("single_product", kwargs={"slug": self.slug})
    


class ProductImage(models.Model):
    #untuk mengasosiasikan gambar dan product kita perlu membuat relasi foreignkey antara Model Product dan ProductImage
    #verbose_name adalah nama dengan bahasa manusia untuk ditampilkan kepada user.
    #on_delete=model.cascade diperlukan oleh tabel dengan foreignkey
    #karena apabila menghapus data di tabel 'parent' maka data yang ada di tabel 'child' juga akan terhapus.
    #hal ini diperlukan agar terhindar dari duplikasi data
    #untuk upload image memerlukan direktori yang spesifik seperti 'app/images'
    product = models.ForeignKey("products.Product", verbose_name=("Product"), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images', height_field=None, width_field=None, max_length=None)
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.product.title
    

class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def colors(self):
        return self.all().filter(category='color')


VAR_CATEGORIES = (
    ('color', 'color'),
)

    
class Variation(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='color')
    title = models.CharField(max_length=120)
    image = models.ForeignKey("products.ProductImage", on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = VariationManager()

    def __str__(self):
        return self.title
    




