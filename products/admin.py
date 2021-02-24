from django.contrib import admin

# Register your models here.

from .models import Product, ProductImage, Variation

#Membuat class ProductAdmin bertujuan untuk mengubah tampilan admin page pada model Product
#admin.ModelAdmin, adalah options yang bisa digunakan untuk kustomisasi interface admin.
#semua options telah didefinisikan di dalam ModalAdmin.
class ProductAdmin(admin.ModelAdmin):
    #date_hierarchy dapat di set dengan model yang menggunakan DateField atau DateTimeField. 
    #Tujuannya agar bisa memfilter data berdasarkan kapan data itu dibuat pada halaman daftar perubahan admin
    #search_fields dapat di set dengan  model yang menggunakan CharField, TextField.
    #Tujuannya agar bisa membuat kolom pencarian pada halaman daftar perubahan admin. Yang dicari judul dan deskripsi.
    #list_display, tujuannya untuk mengontrol fields apa saja yang ditampilkan di halaman daftar perubahan admin.
    #list_editable, tujuannya untuk mengedit fields yang ada di halaman daftar perubahan admin
    #list_filter, tujuannya untuk mengaktifkan filters di kanan sidebar pada halaman daftar perubahan admin.
    #readonly_fields, tujuannya untuk membuat kolom fields tidak bisa edit, hanya bisa dibaca.
    #prepopulated_fields dapat di set dengan dictionary mapping pada nama fields. Biasanya digunakan untuk slug
    #ketika memberi nama di kolom judul, saat itu juga kolom slug akan terisi nama judul dan akan menjadi slug
    date_hierarchy = 'timestamp'
    search_fields = ['title', 'description']
    list_display = ['title', 'price', 'active', 'updated']
    list_editable = ['price', 'active']
    list_filter = ['price', 'active']
    readonly_fields = ['updated', 'timestamp']
    prepopulated_fields = {"slug": ("title",)}
    #class Meta adalah class metadata. Ini optional.
    class Meta:
        model = Product

#register diperlukan agar class dapat muncul di halamnan admin
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Variation)